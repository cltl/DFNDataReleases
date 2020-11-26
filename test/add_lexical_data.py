import sys
import os
from datetime import datetime

sys.path.insert(0, '../../')

import DFNDataReleases


print(datetime.now())


repo_dir = os.path.join(DFNDataReleases.dir_path, 'test')


DFNDataReleases.add_lexical_data(repo_dir=repo_dir,
                                 dfn_major_version=0,
                                 dfn_minor_version=1,
                                 project='HistoricalDistanceData',
                                 verbose=2)


print(datetime.now())