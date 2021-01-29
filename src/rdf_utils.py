from lxml import etree
import os
import time
from datetime import datetime
from collections import defaultdict
import inspect
import sys
import json

from .path_utils import get_relevant_info
from .stats_utils import get_lang_to_naf_paths

from rdflib.namespace import Namespace
from rdflib.namespace import RDF
from rdflib import Graph
from rdflib import URIRef, Literal, XSD

import requests


WDT_SPARQL_URL = 'https://query.wikidata.org/sparql'
BATCH_SIZE = 100  # at 500 the api calls do not work anymore
DEV_LIMIT = 1000000  # how many items do you want to have when you put verbose to 4 or higher
NUM_RETRIES = 5  # after how many retries do you give up
LOG_BATCHES = False  # if True, send information about each batch to stdout
OVERWRITE = True  # if True, overwrite existing results
LANGUAGE_ORDER = ['en', 'nl']


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def call_wikidata(sparql_query,
                  query_name,
                  verbose=0):
    """
    call wikidata sparql query and optionally store results in
    OUTPUT_FOLDER/QUERY_NAME.json

    :param str sparql_query: the sparql query
    :param str query_name: name of the query

    :rtype: dict
    :return: response
    """
    response = get_results_with_retry(wdt_sparql_url=WDT_SPARQL_URL,
                                      query=sparql_query)

    post_process_function = globals()[f'post_process_{query_name}']

    post_processed = post_process_function(response, verbose=verbose)

    return post_processed


def get_results_with_retry(wdt_sparql_url, query):
    """
    Run SPARQL query multiple times until the results are there.

    :param str wdt_sparql_url: the Wikidata sparql url
    :param str query: the query to execute

    :rtype: dict
    :return: response from api
    """
    num_attempts = 0
    while True:
        try:
            r = requests.get(wdt_sparql_url,
                             params={'format': 'json', 'query': query})
            response = r.json()
            break
        except Exception as e:
            sys.stderr.write(f'{e},error, retrying\n')
            num_attempts += 1
            time.sleep(2)

            if num_attempts == NUM_RETRIES:
                print(f'unable to run query: {query}')
                response = {'results': {'bindings': []}}
                break

            continue

    return response


def post_process_labels(response, verbose=0):
    """
    postprocess the response of the "inc_to_labels" query

    :param dict response: api response

    :rtype: set of tuples
    :return: {(incident_wd_uri,
               english_label)}
    """
    qid_to_labels = defaultdict(dict)

    for info in response['results']['bindings']:
        uri = info['q_id']['value']
        qid = uri.replace('http://www.wikidata.org/entity/', '')
        label = info['label']['value']
        lang = info['lang']['value']
        qid_to_labels[qid][lang] = label

    if verbose >= 2:
        this_function_name = inspect.currentframe().f_code.co_name
        print('INSIDE FUNCTION', this_function_name)
        print(f'found {len(qid_to_labels)} incidents with at least label in Italian, English, and Dutch')

    qid_to_dropdown_label = {}
    for qid, labels in qid_to_labels.items():
        for lang in LANGUAGE_ORDER:
            value = labels.get(lang)
            if value is not None:
                qid_to_dropdown_label[qid] = f'{value}@{lang} ({qid})'
                break

        dropdown_label = qid_to_dropdown_label.get(qid)
        if dropdown_label is None:
            qid_to_dropdown_label[qid] = qid

    return qid_to_dropdown_label


def get_labels(set_of_q_ids,
               output_path=None,
               verbose=0):
    """

    :param set set_of_q_ids: {"Q62090804", "Q699872"}
    :return:
    """
    sparql_query = """SELECT ?q_id ?label ?lang WHERE {
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
      VALUES ?q_id { %s }
      ?q_id rdfs:label ?label .
      filter(lang(?label) = 'en' || lang(?label) = 'nl')
      BIND(lang(?label) as ?lang)
    }"""

    count = 0
    post_processed = dict()
    for batch in chunks(list(set_of_q_ids), BATCH_SIZE):

        if verbose >= 2:
            print()
            print(f'working on batch starting from index {count} ({datetime.now()})\n')

        list_of_wd_ids = [f'wd:{qid}' for qid in batch
                                 if qid.startswith('Q')]

        if list_of_wd_ids:
            items_string = ' '.join(list_of_wd_ids)
            the_query = sparql_query % items_string

            if verbose >= 5:
                print(the_query)

            part_post_processed = call_wikidata(sparql_query=the_query,
                                                query_name='labels',
                                                verbose=verbose)
        else:
            part_post_processed = {}

        for item in batch:
            value = part_post_processed.get(item, item)
            post_processed[item] = value

        count += len(batch)

    if output_path is not None:
        with open(output_path, 'w') as outfile:
            json.dump(post_processed, outfile)
        if verbose >= 1:
            print(f'written event and incident labels to {output_path}')

    return post_processed


def convert_to_sem(repo_dir,
                   project,
                   wd_prefix='http://www.wikidata.org/entity/',
                   verbose=0):
    """
    Serialize a collection of incidents to a .ttl file.

    :param str repo_dir: use DFNDataReleases.dir_path
    :param str project: name of project for which you want to compute statistics
    :param int verbose: different levels of debugging information
    """
    relevant_info = get_relevant_info(repo_dir=repo_dir,
                                      project=project,
                                      start_from_scratch=False, # do not remove statistics folder if it exists
                                      verbose=verbose)

    # instance-level
    project_incs = set(relevant_info['proj2inc']['HistoricalDistanceData'])
    if verbose >= 1:
        print()
        print(f'found {len(project_incs)} incidents for project {project}')

    incid_to_lang_to_naf_paths, \
    languages = get_lang_to_naf_paths(relevant_info=relevant_info,
                                      project_incs=project_incs,
                                      verbose=verbose)


    # initialize graph
    g = Graph()

    # Namespaces definition
    SEM = Namespace('http://semanticweb.cs.vu.nl/2009/11/sem/')
    GRASP = Namespace('http://groundedannotationframework.org/grasp#')
    DCT = Namespace('http://purl.org/dc/elements/1.1/')
    g.bind('sem', SEM)
    g.bind('grasp', GRASP)
    g.bind('dct', DCT)

    # update graph
    for inc_id in project_incs:
        inc_uri = URIRef(f'{wd_prefix}{inc_id}')

        # event type information
        inc_type = relevant_info['inc2type'][inc_id]
        inc_type_uri = f'{wd_prefix}{inc_type}'
        inc_type_uri = URIRef(inc_type_uri)

        g.add((inc_uri, RDF.type, SEM.Event))
        g.add((inc_uri, SEM.eventType, inc_type_uri))

        if verbose >= 3:
            print()
            print('INCIDENT URI {inc_uri}')

        # event labels in all languages
        lang_to_naf_paths = incid_to_lang_to_naf_paths[inc_id]

        for lang, naf_paths in lang_to_naf_paths.items():
            for naf_path in naf_paths:

                doc = etree.parse(naf_path)
                file_desc_el = doc.find('nafHeader/fileDesc')
                public_el = doc.find('nafHeader/public')
                raw_el = doc.find('raw')

                title = file_desc_el.get('title')
                ref_text_uri = public_el.get('uri')
                content = raw_el.text

                ref_text_uriref = URIRef(ref_text_uri)
                g.add((inc_uri, GRASP.denotedIn, ref_text_uriref))
                g.add((ref_text_uriref, DCT.description, Literal(content)))
                g.add((ref_text_uriref, DCT.title, Literal(title)))
                g.add((ref_text_uriref, DCT.language, Literal(lang)))
                g.add((ref_text_uriref, DCT.type, URIRef('http://purl.org/dc/dcmitype/Text')))

        # update structured data
        inc_str_data = relevant_info['inc2str'][inc_id]

        # location and actor
        key_to_url = {f'{key}' : f'{SEM}{key.split(":")[1]}'
                      for key in ['sem:hasActor', 'sem:hasPlace', 'sem:hasTimeStamp']
                      }

        for short, long in key_to_url.items():
            values = inc_str_data.get(short, [])

            for value in values:

                value_uri, value_label = value.split(' | ')

                if short in {'sem:hasActor', 'sem:hasPlace'}:
                    an_obj = URIRef(value_uri)

                if short == 'sem:hasTimeStamp':
                    an_obj = Literal(value_uri, datatype=XSD.date)

                g.add((inc_uri, # incident uri
                       URIRef(long),  # full SEM relationship
                       an_obj)) # the value of the SEM relationship

    # Done. Store the resulting .ttl file now...
    output_path = os.path.join(relevant_info['project_statistics'],
                               'sem.ttl')
    g.serialize(format='turtle', destination=output_path)
    if verbose >= 1:
        print(f'written SEM representation of project {project} to {output_path}')
