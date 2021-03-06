#!/usr/bin/python

from unittest import TestCase

import ocr.googlevision.get_vision_service 
from ocr.googlevision.get_vision_service  import get_vision_service
from ocr.googlevision import detect_text

from ocr.googlevision.get_vision_service import GoogleCredentials
from oauth2client.service_account import _JWTAccessCredentials

from mock import MagicMock, patch, ANY, sentinel, mock_open, Mock



patch_discoverty_build = patch.object(ocr.googlevision.get_vision_service.discovery, 'build')


class _AbstractGetVisionServiceTestCaseBase(TestCase):

	def assert_build_called_with_developerKey(self, discovery_build, developerKey):
		#
		discovery_build.assert_called_once()

		#
		_args, kwargs = discovery_build.call_args
		self.assertEqual(kwargs['developerKey'], developerKey)

	def assert_build_called_with_credentials(self, discovery_build):
		#
		discovery_build.assert_called_once()

		#
		_args, kwargs = discovery_build.call_args
		self.assertEqual(kwargs['credentials'], sentinel.FAKE_CREDENTIALS)

	def assert_build_credentials_from_dict(self, from_json_keyfile_dict):
		#
		#_args, kwargs = discovery_build.call_args
		#self.assertIsInstance(kwargs['credentials'], GoogleCredentials)

		# cannot test actual build, it checks signature.
		from_json_keyfile_dict.assert_called_once()



@patch_discoverty_build
class GetVisionServiceByArgumentTestCase(_AbstractGetVisionServiceTestCaseBase):

	def test_passing__api_key__builds_service_with_developerKey_option(self, build):
		'''passing `api_key` builds service with `developerKey` option '''
		api_key = 'ABCD1234'
		service = get_vision_service(api_key=api_key)
		#
		self.assert_build_called_with_developerKey(build, api_key)

	def test_passing__credentials__builds_service_with_credentials(self, discovery_build):
		'''passing `credentials` builds service with `credentials` option '''
		service = get_vision_service(credentials=sentinel.FAKE_CREDENTIALS)
		#
		self.assert_build_called_with_credentials(discovery_build)

	@patch.object(_JWTAccessCredentials, 'from_json_keyfile_dict')
	def test_passing__credentials__as_dict_builds_credentials(self, from_json_keyfile_dict, discovery_build):
		'''passing `credentials` as a json data builds service with credentials built '''

		fake_json_data = {
			"type": "service_account",
			"project_id": "projectid",
			"private_key_id": "12345abcdefg",
			"private_key": "-----BEGIN PRIVATE KEY-----\nABCE12334\n-----END PRIVATE KEY-----\n",
			"client_email": "projectid@projectid.iam.gserviceaccount.com",
			"client_id": "12345",
			"auth_uri": "https://accounts.google.com/o/oauth2/auth",
			"token_uri": "https://accounts.google.com/o/oauth2/token",
			"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
			"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/projectid%40projectid.iam.gserviceaccount.com"
		}
		service = get_vision_service(credentials=fake_json_data)

		#
		self.assert_build_credentials_from_dict(from_json_keyfile_dict)




@patch.dict('os.environ', {'GOOGLE_SERVER_APIKEY_': ''})
@patch.dict('os.environ', {'GOOGLE_APPLICATION_CREDENTIALS': ''})
@patch_discoverty_build
class GetVisionServiceByEnvionrmentVariable(_AbstractGetVisionServiceTestCaseBase):

	@patch.dict('os.environ', {'GOOGLE_SERVER_APIKEY_': 'ABCD1234'})
	def test_setting_environment_variable_GOOGLE_SERVER_APIKEY___builds_service_with_developerKey_option(self, build):
		'''GOOGLE_SERVER_APIKEY_ env variable builds service with `developerKey` option '''
		service = get_vision_service()
		#
		self.assert_build_called_with_developerKey(build, 'ABCD1234')


	@patch.dict('os.environ', {'GOOGLE_APPLICATION_CREDENTIALS': 'credentials_file_test.json'})
	@patch.object(GoogleCredentials, 'get_application_default')
	def test_setting_environment_variable_GOOGLE_APPLICATION_CREDENTIALS__builds_service_with_credentials_option(self, get_app_default, build):
		'''GOOGLE_APPLICATION_CREDENTIALS env variable builds discovery service with `credentials` option '''
		get_app_default.return_value = sentinel.FAKE_CREDENTIALS

		#
		service = get_vision_service()

		#
		self.assert_build_called_with_credentials(build)


@patch_discoverty_build
class GetVisionServiceBySettings(_AbstractGetVisionServiceTestCaseBase):

	def setUp(self):
		class FakeSetting: 
			pass
		self.settings = FakeSetting()

	def test_passing_object_with__GOOGLE_SERVER_APIKEY___builds_service_with_developerKey_option(self, build):
		self.settings.GOOGLE_SERVER_APIKEY_ = 'ABCD1234'
		#
		service = get_vision_service(settings=self.settings)
		#
		self.assert_build_called_with_developerKey(build, 'ABCD1234')


	@patch.object(ocr.googlevision.get_vision_service, '_get_application_default_credential_from_file')
	def test_passing_object_with__GOOGLE_APPLICATION_CREDENTIALS__builds_service_with_credentials_option(self, get_app_default, build):
		self.settings.GOOGLE_APPLICATION_CREDENTIALS = 'fake_credential.json'
		get_app_default.return_value = sentinel.FAKE_CREDENTIALS

		#
		service = get_vision_service(settings=self.settings)
		#
		self.assert_build_called_with_credentials(build)


	@patch.object(_JWTAccessCredentials, 'from_json_keyfile_dict')
	def test_passing_object_with__each_of__GOOGLE_APPLICATION_CREDENTIALS____builds_GoogleCredentials(self, from_json_keyfile_dict, discovery_build):

		self.settings.GOOGLE_APPLICATION_CREDENTIALS__type                        = "service_account"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__project_id                  = "projectid"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__private_key_id              = "12345abcdefg"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__private_key                 = "-----BEGIN PRIVATE KEY-----\nABCE12334\n-----END PRIVATE KEY-----\n"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__client_email                = "projectid@projectid.iam.gserviceaccount.com"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__client_id                   = "12345"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__auth_uri                    = "https://accounts.google.com/o/oauth2/auth"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__token_uri                   = "https://accounts.google.com/o/oauth2/token"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
		self.settings.GOOGLE_APPLICATION_CREDENTIALS__client_x509_cert_url        = "https://www.googleapis.com/robot/v1/metadata/x509/projectid%40projectid.iam.gserviceaccount.com"

		#
		service = get_vision_service(settings=self.settings)
		#
		self.assert_build_credentials_from_dict(from_json_keyfile_dict)


