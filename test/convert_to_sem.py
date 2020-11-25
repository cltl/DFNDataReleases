import sys
import os
sys.path.insert(0, '../../')

import DFNDataReleases


test_repo_dir = os.getcwd()


DFNDataReleases.convert_to_sem(repo_dir=test_repo_dir,
                               project='HistoricalDistanceData',
                               verbose=2)

