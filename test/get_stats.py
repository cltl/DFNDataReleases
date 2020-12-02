import sys
import os

sys.path.insert(0, '../../')

import DFNDataReleases

test_repo_dir = os.getcwd()

time_buckets = {'day_0':range(0,1),
                'day_1':range(1,2),
                'day_2_to_30':range(2,31),
                'day_31_beyond' :range(31,100000)}

DFNDataReleases.get_stats(repo_dir=test_repo_dir,
                          project='HistoricalDistanceData',
                          time_buckets=time_buckets,
                          verbose=2)

