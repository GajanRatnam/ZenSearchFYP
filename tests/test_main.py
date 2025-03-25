import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi import HTTPException  # Import HTTPException
import sys
import os

# Add the 'backend' directory to the Python path.
backend_dir = "/Users/gajanratnam/Downloads/clothing-ecommerce/backend"  # Replace this
sys.path.append(backend_dir)


def test_search_endpoint_success(test_client):
    data = {"text_query": "fashion"}
    response = test_client.post("/search/", data=data)  # Use data, not json
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "image_base64_list" in response.json()
    assert isinstance(response.json()["image_base64_list"], list)


def test_voice_search_endpoint(test_client):
    from unittest.mock import patch
    from main import listen_for_query

    with patch("main.listen_for_query", return_value="test_query"):
        response = test_client.post("/voice_search/")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "image_base64_list" in response.json()
    assert isinstance(response.json()["image_base64_list"], list)