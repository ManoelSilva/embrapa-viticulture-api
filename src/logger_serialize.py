import json
from datetime import datetime, timedelta, timezone


def serialize(message):
    record = message.record
    time = record['time'].timestamp()
    subset = {
        'timestamp': datetime.fromtimestamp(time, timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M:%S.%f'),
        'level': record['level'].name,
        'message': record['message']
    }
    print(json.dumps(subset))
