import pytest


@pytest.fixture
def mock_succesful_api_fetch(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {
        "title": "A super cool mocked video"
    }
    return mock


@pytest.fixture
def mock_failed_api_fetch(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 404
    mock.get.return_value.json.return_value = {}
    return mock
