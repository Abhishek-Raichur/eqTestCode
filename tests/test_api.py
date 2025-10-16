import json
from app import app
import werkzeug
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def clear_cache():
    # Ensure in-memory cache is cleared before each test so mocks are effective
    if hasattr(app, '_gist_cache'):
        app._gist_cache.clear()
    yield


def test_octocat_gists(monkeypatch):
    # Workaround: newer werkzeug may omit __version__; Flask's test client expects it.
    if not hasattr(werkzeug, "__version__"):
        werkzeug.__version__ = "3.0.0"

    # Use real GitHub for this lightweight test; if offline, this may fail.
    client = app.test_client()
    resp = client.get('/octocat')
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    # Each gist should have an 'id' field
    if len(data) > 0:
        assert 'id' in data[0]

def test_gists_success(monkeypatch):
    """Test successful gist fetch with mock."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "abc123", "description": "Test gist"}]
    with patch("app.requests.get", return_value=mock_response):
        client = app.test_client()
        resp = client.get("/octocat")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert data[0]["id"] == "abc123"

def test_gists_user_not_found(monkeypatch):
    """Test 404 for non-existent user with mock."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"message": "Not Found"}
    with patch("app.requests.get", return_value=mock_response):
        client = app.test_client()
        resp = client.get("/nonexistentuser")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["error"] == "not_found"

def test_gists_upstream_error(monkeypatch):
    """Test upstream error handling with mock."""
    import requests as _requests
    with patch("app.requests.get", side_effect=_requests.RequestException("timeout")):
        client = app.test_client()
        resp = client.get("/octocat")
        assert resp.status_code == 502
        data = resp.get_json()
        assert data["error"] == "upstream_error"

def test_gists_invalid_json(monkeypatch):
    """Test invalid JSON from upstream with mock."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("not json")
    with patch("app.requests.get", return_value=mock_response):
        client = app.test_client()
        resp = client.get("/octocat")
        assert resp.status_code == 502
        data = resp.get_json()
        assert data["error"] == "invalid_response"
