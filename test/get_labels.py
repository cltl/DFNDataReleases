import sys
sys.path.insert(0, '../../')

from DFNDataReleases import get_labels


result = get_labels(set_of_q_ids={"Q62090804", "Q699872", "GVA-1"},
                    verbose=5)
