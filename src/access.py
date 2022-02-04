from datetime import datetime, date, time
from enum import Enum
from typing import Dict, List, Any, Iterable
import boto3
from boto3.dynamodb.conditions import Key
from src.models import Notification

resource = boto3.resource("dynamodb")


class UserNotificationsRepository:
    @classmethod
    def build(cls, environment: str):

        table_name = f"{environment}-UserNotifications"
        return cls(resource.Table(table_name))

    def __init__(self, table):
        self._table = table
        self._partition_key = "user_id"

    def load_user_notifications(self, user_id: str) -> List[Notification]:
        response = self._table.query(KeyConditionExpression=Key(self._partition_key).eq(user_id))

        notifications = [
            Notification(id=db_item.pop("notification_id"), **db_item)
            for db_item in response.get("Items", [])
        ]
        return notifications

    def save_notifications(self, user_id: str, notifications: Iterable[Notification]):
        with self._table.batch_writer() as batch:
            for item in notifications:
                item_dict = _clean_dict(item.dict())
                item_dict["notification_id"] = item_dict.pop("id")
                put_item: Dict[str, Any] = {self._partition_key: user_id, **item_dict}
                batch.put_item(Item=put_item)


def _clean_dict(item_dict: Dict) -> Dict:
    dicts = [item_dict]

    while len(dicts) > 0:
        current_dict = dicts.pop()
        for k, v in current_dict.items():
            if isinstance(v, Dict):
                dicts.append(v)
            elif isinstance(v, List):
                if len(v) > 0:
                    first = v[0]
                    if isinstance(first, Dict):
                        for obj in v:
                            dicts.append(obj)
                    else:
                        current_dict[k] = [_clean_value(el) for el in v]
            else:
                current_dict[k] = _clean_value(v)
    return item_dict


def _clean_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return int(value.timestamp())
    elif isinstance(value, (date, time)):
        return str(value.isoformat())
    elif isinstance(value, Enum):
        return value.value
    else:
        return value
