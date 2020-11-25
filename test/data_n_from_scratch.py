import sys
import os
sys.path.insert(0, '../../')

from DFNDataReleases import integrate_data
import DFNDataReleases

package_dir = DFNDataReleases.dir_path
dir_path = os.path.dirname(os.path.realpath(__file__))
json_dir = os.path.join(dir_path, 'structured')
target_naf_output = os.path.join(dir_path, 'unstructured')


print()
print(sys.modules[__name__])

incidents = ['Q2399631',
             'Q17374096',
             'Q62090804']

start_from_scratch = True

for incident in incidents:

    print()
    print(incident)
    path_inc_coll_obj = os.path.join(dir_path,
                                     f'example_mwep_output/{incident}/bin/{incident}.bin')
    source_naf_dir = os.path.join(dir_path,
                                  f'example_mwep_output/{incident}/wiki_output')

    integrate_data(json_dir=json_dir,
                   source_naf_dir=source_naf_dir,
                   target_naf_dir=target_naf_output,
                   path_inc_coll_obj=path_inc_coll_obj,
                   mwep_repo_dir=DFNDataReleases.mwep_repo_dir,
                   project='HistoricalDistanceData',
                   start_from_scratch=start_from_scratch,
                   overwrite=False,
                   verbose=3)

    start_from_scratch = False



