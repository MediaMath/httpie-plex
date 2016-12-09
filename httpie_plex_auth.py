"""Auth plugin for HTTPie for MediaMath's Bid Opportunity Firehose"""

# Copyright 2016 MediaMath

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO remove logging
import logging
from os.path import join
from time import time
try:
	import urlparse
	from urllib import urlencode
except ImportError:
	import urllib.parse as urlparse
	from urllib.parse import urlencode
from httpie.config import DEFAULT_CONFIG_DIR, BaseConfigDict
from httpie.plugins import AuthPlugin
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2, OAuth2Session

# TODO remove logging
logging.basicConfig(level=logging.DEBUG)

__version__ = '0.1.0'
__author__ = 'Prasanna Swaminathan'
__license__ = 'Apache Software License v2.0'

TOKEN_URL = 'https://api.mediamath.com/oauth2/v1.0/token'

def get_new_token(client_id, client_secret, token_url, token):
	c = BackendApplicationClient(client_id)
	ses = OAuth2Session(client=c, token_updater=token.update_token)
	return ses.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret, jwt='jws')

class PlexToken(BaseConfigDict):
	name = 'plex'
	helpurl = 'https://github.com/pswaminathan/httpie-plex-auth#token'
	about = 'Plex access token cache'

	def __init__(self):
		super(PlexToken, self).__init__()
		self.directory = join(DEFAULT_CONFIG_DIR, 'plex')
	def _get_path(self):
		return join(self.directory, 'token.json')
	def load(self):
		super(PlexToken, self).load()
		self.pop('key', None)
	def update_token(self, token):
		# TODO remove logging
		logging.debug('updating token')
		self.update(token)
		self.save()
	def is_expired(self):
		if time() > self.get('expires_at', 0):
			return True
		return False

class PlexAuth(OAuth2):
	def __init__(self, client_id=None, client=None, token=None):
		self.client_id = client_id
		super(PlexAuth, self).__init__(client_id, client, token)
	def __call__(self, r):
		# TODO remove logging
		logging.debug(r.url)
		url_parts = list(urlparse.urlparse(r.url))
		query = dict(urlparse.parse_qsl(url_parts[4]))
		query['api_key'] = self.client_id
		url_parts[4] = urlencode(query)
		r.url = urlparse.urlunparse(url_parts)
		# TODO remove logging
		logging.debug(r.url)
		return super(PlexAuth, self).__call__(r)

class PlexAuthPlugin(AuthPlugin):
	name = 'Plex v1.0 auth'
	auth_type = 'plex'
	description = 'OAuth2 client credentials grant'

	def get_auth(self, username, password):
		client = BackendApplicationClient(username)
		token = PlexToken()
		token.load()
		if token.is_expired():
			# TODO remove logging
			logging.debug('need a new token')
			tok = get_new_token(username, password, TOKEN_URL, token)
			token.update_token(tok)
		return PlexAuth(username, client, token)
