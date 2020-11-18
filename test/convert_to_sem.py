import sys

sys.path.insert(0, '../../')

import DFNDataReleases

DFNDataReleases.convert_to_sem(repo_dir=DFNDataReleases.dir_path,
                               project='HistoricalDistanceData',
                               verbose=2)

