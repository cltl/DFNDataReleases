import json
from datetime import datetime

from .path_utils import get_relevant_info
from .time_utils import time_in_correct_format

def edit_structured_data(repo_dir,
                         project,
                         inc_id,
                         sem_rel,
                         label,
                         identifier,
                         action,
                         verbose=0):
    """
    add to structured data
    (structured/inc2str_index.json)

    :param str repo_dir: use DFNDataReleases.dir_path
    :param str project: name of project for which you want to add structured data
    :param str inc_id: e.g., Q17374096
    :param str sem_rel: "sem:hasActor" | "sem:hasPlace" | "sem:hasTimeStamp"
    :param str label: the label of the value of the SEM relationship
    :param str identifier: the identifier of the value of the SEM relationship
    :param str action: add | remove
    :param int verbose: debugging information
    """
    sem_rels = ["sem:hasActor", "sem:hasPlace", "sem:hasTimeStamp"]
    assert sem_rel in sem_rels, f'{sem_rel} not part of accepted set: {sem_rels}'
    actions = ['add', 'remove']
    assert action in actions, f'{action} not part of accepted actions: {actions}'

    if sem_rel in {'sem:hasPlace', 'sem:hasActor'}:
        error_message = f'identifiers of locations and actors have to start with: http://www.wikidata.org/entity/'
        assert identifier.startswith('http://www.wikidata.org/entity/'), error_message

    if sem_rel == 'sem:hasTimeStamp':
        assert type(identifier) == datetime, f'please provide a datetime object as identifier for sem:hasTimeStamp'
        assert type(label) == datetime, f'please provide a datetime object as identifier for sem:hasTimeStamp'
        assert identifier == label, f'for sem:hasTimeStamp, identifier and label should be the same.'

        identifier = time_in_correct_format(datetime_obj=identifier)
        label = time_in_correct_format(datetime_obj=label)

    relevant_info = get_relevant_info(repo_dir=repo_dir,
                                      project=project,
                                      start_from_scratch=False,
                                      verbose=verbose)


    inc2str = relevant_info['inc2str']

    assert inc_id in inc2str, f'Incident ({inc_id}) not part of project: {project}'
    str_of_inc = inc2str[inc_id]

    current_values = str_of_inc.get(sem_rel, [])
    identifier_to_value = {}

    for value in current_values:
        existing_identifier, existing_value = value.split(' | ')
        identifier_to_value[existing_identifier] = existing_value

    # perform action
    if action == 'remove':
        if identifier not in identifier_to_value:
            raise Warning(f'for {sem_rel} of incident {inc_id}, identifier {identifier} is NOT part of the structured data.')
        else:
            del identifier_to_value[identifier]
            if verbose >= 2:
                print(f'removed: {identifier}: {label}')

    elif action == 'add':
        if identifier in identifier_to_value:
            raise Warning(f'for {sem_rel} of incident {inc_id}, identifier {identifier} is already part of the structured data.')

        if all([sem_rel in {'sem:hasPlace', 'sem:hasTimeStamp'},
                len(identifier_to_value) == 1]):
            raise Exception(
                f'{sem_rel} already has a value {current_values}. Please first remove that one before adding new one.')
        else:
            identifier_to_value[identifier] = label
            if verbose >= 2:
                print(f'added: {identifier}: {label}')

    # convert to the format
    new_values = [f'{new_identifier} | {new_value}'
                  for new_identifier, new_value in identifier_to_value.items()]

    str_of_inc[sem_rel] = new_values
    inc2str[inc_id] = str_of_inc


    # write to disk
    output_path = relevant_info['path_inc2str']
    with open(output_path, 'w') as outfile:
        json.dump(inc2str, outfile)















