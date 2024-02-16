import datetime


def delete_first_zero(text):
    return text[1:] if text.startswith('0') else text


def text_to_time(text):
    timestamps = text.split(':')
    return [int(delete_first_zero(piece)) for piece in timestamps]


def to_datetime_time(time):
    return datetime.time(time[0], time[1])


def yaml_to_datetime_time(time_list):
    return [to_datetime_time(text_to_time(time)) for time in time_list]
