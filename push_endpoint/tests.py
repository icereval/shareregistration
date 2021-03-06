import copy
import json

from django.test import TestCase
from push_endpoint.views import DataList
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser, User


VALID_POST = {
    "description": "Ducks, their calls, and their habbits.",
    "contributors": "Shawn Michaels",
    "tags": "ducks, hunting",
    "title": "All About Ducks",
    "url": "http://dudley.net",
    "serviceID": "DuckID11",
    "doi": "sdf"
}


class APIPostTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='bubbaray', password='dudley')

    def test_valid_submission(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_missing_doi(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('doi')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['doi'], ['This field is required.'])

    def test_invalid_doi(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post['doi'] = 'thisistotallynotadoi'
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(
            data['non_field_errors'],
            ['DOI does not resolve, please enter a valid DOI']
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_url(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('url')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['url'], ['This field is required.'])
        self.assertEqual(response.status_code, 400)

    def test_invalid_url(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post['url'] = 'thisistotallynotaurl'
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['url'], ['Enter a valid URL.'])
        self.assertEqual(response.status_code, 400)

    def test_missing_title_fails(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('title')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['title'], ['This field is required.'])
        self.assertEqual(response.status_code, 400)

    def test_missing_service_id_fails(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('serviceID')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['serviceID'], ['This field is required.'])
        self.assertEqual(response.status_code, 400)

    def test_missing_contributors_fails(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('contributors')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['contributors'], ['This field is required.'])
        self.assertEqual(response.status_code, 400)

    def test_missing_tags_is_ok(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('tags')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_missing_description_is_ok(self):
        view = DataList.as_view()
        invalid_post = copy.copy(VALID_POST)
        invalid_post.pop('description')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_anonomous_user_can_view(self):
        view = DataList.as_view()
        request = self.factory.get('/pushed_data/')
        request.user = AnonymousUser()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_anonomous_user_can_not_post(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = AnonymousUser()
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_source_is_same_as_user(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['source'], request.user.username)
