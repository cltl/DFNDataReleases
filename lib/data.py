import os
import pickle
import sys
import json
import shutil
from collections import defaultdict

from .stats_utils import  print_dict_stats


def integrate_data(json_dir,
                   source_naf_dir,
                   target_naf_dir,
                   path_inc_coll_obj,
                   mwep_repo_dir,
                   project,
                   overwrite=False,
                   start_from_scratch=False,
                   verbose=0):
    """

    :param str json_dir: folder in which structured data will be (over)written
    :param str source_naf_dir: folder of NAF files to add
    :param str target_naf_dir: folder where all NAF files of data release are found
    (called unstructured)
    :param str path_inc_coll_obj: path to an instance of IncidentCollection
    (https://github.com/cltl/multilingual-wiki-event-pipeline/blob/master/classes.py)
    :param str mwep_repo_dir: path to folder
    where https://github.com/cltl/multilingual-wiki-event-pipeline is cloned
    :param str project: the project to which the IncidentCollection belongs,
    e.g., "HistoricalDistanceData"
    :param bool overwrite:
    :param bool start_from_scratch: if True, start with empty json files for structured data
    :return:
    """
    # TODO: structured data (validate in MWEP_on_one_incident)

    if verbose >=  3:
        print('############ BEFORE')

    dirs = [json_dir, target_naf_dir]
    for dir_path in dirs:
        if all([start_from_scratch,
                os.path.exists(dir_path)]):
            shutil.rmtree(dir_path)
            if verbose >= 1:
                print(f'removed {dir_path}, starting from scratch')

    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            if verbose >= 2:
                print(f'recreated {dir_path}')

    # load IncidentCollection
    sys.path.insert(0, mwep_repo_dir)
    with open(path_inc_coll_obj, 'rb') as infile:
        inc_coll_obj_to_add = pickle.load(infile)
    sys.path.remove(mwep_repo_dir)

    # load IncidentCollection of the data release
    sys.path.insert(0, mwep_repo_dir)
    release_inc_coll_obj_path = os.path.join(json_dir, 'data_release_inc_coll_obj.p')
    if os.path.exists(release_inc_coll_obj_path):
        release_inc_coll_obj = pickle.load(open(release_inc_coll_obj_path, 'rb'))
    else:
        from classes import IncidentCollection
        release_inc_coll_obj = IncidentCollection(incident_type=None,
                                                  incident_type_uri=None,
                                                  languages=[],
                                                  incidents=[])
    sys.path.remove(mwep_repo_dir)


    dictname_to_info = {
        'inc2doc' : {
            'path' : '%s/inc2doc_index.json' % json_dir,
            'key_label' : 'number of incidents',
            'value_label' : 'distribution of # of docs per incident',
            'metric' : 'length_distribution'
        },
        'inc2str' : {
            'path' : '%s/inc2str_index.json' % json_dir,
            'key_label' : 'number of incidents',
            'value_label' : 'number of incidents',
            'metric' : 'count'
        },
        'proj2inc' : {
            'path' : '%s/proj2inc_index.json' % json_dir,
            'key_label' : 'number of projects',
            'value_label' : 'distribution of # of incidents per project',
            'metric' : 'length_distribution'
        },
        'type2inc' : {
            'path' : '%s/type2inc_index.json' % json_dir,
            'key_label' : 'number of event types',
            'value_label' : 'number of incidents per event type',
            'metric' : 'length_distribution'
        }
    }

    inc2doc_stats = defaultdict(int)
    inc2str_stats = defaultdict(int)
    proj2inc_stats = defaultdict(int)
    type2inc_stats = defaultdict(int)

    for variable, info in dictname_to_info.items():
        path = info['path']

        if any([start_from_scratch,
                not os.path.exists(path)]):

            if variable in {'proj2inc', 'type2inc',
                            'inc2doc', 'inc2str'}:
                the_dict = defaultdict(list)
            else:
                raise Exception(f'Please inspect.')

        elif os.path.exists(path):
            the_dict = json.load(open(path))
        else:
            raise Exception(f'Please inspect.')

        globals()[variable] = the_dict
        if verbose >= 3:
            print_dict_stats(a_dict=the_dict,
                             dict_label=variable,
                             key_label=info['key_label'],
                             value_label=info['value_label'],
                             metric=info['metric'])

    for inc_obj in inc_coll_obj_to_add.incidents:
        str_data = {}
        for k, v in inc_obj.extra_info.items():
            str_data[k] = list(v)

        rts = []
        for rt in inc_obj.reference_texts:
            rt_info = '%s/%s' % (rt.language, rt.name)
            rts.append(rt_info)

        inc_id = inc_obj.wdt_id
        event_type = inc_obj.incident_type

        if rts:

            #update_inc2doc
            result = update_inc2doc(inc2doc,
                                    inc_id,
                                    rts,
                                    release_inc_coll_obj,
                                    inc_obj,
                                    source_naf_dir,
                                    target_naf_dir,
                                    overwrite)
            inc2doc_stats[result] += 1

            #update_inc2str
            result = update_inc2str(inc2str,
                                    inc_id,
                                    str_data,
                                    overwrite)
            inc2str_stats[result] += 1

            #update_proj2inc
            result = update_proj2inc(proj2inc, project, inc_id)
            proj2inc_stats[result] += 1

            #update_type2inc
            result = update_type2inc(type2inc, event_type, inc_id)
            type2inc_stats[result] += 1


    if verbose >=  2:
        print('############ AFTER')

    for variable, info in dictname_to_info.items():
        path = info['path']
        the_dict = globals()[variable]
        with open(path, 'w') as outfile:
            json.dump(the_dict,
                      outfile)
            if verbose >= 2:
                print(f'written {path} to disk.')
                print_dict_stats(a_dict=the_dict,
                                 dict_label=variable,
                                 key_label=info['key_label'],
                                 value_label=info['value_label'],
                                 metric=info['metric'])

    with open(release_inc_coll_obj_path, 'wb') as outfile:
        pickle.dump(release_inc_coll_obj, outfile)
        if verbose >= 2:
            print(f'pickled IncidentCollection of data release to {release_inc_coll_obj_path}')

    if verbose >= 1:
        print()
        print(f'inc2doc stats: {inc2doc_stats}')
        print(f'inc2str stats: {inc2str_stats}')
        print(f'proj2inc stats: {proj2inc_stats}')
        print(f'type2inc stats: {type2inc_stats}')


def update_inc2doc(inc2doc,
                   inc_id,
                   rts,
                   release_inc_coll_obj,
                   inc_obj,
                   source_naf_dir,
                   target_naf_dir,
                   overwrite):

    write_docs = False

    if inc_id in inc2doc:
        if overwrite:
            inc2doc[inc_id] = rts
            write_docs = True
            result = 'replaced docs for existing incident'

            # retrieve incident and add reference texts
            target_inc_obj = None
            for candidcate_inc_obj in release_inc_coll_obj.incidents:
                if candidcate_inc_obj.wdt_id == inc_obj.wdt_id:
                    target_inc_obj = candidcate_inc_obj

            len_before = len(release_inc_coll_obj.incidents)
            release_inc_coll_obj.incidents.remove(target_inc_obj)
            len_after = len(release_inc_coll_obj.incidents)
            assert len_before == len_after + 1

            # add entire incident to IncidentCollection of the data release
            release_inc_coll_obj.incidents.append(inc_obj)
            assert len_before == len(release_inc_coll_obj.incidents)

        else:
            result = 'incident existed and did not insert new documents'
    else:
        inc2doc[inc_id] = rts
        write_docs = True
        result = 'added new documents to not existing incident.'

        # add entire incident to IncidentCollection of the data release
        release_inc_coll_obj.incidents.append(inc_obj)


    if write_docs:
        for ref_text_obj in inc_obj.reference_texts:
            lang = ref_text_obj.language
            basename = ref_text_obj.name

            lang_dir = os.path.join(target_naf_dir, lang)
            if not os.path.exists(lang_dir):
                os.mkdir(lang_dir)

            source_path = os.path.join(source_naf_dir, lang, f'{basename}.naf')
            target_path = os.path.join(target_naf_dir, lang, f'{basename}.naf')
            shutil.copy(source_path, target_path)

    return result

def update_inc2str(inc2str, inc_id, str_data, overwrite):

    if inc_id in inc2str:

        if overwrite:
            inc2str[inc_id] = str_data
            result = 'inserted new structured data for existing incident'
        else:
            result = 'incident exsisted and no new structured data was added'

    else:
        inc2str[inc_id] = str_data
        result = 'added new structured data to not existing incident'

    return result


def update_proj2inc(proj2inc, project, inc_id):

    if project not in proj2inc:
        proj2inc[project] = []

    if inc_id not in proj2inc[project]:
        proj2inc[project].append(inc_id)
        result = 'added new incident to project'
    else:
        result = 'incident was already linked to project'

    return result


def update_type2inc(type2inc, event_type, inc_id):

    if event_type not in type2inc:
        type2inc[event_type] = []

    if inc_id not in type2inc[event_type]:
        type2inc[event_type].append(inc_id)
        result = 'added new incident to event type'
    else:
        result = 'incident was already linked to event type'

    return result