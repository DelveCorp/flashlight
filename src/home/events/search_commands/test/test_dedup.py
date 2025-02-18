"""This test module is meant to test the dedup search
command, located at events.search_commands.dedup.
"""
import json
from unittest.mock import MagicMock

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    APIClient,
    force_authenticate,
)

from events.models import (
    Event,
    Query,
)


# from apps.core import models, admin
# from apps.rest import views

TEST_USER = "testuser"
TEST_USER_PASS = "testuser"
TEST_ADMIN = "testadmin"
TEST_ADMIN_PASS = "testadmin"

class DedupTests(APITestCase):
    def setUp(self, *args, **kwargs):
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
        # self.user.is_superuser = True
        # self.user.is_staff = True
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

    def test_dedup_everything_else_worked(self):
        """Basic sanity checks, if this does not work, it is not dedup,
        but rather something with event.models.Query or event.models.Query.resolve
        or we were unable to create test events
        """
        query = Query(
            name="test",
            text="search index=test",
            user=self.user,
        )
        results = query.resolve(request=MagicMock(user=self.user))
        self.assertEqual(len(results), 10)

    def test_dedup_deduplicates_events(self):
        """All events have the same index, so if we dedup
        based on index, the results should contain one event,
        the first event. 
        """
        query = Query(
            name="test",
            text="search index=test | dedup index",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        self.assertEqual(len(results), 1)
        
        # Here, the foo key was incremented 0..9, so when deduping
        # identical events, the first value for foo (or 0) should be the one
        # that was kept
        self.assertEqual(results[0]["extracted_fields"]["foo"], 0)

