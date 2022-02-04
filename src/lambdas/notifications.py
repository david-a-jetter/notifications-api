from http import HTTPStatus
from typing import Dict

from src.managers import UserNotificationsManager


def get_user_notifications(event: Dict, context) -> Dict:
    user_id = event["pathParameters"]["user_id"]
    manager = UserNotificationsManager.build("notification-api-dev")
    notifications = manager.get_user_notifications(user_id)
    response = {
        "statusCode": HTTPStatus.OK.value,
        "body": notifications.json()
    }

    return response
