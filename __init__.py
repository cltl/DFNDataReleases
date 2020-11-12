import os

from .lib import integrate_data
from .lib import get_stats

dir_path = os.path.dirname(os.path.realpath(__file__))
mwep_repo_dir = os.path.join(dir_path, 'lib/res/multilingual-wiki-event-pipeline')
assert os.path.exists(mwep_repo_dir), f'{mwep_repo_dir} does not exist. Please inspect.'