from pathlib import Path
from unittest.mock import mock_open, patch

import httpx
import pytest

from lunar_birthday_ical.pastebin import (
    pastebin_helper,
    pastebin_update,
    pastebin_upload,
)


@pytest.fixture
def mock_file():
    return Path("/path/to/mock/file.txt")


@pytest.fixture
def mock_config():
    return {
        "pastebin": {
            "baseurl": "http://mockbaseurl.com",
            "name": "mockname",
            "password": "mockpassword",
            "expiration": "7d",
        }
    }


@patch("builtins.open", new_callable=mock_open, read_data="mock file content")
@patch("httpx.post")
def test_pastebin_upload(mock_post, mock_open, mock_file):
    mock_response = httpx.Response(200, json={"key": "value"})
    mock_post.return_value = mock_response

    response = pastebin_upload("http://mockbaseurl.com", mock_file, expiration="7d")

    mock_post.assert_called_once_with(
        "http://mockbaseurl.com/",
        data={"p": True, "e": "7d"},
        files={"c": mock_open.return_value},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


@patch("builtins.open", new_callable=mock_open, read_data="mock file content")
@patch("httpx.put")
def test_pastebin_update(mock_put, mock_open, mock_file):
    mock_response = httpx.Response(200, json={"key": "value"})
    mock_put.return_value = mock_response

    response = pastebin_update(
        "http://mockbaseurl.com", "mockname", "mockpassword", mock_file, expiration="7d"
    )

    mock_put.assert_called_once_with(
        "http://mockbaseurl.com/mockname:mockpassword",
        data={"e": "7d"},
        files={"c": mock_open.return_value},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


@patch("lunar_birthday_ical.pastebin.pastebin_upload")
@patch("lunar_birthday_ical.pastebin.pastebin_update")
def test_pastebin_helper(mock_update, mock_upload, mock_config, mock_file):
    mock_response = httpx.Response(200, json={"key": "value"})
    mock_upload.return_value = mock_response
    mock_update.return_value = mock_response

    pastebin_helper(mock_config, mock_file)
    mock_update.assert_called_once_with(
        baseurl="http://mockbaseurl.com",
        name="mockname",
        password="mockpassword",
        file=mock_file,
        expiration="7d",
    )

    mock_config["pastebin"]["password"] = None
    pastebin_helper(mock_config, mock_file)
    mock_upload.assert_called_once_with(
        baseurl="http://mockbaseurl.com", file=mock_file, expiration="7d"
    )
