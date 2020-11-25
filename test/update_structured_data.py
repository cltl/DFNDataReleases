import sys
import os
import pytest

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