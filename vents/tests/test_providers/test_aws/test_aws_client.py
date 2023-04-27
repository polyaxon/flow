import os

from unittest import TestCase

import boto3

from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from moto import mock_s3

from vents.providers.aws.base import get_aws_client, get_aws_resource, get_aws_session


class TestAwsClient(TestCase):
    @mock_s3
    def test_get_aws_session(self):
        session = get_aws_session(
            aws_access_key_id="a1",
            aws_secret_access_key="a2",
            aws_session_token="a3",
            region_name="a4",
        )
        assert isinstance(session, boto3.session.Session)
        assert session.region_name == "a4"
        credentials = session.get_credentials()
        assert credentials.access_key == "a1"
        assert credentials.secret_key == "a2"
        assert credentials.token == "a3"

        os.environ.pop("AWS_ACCESS_KEY_ID", "")
        os.environ.pop("AWS_SECRET_ACCESS_KEY", "")
        os.environ.pop("AWS_SECURITY_TOKEN", "")
        os.environ.pop("AWS_REGION", "")
        os.environ["VENTS_AWS_ACCESS_KEY_ID"] = "b1"
        os.environ["VENTS_AWS_SECRET_ACCESS_KEY"] = "b2"
        os.environ["VENTS_AWS_SECURITY_TOKEN"] = "b3"
        os.environ["VENTS_AWS_REGION"] = "b4"
        session = get_aws_session()
        assert isinstance(session, boto3.session.Session)
        assert session.region_name == "b4"
        credentials = session.get_credentials()
        assert credentials.access_key == "b1"
        assert credentials.secret_key == "b2"
        assert credentials.token == "b3"

        # Prevent moto unmock_env_variables from raising an error.
        os.environ["AWS_ACCESS_KEY_ID"] = ""
        os.environ["AWS_SECRET_ACCESS_KEY"] = ""
        os.environ["AWS_SECURITY_TOKEN"] = ""
        os.environ["AWS_REGION"] = ""

    @mock_s3
    def test_get_client(self):
        s3_client = get_aws_client("s3")
        assert isinstance(s3_client, BaseClient)

    @mock_s3
    def test_get_resource(self):
        s3_resource = get_aws_resource("s3")
        assert isinstance(s3_resource, ServiceResource)
