import datetime


def yaml_to_datetime_time(times_str: list) -> list:
    return [
        datetime.time(
            *map(
                int,
                time_str.split(':')
            )
        )
        for time_str
        in times_str
    ]
