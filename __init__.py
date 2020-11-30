import os

from .src import integrate_data
from .src import integrate_data_collection
from .src import get_stats
from .src import convert_to_sem
from .src import edit_structured_data
from .src import add_lexical_data

dir_path = os.path.dirname(os.path.realpath(__file__))
mwep_repo_dir = os.path.join(dir_path, 'res/multilingual-wiki-event-pipeline')
assert os.path.exists(mwep_repo_dir), f'{mwep_repo_dir} does not exist. Please inspect.'