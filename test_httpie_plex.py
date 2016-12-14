# -*- coding: utf-8 -*-
"""Unit tests for httpie_plex"""

import os
import shutil
from time import time
from unittest import TestCase
from httpie.config import DEFAULT_CONFIG_DIR
from httpie.plugins import AuthPlugin
from httpie_plex import (PlexAuth, PlexAuthPlugin, PlexToken, add_to_query,
                         __version__, __author__, __license__)
from oauthlib.oauth2 import BackendApplicationClient


class MetaInfoTestCase(TestCase):

    def test_meta_info(self):
        self.assertIsNotNone(__version__)
        self.assertEqual(__author__, 'pswaminathan')
        self.assertEqual(__license__, 'Apache Software License v2.0')


class AddToQueryTestCase(TestCase):

    def test_no_query_string(self):
        u, q = 'http://ex.com/path', {'hi': 'there'}
        url = add_to_query(u, q)
        self.assertEqual(url, 'http://ex.com/path?hi=there')

    def test_with_query_string(self):
        u, q = 'http://ex.com/path?a=b', {'hi': 'there'}
        url = add_to_query(u, q)
        self.assertEqual(url, 'http://ex.com/path?a=b&hi=there')


class PlexTokenTestCase(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(DEFAULT_CONFIG_DIR, 'plextokentest'))

    def test_paths(self):
        token = PlexToken('plextokentest')
        dir_ = os.path.join(DEFAULT_CONFIG_DIR, 'plextokentest')
        path = os.path.join(DEFAULT_CONFIG_DIR, 'plextokentest', 'token.json')

        self.assertEqual(token.name, 'plextokentest')
        self.assertEqual(token.directory, dir_)
        self.assertEqual(token._get_path(), path)

        token = PlexToken()
        dir_ = os.path.join(DEFAULT_CONFIG_DIR, 'plex')
        path = os.path.join(DEFAULT_CONFIG_DIR, 'plex', 'token.json')

        self.assertEqual(token.name, 'plex')
        self.assertEqual(token.directory, dir_)
        self.assertEqual(token._get_path(), path)

    def test_load_update_save(self):
        token = PlexToken('plextokentest')
        upd = {'access_token': 'TOKEN'}
        token.load()
        token.update_token(upd)
        # token.load() is called here because the save method adds in a
        # __meta__ object, but load pops that out
        token.load()

        self.assertDictEqual(upd, token)

    def test_time_expired(self):
        token = PlexToken('plextokentest')
        token.load()
        self.assertTrue(token.is_expired())
        token['expires_at'] = time() + 1000
        self.assertFalse(token.is_expired())


class PlexAuthTestCase(TestCase):

    def test_init(self):
        from httpie_plex import PlexAuth
        client = BackendApplicationClient('clientid')
        token = {'access_token': 'TOKEN'}
        plex = PlexAuth('clientid', client, token)

        self.assertEqual(plex.client_id, 'clientid')
        self.assertEqual(plex._client, client)
        self.assertEqual(plex._client.access_token, token['access_token'])

    def test_call(self):

        class RequestMock(object):
            def __init__(self, headers):
                self.headers = headers
                self.url = 'https://api.mediamath.com/base'
                self.method = 'GET'
                self.body = None

        request = RequestMock({})
        plex = PlexAuth('clientid',
                        BackendApplicationClient('clientid'),
                        {'access_token': 'TOKEN', 'token_type': 'Bearer'})
        updated = plex(request)

        self.assertIsNotNone(updated.headers['Authorization'])
        self.assertEqual(updated.headers['Authorization'], 'Bearer TOKEN')
        self.assertEqual(updated.url,
                         'https://api.mediamath.com/base?api_key=clientid')


class PlexAuthPluginTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        PlexToken.name = 'plexauthtest'
        t = PlexToken()
        t.load()
        t.update_token({'access_token': 'TOKEN', 'expires_at': time()+1000})

    @classmethod
    def tearDownClass(cls):
        PlexToken.name = 'plex'
        shutil.rmtree(os.path.join(DEFAULT_CONFIG_DIR, 'plexauthtest'))

    def test_instance_type(self):
        plex_plugin = PlexAuthPlugin()
        self.assertIsInstance(plex_plugin, AuthPlugin)

    def test_attribute(self):
        desc = 'OAuth2 client credentials grant for Bid Opp Firehose'
        self.assertEqual(PlexAuthPlugin.name, 'Plex v1.0 auth')
        self.assertEqual(PlexAuthPlugin.auth_type, 'plex')
        self.assertEqual(PlexAuthPlugin.description, desc)

    def test_get_auth(self):
        plex_plugin = PlexAuthPlugin()
        plex = plex_plugin.get_auth('clientid', 'clientsecret')
        self.assertEqual(plex.client_id, 'clientid')
