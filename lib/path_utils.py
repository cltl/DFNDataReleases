import os
import json
import shutil

def get_relevant_info(repo_dir, project, verbose=0):
    """

    :param str repo_dir: the absolute path of the DFNDataReleases repository,
    advised to pass it as DFNDataReleases.dir_path

    :rtype: dict
    """

    paths = {
        'inc2doc': os.path.join(repo_dir, 'structured', 'inc2doc_index.json'),
        'inc2str': os.path.join(repo_dir, 'structured', 'inc2str_index.json'),
        'proj2inc': os.path.join(repo_dir, 'structured', 'proj2inc_index.json'),
        'type2inc': os.path.join(repo_dir, 'structured', 'type2inc_index.json'),
    }

    for name, path in paths.items():
        paths[name] = json.load(open(path))

    paths['inc_coll_obj'] = os.path.join(repo_dir, 'structured', 'data_release_inc_coll_obj.p')
    paths['unstructured'] = os.path.join(repo_dir, 'unstructured')
    paths['main_statistics_folder'] = os.path.join(repo_dir, 'statistics')
    paths['project_statistics'] = os.path.join(paths['main_statistics_folder'], project)

    if not os.path.exists(paths['main_statistics_folder']):
        os.mkdir(paths['main_statistics_folder'])
        if verbose >= 1:
            print('created folder at {paths["main_statistics_folder"]}')

    project_dir = paths['project_statistics']
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
        if verbose >= 1:
            print(f'removed existing folder {project_dir}')
    os.mkdir(project_dir)
    if verbose >= 1:
        print(f'created folder at {project_dir}')

    for name, path in paths.items():
        assert os.path.exists, f'{path} does not exist'

    return paths
