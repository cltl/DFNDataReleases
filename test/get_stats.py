import sys

sys.path.insert(0, '../../')

import DFNDataReleases

DFNDataReleases.get_stats(repo_dir=DFNDataReleases.dir_path,
                          project='HistoricalDistanceData',
                          verbose=2)

