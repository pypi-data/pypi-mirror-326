import os
from unittest import TestCase

import boto3
from moto import mock_aws

from mirror_lambda_environment import MirrorLambdaEnvironment
from mirror_lambda_environment.decorator import mirror_lambda_environment


class TestMirrorEnvironment(TestCase):
    test_lambda_name = 'testing-lambda'

    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()

        # you can use boto3.client("s3") if you prefer
        iam_client = boto3.client("iam", region_name="eu-west-2")
        iam_role = iam_client.create_role(
            RoleName="my-role",
            AssumeRolePolicyDocument="some policy",
            Path="/my-path/",
        )["Role"]["Arn"]
        lambda_client = boto3.client('lambda')
        lambda_client.create_function(
            FunctionName=self.test_lambda_name,
            Runtime='python3.9',
            Role=iam_role,
            Handler='lambda_function.lambda_handler',
            Environment={
                'Variables': {
                    'LAMBDA_VARIABLE_1': 'foo',
                    'LAMBDA_VARIABLE_2': 'bar',
                }
            },
            Code={
                'ZipFile': b'bytes',
            },
            Publish=True,
            Timeout=30,
            MemorySize=128
        )

    def tearDown(self):
        self.mock_aws.stop()

    def _test_environs(self, start, during, end):
        self.assertEqual(
            start, end
        )
        self.assertEqual(
            len(start), len(end)
        )
        self.assertEqual(
            len(start) + 2, len(during)
        )

    def test_with_statement(self):
        start_environ = os.environ
        with MirrorLambdaEnvironment(self.test_lambda_name):
            mirrored_environ = os.environ
        end_environ = os.environ
        self._test_environs(start_environ, mirrored_environ, end_environ)

    def test_decorator(self):
        @mirror_lambda_environment(self.test_lambda_name)
        def mirror_function():
            return os.environ
        start_environ = os.environ
        mirrored_environ = mirror_function()
        end_environ = os.environ
        self._test_environs(start_environ, mirrored_environ, end_environ)



