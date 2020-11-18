from lxml import etree
import os

from .path_utils import get_relevant_info
from .stats_utils import get_lang_to_naf_paths

from rdflib.namespace import Namespace
from rdflib.namespace import RDF, RDFS
from rdflib import Graph
from rdflib import URIRef, Literal, XSD


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
