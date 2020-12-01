import sys
import os
import pytest
from datetime import datetime

sys.path.insert(0, '../../')

import DFNDataReleases

test_repo_dir = os.getcwd()


def test_assert_identifier_location():
    with pytest.raises(AssertionError):
        DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                             project='HistoricalDistanceData',
                                             inc_id='Q17374096',
                                             sem_rel='sem:hasPlace',
                                             identifier='http://www.wikidata.org/wiki/Q212',
                                             label='Ukraine',
                                             action='add',
                                             verbose=2)

def test_add_location():
    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q17374096',
                                         sem_rel='sem:hasPlace',
                                         identifier='http://www.wikidata.org/entity/Q212',
                                         label='Ukraine',
                                         action='add',
                                         verbose=2)


def test_assert_add_location():
    with pytest.raises(Warning):
        DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                             project='HistoricalDistanceData',
                                             inc_id='Q17374096',
                                             sem_rel='sem:hasPlace',
                                             identifier='http://www.wikidata.org/entity/Q212',
                                             label='Ukraine',
                                             action='add',
                                             verbose=2)


def test_remove_location():
    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q17374096',
                                         sem_rel='sem:hasPlace',
                                         identifier='http://www.wikidata.org/entity/Q212',
                                         label='Ukraine',
                                         action='remove',
                                         verbose=2)


def test_warning_remove_location():
    with pytest.raises(Warning):
        DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                             project='HistoricalDistanceData',
                                             inc_id='Q17374096',
                                             sem_rel='sem:hasPlace',
                                             identifier='http://www.wikidata.org/entity/Q1234',
                                             label='dummy_label',
                                             action='remove',
                                             verbose=2)

def test_re_add_location():
    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q17374096',
                                         sem_rel='sem:hasPlace',
                                         identifier='http://www.wikidata.org/entity/Q212',
                                         label='Ukraine',
                                         action='add',
                                         verbose=2)

def test_add_timestamp():
    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q17374096',
                                         sem_rel='sem:hasTimeStamp',
                                         identifier=datetime(2014,7,17),
                                         label=datetime(2014,7,17),
                                         action='add',
                                         verbose=2)

    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q2399631',
                                         sem_rel='sem:hasTimeStamp',
                                         identifier=datetime(2012,9,21),
                                         label=datetime(2012,9,21),
                                         action='add',
                                         verbose=2)

    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q62090804',
                                         sem_rel='sem:hasTimeStamp',
                                         identifier=datetime(2019,3,18),
                                         label=datetime(2019,3,18),
                                         action='add',
                                         verbose=2)




def test_assert_timestamp():
    with pytest.raises(AssertionError):
        DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                             project='HistoricalDistanceData',
                                             inc_id='Q17374096',
                                             sem_rel='sem:hasTimeStamp',
                                             identifier=datetime(2014,7,17),
                                             label=datetime(2014,7,18),
                                             action='add',
                                             verbose=2)



def test_add_actor():
    DFNDataReleases.edit_structured_data(repo_dir=test_repo_dir,
                                         project='HistoricalDistanceData',
                                         inc_id='Q17374096',
                                         sem_rel='sem:hasActor',
                                         identifier='http://www.wikidata.org/entity/Q308952',
                                         label='Malaysia Airlines',
                                         action='add',
                                         verbose=2)

