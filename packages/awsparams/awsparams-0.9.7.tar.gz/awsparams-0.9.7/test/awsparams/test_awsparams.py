import pytest
from awsparams import awsparams
from moto import mock_ssm


def test_version():
    assert awsparams.__VERSION__ == '0.9.7'


@mock_ssm
def test_connect_ssm():
    assert awsparams.connect_ssm()


def test_translate_results():
    parms = [{'Name': 'test', 'Description': 'testing'}]
    assert awsparams.translate_results(parms) == ['test']
