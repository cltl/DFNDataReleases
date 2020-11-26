import os
import json
import shutil

def get_relevant_info(repo_dir,
                      project,
                      start_from_scratch=False,
                      load_jsons=True,
                      verbose=0):
    """

    :param str repo_dir: the absolute path of the DFNDataReleases repository,
    advised to pass it as DFNDataReleases.dir_path

    :rtype: dict
    """

    paths = {
        'inc2lang2doc': os.path.join(repo_dir, 'structured', 'inc2lang2doc_index.json'),
        'inc2str': os.path.join(repo_dir, 'structured', 'inc2str_index.json'),
        'proj2inc': os.path.join(repo_dir, 'structured', 'proj2inc_index.json'),
        'type2inc': os.path.join(repo_dir, 'structured', 'type2inc_index.json'),
    }


    if load_jsons:
        for name, path in paths.items():
            paths[name] = json.load(open(path))

        inc2type = {}
        for type_, incs in paths['type2inc'].items():
            for inc in incs:
                assert inc not in inc2type, f'{inc} has been assigned to 2> event types. Please inspect.'
                inc2type[inc] = type_
        paths['inc2type'] = inc2type

    paths['inc_coll_obj'] = os.path.join(repo_dir, 'structured', 'data_release_inc_coll_obj.p')
    paths['unstructured'] = os.path.join(repo_dir, 'unstructured')
    paths['structured'] = os.path.join(repo_dir, 'structured')
    paths['main_statistics_folder'] = os.path.join(repo_dir, 'statistics')
    paths['project_statistics'] = os.path.join(paths['main_statistics_folder'], project)
    paths['path_inc2str'] = os.path.join(repo_dir, 'structured', 'inc2str_index.json')

    if not os.path.exists(paths['main_statistics_folder']):
        os.mkdir(paths['main_statistics_folder'])
        if verbose >= 1:
            print('created folder at {paths["main_statistics_folder"]}')

    project_dir = paths['project_statistics']
    if os.path.exists(project_dir):
        if start_from_scratch:
            shutil.rmtree(project_dir)
            if verbose >= 1:
                print(f'removed existing folder {project_dir}')

    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
        if verbose >= 1:
            print(f'created folder at {project_dir}')

    for name, path in paths.items():
        assert os.path.exists, f'{path} does not exist'

    return paths
