import pytest
import pytest_asyncio
import sys
import os

# Add the 'backend' directory to the Python path.
backend_dir = "/Users/gajanratnam/Downloads/clothing-ecommerce/backend"  # Replace this
sys.path.append(backend_dir)

print(f"Current file: {__file__}")
print(f"backend_dir (ABSOLUTE): {backend_dir}")
print(f"sys.path: {sys.path}")

try:
    from main import app, load_models  # DIRECT IMPORT FROM backend/main.py
    print("Successfully imported main")
except ImportError as e:
    print(f"ImportError: {e}")
    raise  # Re-raise the exception to stop pytest

from fastapi.testclient import TestClient

@pytest.fixture(scope="module", autouse=True)
def setup_model():
    from main import load_models #Importing here will make sure the sys path gets called first.
    load_models("gajanhcc/finetune_colpali_v1_2-own400_steps")  # Replace with a test model
    yield
    # Teardown code here (if needed)

@pytest.fixture
def test_client():
    from main import app
    with TestClient(app) as client:
        yield client