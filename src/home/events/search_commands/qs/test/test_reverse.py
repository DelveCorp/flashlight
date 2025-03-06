"""This test module is meant to test the reverse command,
located at events.search_commands.qs.reverse.
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
)

from events.models import (
    Event,
    Query,
)


TEST_USER = "testuser"
TEST_USER_PASS = "testuser"
TEST_ADMIN = "testadmin"
TEST_ADMIN_PASS = "testadmin"

class ReverseTests(APITestCase):
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
                        "bar": i % 2,
                    }
                )
            )
            event.extract_fields()
            event.process()
            event.save()
            self.events.append(event)
        super().setUp(*args, **kwargs)

    def test_reverse(self):
        """Test the reverse command to ensure it correctly reverses
        the order of the records in the QuerySet.
        """
        query = Query(
            name="test",
            text="""search index=test | qs_order_by created | qs_reverse""",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        # print(results)
        self.assertEqual(len(results), 10)
        self.assertEqual(results[0]['extracted_fields']['foo'], 9)
        self.assertEqual(results[1]['extracted_fields']['foo'], 8)
        self.assertEqual(results[2]['extracted_fields']['foo'], 7)
