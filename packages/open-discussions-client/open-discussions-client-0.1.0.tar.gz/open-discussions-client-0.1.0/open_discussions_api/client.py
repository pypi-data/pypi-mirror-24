"""open-discussions api client"""
import time

import jwt
import requests

from .users.client import UsersApi

EXPIRATION_DELTA_SECONDS = 60 * 60


class OpenDiscussionsApi(object):
    """
    A client for speaking with open-discussions

    Args:
        secret (str): the JWT secret
        base_url (str): the base API url
        username (str): the username to use for the token
        roles (list(str)): the list of roles the user headers
        version (str): the version of the API to use
    """

    def __init__(self, secret, base_url, username, roles=None, version="v0"):  # pylint: disable=too-many-arguments
        if not secret:
            raise AttributeError("secret is required")
        if not base_url:
            raise AttributeError("base_url is required")

        self.base_url = base_url
        self.secret = secret
        self.version = version
        self.username = username
        self.roles = roles or []

    def get_token(self):
        """
        Gets a JWt token

        Returns:
            str: encoded JWT token
        """
        now = int(time.time())
        return jwt.encode({
            'username': self.username,
            'roles': self.roles,
            'exp': now + EXPIRATION_DELTA_SECONDS,
            'orig_iat': now,
        }, self.secret, algorithm='HS256').decode('utf-8')

    def _get_session(self):
        """
        Gets an initial session

        Returns:
            requests.Session: default session
        """
        # NOTE: this method is a hook to allow substitution of the base session via mocking
        return requests.session()

    def _get_authenticated_session(self):
        """
        Returns an object to make authenticated requests. See python `requests` for the API.

        Returns:
            requests.Session: authenticated session
        """
        session = self._get_session()
        session.headers.update({
            'Authorization': 'Bearer {}'.format(self.get_token()),
            'Content-Type': 'application/json',
        })
        return session

    @property
    def users(self):
        """
        Users API

        Returns:
            open_discussions_api.users.client.UsersApi: configured users api
        """
        return UsersApi(self._get_authenticated_session(), self.base_url, self.version)
