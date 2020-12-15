from datetime import datetime



def time_in_correct_format(datetime_obj):
    "Function that returns the current time (UTC)"
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


def convert_time_values_to_utc(time_values):
    new_time_values = []

    for identifier_label in time_values:
        identifier, label = identifier_label.split(" | ")
        if identifier.endswith('Z'):
            timestamp_utc = convert_z_to_utc(timestamp_z=identifier)
        else:
            timestamp_utc = identifier

        new_time_values.append(f'{timestamp_utc} | {timestamp_utc}')

    return new_time_values

def convert_z_to_utc(timestamp_z):
    """

    :param timestamp_z: "%Y-%m-%dT%H:%M:%SZ" like timestamp, e.g.,
    "2019-03-18T00:00:00Z"
    :return:
    """
    datetime_obj = datetime.strptime(timestamp_z,
                                     "%Y-%m-%dT%H:%M:%SZ")

    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


