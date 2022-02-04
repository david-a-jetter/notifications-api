import os

from src.access import UserNotificationsRepository
from test.factories import NotificationFactory
import boto3

session = boto3.Session(
    aws_access_key_id=os.environ["PERSONAL_AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["PERSONAL_AWS_SECRET_KEY"],
)


def test_add_notifications():
    user_id = "c5f145bc-7705-4204-a0b5-c4dc68266e6e"
    table = session.resource("dynamodb").Table("notification-api-dev-UserNotifications")
    repo = UserNotificationsRepository(table)
    notifications = NotificationFactory.build_batch(3)
    repo.save_notifications(user_id, notifications)
