from collections import Counter



def print_dict_stats(a_dict,
                     dict_label='dict',
                     key_label='keys',
                     value_label='values',
                     metric='count'):
    """
    print the number of keys and values in a dict
    you can indicate what the keys and values mean using the keyword parameters

    :param dict a_dict: a dict
    :param str key_label: optionally, a label to clarify what the keys are
    :param str value_label: optionally, a label to clarify what the keys are
    :param str metric: count | length_distribution
    """
    print()
    print(f'information about dictionary: {dict_label}')
    print(f'found {len(a_dict.keys())} {key_label}')

    if metric == 'count':
        print(f'found {len(a_dict.values())} {value_label}')
    elif metric == 'length_distribution':
        distribution = Counter([len(value)
                                for value in a_dict.values()])
        print(f'{value_label}: {distribution}')



