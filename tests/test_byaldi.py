# tests/test_byaldi.py
import pytest
import sys
import os
# Add the 'backend' directory to the Python path.
backend_dir = "/Users/gajanratnam/Downloads/clothing-ecommerce/backend"  # Replace this
sys.path.append(backend_dir)

from main import RAGMultiModalModel

@pytest.fixture(scope="module")
def rag_model():
    model = RAGMultiModalModel.from_pretrained("gajanhcc/finetune_colpali_v1_2-own400_steps", device='cpu')
    yield model # provide the fixture value
    del model # cleanup after the fixture is used

def test_rag_loading(rag_model):
  """Test loading the RAG Model"""
  assert rag_model is not None, "Model failed to load"