"""This test module is meant to test the filter search
command, located at events.search_commands.filter.
"""
import json
from unittest.mock import MagicMock
from typing import Any

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    APIClient,
)

from events.models import (
    Event,
    Query,
)

TEST_USER = "testuser"
TEST_USER_PASS = "testuser"
TEST_ADMIN = "testadmin"
TEST_ADMIN_PASS = "testadmin"

class FilterTests(APITestCase):
    def setUp(self, *args: Any, **kwargs: Any) -> None:
        """For preparation, we are going to setup a user and
        an APIClient and add ten Events.
        """
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser',
        )
        self.user.save()
        self.events = []
        for i in range(10):
            event = Event.objects.create(
                index="test",
                host="127.0.0.1",
                source="test",
                sourcetype="json",
                user=self.user,
                text=json.dumps(
                    {
                        "foo": i,
                    }
                )
            )
            event.extract_fields()
            event.process()
            event.save()
            self.events.append(event)
        super().setUp(*args, **kwargs)

    def test_filter_everything_else_worked(self) -> None:
        """Basic sanity checks, if this does not work, it is not filter,
        but rather something with event.models.Query or event.models.Query.resolve
        or we were unable to create test events.
        """
        query = Query(
            name="test",
            text="search index=test",
            user=self.user,
        )
        results = query.resolve(request=MagicMock(user=self.user))
        self.assertEqual(len(results), 10)

    def test_filter_filters_events(self) -> None:
        """Test that filter correctly filters events based on the specified criteria."""
        query = Query(
            name="test",
            text="search index=test | filter extracted_fields__foo__gte=5",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        self.assertEqual(len(results), 5)
