import json

import httpretty

from analyticsclient.exceptions import NotFoundError
from analyticsclient.tests import ClientTestCase


class UserTests(ClientTestCase):
    def setUp(self):
        super(UserTests, self).setUp()
        self.username = "TestUser"
        httpretty.enable()

    def tearDown(self):
        super(UserTests, self).tearDown()
        httpretty.disable()

    def test_not_found(self):
        """ User API calls should raise a NotFoundError when provided with an invalid user ID. """

        username = "B@dName!"
        uri = self.get_api_url('users/{0}/'.format(username))
        httpretty.register_uri(httpretty.GET, uri, status=404)

        user = self.client.users(username)
        with self.assertRaises(NotFoundError):
            user.profile()

    def test_profile(self):

        body = {
            "id": 123,
            "username": self.username,
            "last_login": "2015-05-28T00:08:45Z",
            "date_joined": "2015-05-28T00:08:43Z",
            "is_staff": False,
            "email": "test@example.com",
            "name": "Test User",
            "gender": "unknown",
            "year_of_birth": 1903,
            "level_of_education": "unknown"
        }

        uri = self.get_api_url('users/{0}/'.format(self.username))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.client.users(self.username).profile())


class UserWeeklyProblemDataTests(ClientTestCase):
    def setUp(self):
        super(UserWeeklyProblemDataTests, self).setUp()
        self.course_id = 'edX/DemoX/Demo_Course'
        self.course = self.client.courses(self.course_id)
        self.user_id = 10000
        httpretty.enable()

    def tearDown(self):
        super(UserWeeklyProblemDataTests, self).tearDown()
        httpretty.disable()

    def test_not_found(self):
        """ User API calls should raise a NotFoundError when provided with an invalid user ID. """

        user_id = 555
        uri = self.get_api_url('courses/{}/users/{}/problem_data/'.format(self.course_id, user_id))
        httpretty.register_uri(httpretty.GET, uri, status=404)

        problem_data_client = self.client.user_problem_weekly_data(self.course_id, user_id)
        with self.assertRaises(NotFoundError):
            problem_data_client.weekly_problem_data()

    def test_weekly_problem_data(self):
        body = [
            {
                "id": 1,
                "week_ending": "2015-08-20",
                "course_id": self.course_id,
                "user_id": self.user_id,
                "problem_id": "dummy_problem_1",
                "num_attempts": 11,
                "most_recent_score": 0,
                "max_score": 3,
            },
            {
                "id": 2,
                "week_ending": "2015-08-27",
                "course_id": self.course_id,
                "user_id": self.user_id,
                "problem_id": "dummy_problem_2",
                "num_attempts": 22,
                "most_recent_score": 1,
                "max_score": 3,
            },
        ]

        uri = self.get_api_url('courses/{}/users/{}/problem_data/'.format(self.course_id, self.user_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(
            body, self.client.user_problem_weekly_data(self.course_id, self.user_id).weekly_problem_data()
        )
