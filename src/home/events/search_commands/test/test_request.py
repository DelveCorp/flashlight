"""This test module is meant to test the request search
command, located at events.search_commands.request.
"""
import json
from unittest.mock import MagicMock, patch
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

class RequestTests(APITestCase):
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

    @patch('requests.request')
    def test_request(self, mock_request) -> None:
        """Test the request command to ensure it correctly issues
        an HTTP request and processes the response.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        query = Query(
            name="test",
            text="request GET --extract-fields http://example.com",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['extracted_fields']['status_code'], 200)
        self.assertEqual(results[0]['extracted_fields']['key'], "value")
