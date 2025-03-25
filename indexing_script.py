# indexing_script.py
import os
from byaldi import RAGMultiModalModel
import torch

# Directory containing the document you want to index.
DOC_DIR = "/Users/gajanratnam/Downloads"  # Replace with the actual path

# Model to Use
COLPALI_MODEL = "vidore/colpali"
# Use the load_models function from the Streamlit app to handle model loading

def load_models(colpali_model):
    try:
        return RAGMultiModalModel.from_pretrained(colpali_model, verbose=10)
    except Exception as e:
        print(f"Failed to load model {colpali_model}: {e}")
        return None


def index_documents(doc_dir, model_name):
    # Set the device
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using MPS device.")
    else:
        device = torch.device("cpu")
        print("Using CPU device.")

    # Check if the directory exists
    if not os.path.exists(doc_dir):
        print(f"Error: Directory '{doc_dir}' not found.")
        return

    # Check if the directory is actually a directory
    if not os.path.isdir(doc_dir):
        print(f"Error: '{doc_dir}' is not a directory.")
        return

    # Initialize RAGMultiModalModel
    RAG = load_models(COLPALI_MODEL)

    if RAG is not None:

        # Get a list of all files in the directory
        files = [f for f in os.listdir(doc_dir) if os.path.isfile(os.path.join(doc_dir, f))]

        if not files:
            print(f"No files found in directory '{doc_dir}'.")
            return

        for filename in files:
            if filename.startswith('.'):  # Skip hidden files
                continue
            file_path = os.path.join(doc_dir, filename)
            print(f"Indexing document: {filename}")

            try:
                RAG.index(
                    input_path=file_path,
                    index_name="document_index",
                    store_collection_with_index=True,
                    overwrite=True,
                )
                print(f"Successfully indexed {filename}")
            except Exception as e:
                print(f"Error indexing {filename}: {e}")
    else:
        print ("The model did not load")
    print("Indexing complete.")


if __name__ == "__main__":
    index_documents(DOC_DIR, COLPALI_MODEL)