import os
from collections import Counter
from collections import defaultdict
import statistics

from .path_utils import get_relevant_info

import pandas
from lxml import etree

# TODO: totals structured data
# number of rel1
# number of rel2
# number of rel3
# number of annotated rel1
# number of annotated rel2
# number of annotated rel3


WD_PREFIX = 'http://www.wikidata.org/entity/'

SEM_RELS = [
    "sem:hasPlace",
    "sem:hasTimeStamp",
    "sem:hasActor",
]

def get_lang_to_naf_paths(relevant_info,
                          project_incs,
                          verbose=0):
    """

    :param dict relevant_info: see path_utils.get_relevant_info
    :param set project_incs: the incident ids relevant to the chosen project

    :rtype: dict
    :return: mapping of lang -> set of naf_paths
    """
    incid_to_lang_to_naf_paths = {}
    languages = set()

    for inc_id in project_incs:
        rel_naf_paths = relevant_info['inc2doc'][inc_id]
        incid_to_lang_to_naf_paths[inc_id] = defaultdict(set)

        for rel_naf_path in rel_naf_paths:
            lang, basename = rel_naf_path.split('/', 1)
            absolute_path = os.path.join(relevant_info['unstructured'],
                                         lang,
                                         f'{basename}.naf')
            assert os.path.exists(absolute_path), f'{absolute_path} does not exist.'

            incid_to_lang_to_naf_paths[inc_id][lang].add(absolute_path)
            languages.add(lang)

    return incid_to_lang_to_naf_paths, sorted(languages)




def get_stats(repo_dir,
              project,
              verbose=0):
    """
    compute statistics based on the specified functions
    and combine them into one html file

    :param str repo_dir: use DFNDataReleases.dir_path
    :param str project: name of project for which you want to compute statistics
    :param list functions: the name of the functions to call
    :param int verbose: different levels of debugging information
    """
    relevant_info = get_relevant_info(repo_dir=repo_dir,
                                      project=project,
                                      verbose=verbose)

    # instance-level
    project_incs = set(relevant_info['proj2inc']['HistoricalDistanceData'])
    if verbose >= 1:
        print()
        print(f'found {len(project_incs)} incidents for project {project}')

    incid_to_lang_to_naf_paths,\
    languages = get_lang_to_naf_paths(relevant_info=relevant_info,
                                                   project_incs=project_incs,
                                                   verbose=verbose)


    event_type_to_inc_df = get_event_type_to_inc_df(relevant_info=relevant_info,
                                                    project_incs=project_incs)


    inc_to_lang_df = get_inc_to_lang_df(incid_to_lang_to_naf_paths=incid_to_lang_to_naf_paths,
                                        languages=languages)

    inc_to_str_df = get_inc_to_str_df(relevant_info=relevant_info,
                                      project_incs=project_incs)


    ref_text_to_pred_df = get_ref_text_to_pred_df(incid_to_lang_to_naf_paths=incid_to_lang_to_naf_paths,
                                                  project_incs=project_incs)



    # distributions
    distribution_df = get_distributions_df(event_type_to_inc_df=event_type_to_inc_df,
                                           inc_to_lang_df=inc_to_lang_df)


    # totals
    totals_df = get_totals_df(event_type_to_inc_df,
                              inc_to_lang_df)

    totals_conceptual_df = get_totals_conceptual_df(ref_text_to_pred_df)


    # write to disk
    name_to_df = {
        'Totals' : (totals_df, True),
        'Conceptual totals' : (totals_conceptual_df, True),
        'Distributions' : (distribution_df, True),
        'Event type -> Incidents' : (event_type_to_inc_df, True),
        'Incidents -> Languages' : (inc_to_lang_df, True),
        'Incidents -> Structured Data' : (inc_to_str_df, True),
        'Predicates and Frame Elements' : (ref_text_to_pred_df, False)
    }
    write_to_disk(relevant_info=relevant_info,
                  name_to_df=name_to_df,
                  verbose=verbose)


def get_totals_conceptual_df(ref_text_to_pred_df):

    list_of_lists = []
    headers = ['Predicates',
               'Manual predicates',
               'Automatic predicates',
               'Frame elements',
               'Manual frame elements',
               'Automatic frame elements']

    columns = ['# of predicates',
               '# of manual predicates',
               '# of automatic predicates',
               '# of frame elements',
               '# of manual frame elements',
               '# of automatic frame elements']

    one_row = []
    for column in columns:
        total = sum(ref_text_to_pred_df[column])
        one_row.append(total)

    list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df



def get_totals_df(event_type_to_inc_df,
                  inc_to_lang_df):

    list_of_lists = []
    headers = ['Metric', "Total"]

    one_row = ['Event types', len(event_type_to_inc_df)]
    list_of_lists.append(one_row)

    one_row = ['Incidents', sum(event_type_to_inc_df['# of Incidents'])]
    list_of_lists.append(one_row)

    one_row = ['Reference Texts', sum(inc_to_lang_df['Total # of Reference Texts'])]
    list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df

def write_to_disk(relevant_info,
                  name_to_df,
                  verbose=0):

    main_html_path = os.path.join(relevant_info['project_statistics'],
                                  'descriptive_statistics.html')
    components = []
    html_start = '<html>\n<body>\n'
    components.append(html_start)

    for name, (df, include) in name_to_df.items():

        df_path = os.path.join(relevant_info['project_statistics'], f'{name}.csv')
        df.to_csv(df_path, index=False)
        if verbose >= 1:
            print()
            print(f'written {name} to {df_path}')

        if include:
            header = f'<h2>{name}</h2>'
            components.append(header)

        html_path = os.path.join(relevant_info['project_statistics'], f'{name}.html')
        html_table = df.to_html(index=False,
                                border=0,
                                justify="center")

        if include:
            components.append(html_table)

        df.to_html(html_path,
                   index=False,
                   border=0,
                   justify='center')

        if verbose >= 1:
            print(f'written {name} to {html_path}')

    html_end = '</body>\n</html>'
    components.append(html_end)

    html = ''.join(components)

    with open(main_html_path, 'w') as outfile:
        outfile.write(html)

    if verbose >= 1:
        print(f'written the descriptive statistics to {main_html_path}')





def get_distributions_df(event_type_to_inc_df,
                         inc_to_lang_df):
    list_of_lists = []
    headers = ['Metric', 'Minimum', 'Mean', 'Maximum']

    minimum, mean, maximum = get_distribution(a_df=event_type_to_inc_df,
                                              column_to_count='# of Incidents')
    one_row = ['Event type -> Incidents', minimum, round(mean, 2), maximum]
    list_of_lists.append(one_row)

    minimum, mean, maximum = get_distribution(a_df=inc_to_lang_df,
                                              column_to_count='Total # of Reference Texts')
    one_row = ['Incidents -> Reference Texts', minimum, round(mean, 2), maximum]
    list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df




def get_distribution(a_df,
                     column_to_count):

    values = a_df[column_to_count]

    minimum = min(values)
    mean = statistics.mean(values)
    maximum = max(values)

    return [minimum, mean, maximum]

def get_event_type_to_inc_df(relevant_info,
                             project_incs):


    event_id_to_incidents = defaultdict(set)

    for ev_type, inc_ids in relevant_info['type2inc'].items():

        ev_type_uri = f'{WD_PREFIX}{ev_type}'
        for inc_id in inc_ids:

            if inc_id in project_incs:
                inc_uri = f'{WD_PREFIX}{inc_id}'
                event_id_to_incidents[ev_type_uri].add(inc_uri)


    list_of_lists = []
    headers = ['Event type', '# of Incidents']

    for event_id, incidents in event_id_to_incidents.items():
        list_of_lists.append([event_id,
                              len(incidents)])

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df





def get_inc_to_lang_df(incid_to_lang_to_naf_paths,
                       languages):

    list_of_lists = []
    headers = ['Incident', 'Total # of Reference Texts'] + languages

    for inc_id, lang_to_naf_paths in incid_to_lang_to_naf_paths.items():

        one_row = [f'{WD_PREFIX}{inc_id}']

        total = 0
        for lang in languages:
            naf_paths = lang_to_naf_paths[lang]
            one_row.append(len(naf_paths))
            total += len(naf_paths)

        one_row.append(total)
        list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df


def get_inc_to_str_df(relevant_info,
                      project_incs):

    list_of_lists = []
    headers = ['Incident'] + SEM_RELS

    for inc_id in project_incs:

        one_row = [f'{WD_PREFIX}{inc_id}']

        for sem_rel in SEM_RELS:
            values = relevant_info['inc2str'][inc_id].get(sem_rel, [])

            one_row.append(len(values))

        list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)

    return df


def get_ref_text_to_pred_df(incid_to_lang_to_naf_paths,
                            project_incs):

    list_of_lists = []
    headers = ['Incident',
               'ReferenceText',
               '# of tokens',
               '# of types',
               '# of predicates',
               '# of manual predicates',
               '# of automatic predicates',
               '# of frame elements',
               '# of manual frame elements',
               '# of automatic frame elements']


    for inc_id, lang_to_naf_paths in incid_to_lang_to_naf_paths.items():

        if inc_id not in project_incs:
            continue

        for lang, naf_paths in lang_to_naf_paths.items():
            for naf_path in naf_paths:

                doc = etree.parse(naf_path)

                num_types = len({term_el.get('lemma') for term_el in doc.xpath('terms/term')})
                pred_els = doc.findall('srl/predicate')

                manual_pred = 0
                automatic_pred = 0

                for pred_el in pred_els:
                    status = pred_el.get('status')
                    if status == 'manual':
                        manual_pred += 1
                    elif status == 'system':
                        automatic_pred += 1

                manual_fe = 0
                automatic_fe = 0

                for fe_el in doc.xpath('srl/predicate/role'):
                    status = fe_el.get('status')
                    if status == 'manual':
                        manual_fe += 1
                    elif status == 'system':
                        automatic_fe += 1


                one_row = [
                    f'{WD_PREFIX}{inc_id}',
                    os.path.basename(naf_path),
                    len(doc.findall('text/wf')),
                    num_types,
                    manual_pred + automatic_pred,
                    manual_pred,
                    automatic_pred,
                    manual_fe + automatic_fe,
                    manual_fe,
                    automatic_fe
                ]
                list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)
    return df



def print_dict_stats(a_dict,
                     dict_label='dict',
                     key_label='keys',
                     value_label='values',
                     metric='count'):
    """
    print the number of keys and values in a dict
    you can indicate what the keys and values mean using the keyword parameters

    :param dict a_dict: a dict
    :param str key_label: optionally, a label to clarify what the keys are
    :param str value_label: optionally, a label to clarify what the keys are
    :param str metric: count | length_distribution
    """
    print()
    print(f'information about dictionary: {dict_label}')
    print(f'found {len(a_dict.keys())} {key_label}')

    if metric == 'count':
        print(f'found {len(a_dict.values())} {value_label}')
    elif metric == 'length_distribution':
        distribution = Counter([len(value)
                                for value in a_dict.values()])
        print(f'{value_label}: {distribution}')
