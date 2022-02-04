import random

import factory

from src.models import Foundation, Notification


def random_currency() -> str:
    return random.choice(["USD", "GBP", "EUR", "CAD"])


class FoundationFactory(factory.Factory):
    class Meta:
        model = Foundation

    id = factory.Faker("bothify")
    name = factory.Faker("bs")
    industries = factory.List([factory.Faker("bs") for _ in range(2)])


class NotificationFactory(factory.Factory):
    class Meta:
        model = Notification

    id = factory.Faker("bothify")
    timestamp = factory.Faker("date_time")
    funder = factory.SubFactory(FoundationFactory)
    max_opportunity = factory.Faker("pyint", min_value=0)
    currency = factory.LazyFunction(random_currency)
