import pytest


@pytest.fixture
def mock_failed_status_code(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 404
    return mock


@pytest.fixture
def mock_succesful_api_fetch(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "Introduction to Algorithms",
                    "authors": ["Thomas H. Cormen"],
                    "ISBN": "9780262033848",
                    "imageLinks": {"thumbnail": "super_cool_image.png"}
                }
            }
        ]
    }
    return mock
