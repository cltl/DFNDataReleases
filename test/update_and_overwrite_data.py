import sys
import os

sys.path.insert(0, '../../')

dir_path = os.path.dirname(os.path.realpath(__file__))
json_dir = os.path.join(dir_path, 'structured')
target_naf_output = os.path.join(dir_path, 'unstructured')

path_inc_coll_obj = os.path.join(dir_path, 'example_mwep_output/Q17374096/bin/Q17374096.bin')
source_naf_dir = os.path.join(dir_path, 'example_mwep_output/Q17374096/wiki_output')

print()
print(sys.modules[__name__])

from DFNDataReleases import integrate_data
import DFNDataReleases

integrate_data(json_dir=json_dir,
               source_naf_dir=source_naf_dir,
               target_naf_dir=target_naf_output,
               path_inc_coll_obj=path_inc_coll_obj,
               mwep_repo_dir=DFNDataReleases.mwep_repo_dir,
               project='HistoricalDistanceData',
               start_from_scratch=False,
               overwrite=True,
               verbose=1)

