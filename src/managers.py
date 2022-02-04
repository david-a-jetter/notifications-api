from src.access import UserNotificationsRepository
from src.models import NotificationResponse


class UserNotificationsManager:
    @classmethod
    def build(cls, environment: str):
        return cls(UserNotificationsRepository.build(environment))

    def __init__(self, notifications_repo: UserNotificationsRepository):
        self._notifications_repo = notifications_repo

    def get_user_notifications(self, user_id: str) -> NotificationResponse:
        notifications = self._notifications_repo.load_user_notifications(user_id)
        return NotificationResponse(notifications=notifications)
