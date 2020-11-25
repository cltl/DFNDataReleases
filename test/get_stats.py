import sys
import os

sys.path.insert(0, '../../')

import DFNDataReleases

test_repo_dir = os.getcwd()

DFNDataReleases.get_stats(repo_dir=test_repo_dir,
                          project='HistoricalDistanceData',
                          verbose=2)

