import sys
import os
sys.path.insert(0, '../../')

from DFNDataReleases import intergrate_data_collection
import DFNDataReleases

dir_path = os.path.dirname(os.path.realpath(__file__))

print()
print(sys.modules[__name__])

intergrate_data_collection(data_collection_dir='example_mwep_output',
                           repo_dir=dir_path,
                           mwep_repo_dir=DFNDataReleases.mwep_repo_dir,
                           project='HistoricalDistanceData',
                           overwrite=True,
                           start_from_scratch=True,
                           verbose=3)





