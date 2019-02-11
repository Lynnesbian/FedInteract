#!/usr/bin/env python3

# Copyright (C) 2019 Lynne (@lynnesbian@fedi.lynnesbian.space)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from mastodon import Mastodon
from Misskey import Misskey
import diaspy

#fixtodon overrides a JSON parsing method used by mastodon.py that breaks pleroma support.
#specifically this function: https://github.com/halcy/Mastodon.py/blob/8b8626978752baf14347498640b2319db832145e/mastodon/Mastodon.py#L2110

#another issue not fixed by fixtodon: calling fetch_next will cause a crash if used on pleroma instances, so we're just not gonna use it ;)
#fetching things via activitypub's outbox.json is faster anyway

#thanks to jfmcbrayer - https://github.com/jfmcbrayer/Mastodon.py/commit/07853f241524ea965e796e0c8e1bf6dade63c2a9

class Fixtodon(Mastodon):
	@staticmethod
	def __json_strnum_to_bignum(self, json_object):
		raise AttributeError("dont use this uwu")

	@staticmethod
	def __json_hooks(self, json_object):
		json_object = Mastodon.__json_date_parse(json_object)
		json_object = Mastodon.__json_truefalse_parse(json_object)
		json_object = Mastodon.__json_allow_dict_attrs(json_object)
		return json_object

class FedInteract():
	def __init__(self, instance_type, instance_url, username = None, password = None, client_id = None, client_secret = None, access_token = None, api_token = None):
		"""
		Create a new FedInteract API wrapper. 


		lkjda
		"""
		self.client = None
		if instance_type in ["mastodon", "pleroma"]:
			if username != None and password != None:
				# use username/password
				# warning: grants all scopes (full account access)
				access_token = Mastodon.log_in(username=username, password=password, api_base_url=instance_url)
				self.client = Mastodon(access_token=access_token, api_base_url=instance_url)
			else:
				self.client = Mastodon(client_id=client_id, client_secret=client_secret, access_token = access_token, api_base_url=instance_url)

		elif instance_type == "misskey":
			self.client = Misskey(instanceAddress = instance_url, appSecret = client_secret, accessToken = access_token, apiToken = api_token)

		elif instance_type == "diaspora":
			if username == None or password == None:
				raise FedInteractError("Insufficient credentials.")

			self.client = diaspy.connection.Connection(pod = instance_url, username = username, password = password)
			self.client.login()

class FedInteractError(Exception):
	# base error
	pass

class FedInteractInvalidCredentialsError(FedInteractError):
	# insufficient credentials were supplied
	pass

