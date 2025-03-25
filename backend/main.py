from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from byaldi import RAGMultiModalModel
from PIL import Image
from io import BytesIO
import base64
import os
import torch
from typing import List, Dict, Optional, Tuple
import traceback
import certifi
import sounddevice as sd

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Try to import PyPDF2
try:
    from PyPDF2 import PdfReader
    pdf_reader_available = True
    print("PyPDF2 successfully imported")
except ImportError:
    pdf_reader_available = False
    print("PyPDF2 not available, please install it with: pip install PyPDF2")

import chromadb
from chromadb.utils import embedding_functions

# Voice Integration Libraries
import asyncio

# Whisper Integration
import whisper
import ssl

# Define speak function at the top
def speak(text: str):
    """Prints the given text."""
    print(f"AI: {text}")  # Print to console instead of speaking

# Check sounddevice import at the top level
try:
    import sounddevice as sd
    print("Sounddevice imported successfully at top level!")
except ImportError as e:
    print(f"Error importing sounddevice at top level: {e}")

app = FastAPI()

# Configure CORS (Ensure correct origin for your React app)
origins = [
    "http://localhost:3000",  # VERY IMPORTANT: Replace with your React app's origin
    "http://localhost",  # Also allow localhost for API testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Specify the directory for uploads
UPLOAD_DIR = "./doc"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define the RAG model (outside the endpoint to load it only once)
RAG: Optional[RAGMultiModalModel] = None
COLPALI_MODEL = "gajanhcc/finetune_colpali_v1_2-own400_steps"
CHROMA_COLLECTION_NAME = "document_index"
CHROMA_PERSIST_DIR = "./chroma_db"

# Chroma client and collection (initialize to None)
chroma_client: Optional[chromadb.Client] = None
chroma_collection: Optional[chromadb.Collection] = None
whisper_model = None

def load_models(colpali_model: str):
    global RAG, chroma_client, chroma_collection, whisper_model

    try:
        # Check if MPS is available and use it, otherwise use CPU
        device = torch.device("cpu")  # Default to CPU
        
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            print("MPS device found. Using MPS for model loading.")
        else:
            print("MPS device not found. Using CPU for model loading.")

        # Create the model with device='cpu' first, then move to MPS if available
        # This is safer as some models have initialization steps that aren't MPS compatible
        RAG = RAGMultiModalModel.from_pretrained(
            colpali_model, 
            verbose=10,
            device='cpu'  # Load initially on CPU
        )
        
        # Now move it to the target device if needed
        #if device.type == "mps":
         #   RAG.to(device)
            
        print("RAG model loaded successfully.")

        # Initialize ChromaDB client
        chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

        # Create or get the ChromaDB collection
        chroma_collection = chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME
        )

        print("ChromaDB client and collection initialized successfully.")

        # Index the document if specified file exists
        doc_path = "/Users/gajanratnam/Downloads/ind/doci.pdf"

        # Enhanced diagnostic for file path
        print(f"Checking PDF path: {doc_path}")
        if os.path.exists(doc_path):
            print(f"File exists at: {doc_path}")
            if os.path.isfile(doc_path):
                print("It is a file (not a directory)")
                if os.access(doc_path, os.R_OK):
                    print("File is readable")
                else:
                    print("WARNING: File exists but is not readable")
            else:
                print("WARNING: Path exists but is not a file")
        else:
            print(f"Warning: Document '{doc_path}' not found. Skipping indexing step.")
            return

        if os.path.isdir(doc_path):
            print(f"Error: Directory '{doc_path}' directory can't be indexed, needs a proper directory with files.")
            return

        try:
            RAG.index(
                input_path=doc_path,
                index_name="document_index",
                store_collection_with_index=True,
                overwrite=True,
            )

            print("Documents added to ChromaDB.")
            print("Document indexed successfully.")

        except Exception as e:
            print(f"Error during indexing: {e}")
            traceback.print_exc()

    except Exception as e:
        print(f"Failed to load model {colpali_model}: {e}")
        traceback.print_exc()

def load_whisper_model(model_name="base"):  # Choose a model size
    global whisper_model

    try:
        # Apply SSL Bypass if needed
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        whisper_model = whisper.load_model(model_name)
        print(f"Whisper model '{model_name}' loaded successfully.")
    except Exception as e:
        print(f"Failed to load Whisper model: {e}")
        traceback.print_exc()

# Try a test PDF if the original one fails
def try_test_pdf():
    print("\n=== Trying with a test PDF ===")
    # Create a test PDF with PyPDF2
    try:
        from PyPDF2 import PdfWriter

        test_pdf_path = "./test_document.pdf"
        writer = PdfWriter()

        # Add a blank page with some text
        writer.add_blank_page(width=612, height=792)

        # Write to file
        with open(test_pdf_path, "wb") as output_file:
            writer.write(output_file)

        print(f"Created test PDF at {test_pdf_path}")
        
        # Try to index the test PDF
        if RAG is not None:
            RAG.index(
                input_path=test_pdf_path,
                index_name="document_index",
                store_collection_with_index=True,
                overwrite=True,
            )
            print("Test PDF indexed successfully.")

    except Exception as e:
        print(f"Failed to create or index test PDF: {e}")
        traceback.print_exc()

    print("=== End of test PDF check ===\n")

async def listen_for_query():
    """Listens for a voice query using Whisper and returns the text."""
    global whisper_model  # Access the global Whisper model
    if whisper_model is None:
        speak("Whisper model not loaded. Please check the server logs.")
        return ""

    try:
        print("Listening...")
        speak("Listening...")

        # --- Recording audio using sounddevice ---
        try:
            import numpy as np
            from scipy.io.wavfile import write
        except ImportError as e:
            print(f"Failed to import required library: {e}")
            speak(f"Error during voice transcription setup: Missing library - {e}")
            return ""

        fs = 44100  # Sample rate
        duration = 5  # Recording duration in seconds

        # Record audio
        try:
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()  # Wait until recording is finished

            # Convert the recording to float32, which Whisper expects
            myrecording = myrecording.astype(np.float32)

            # Save as WAV file
            temp_wav_file = "temp_audio.wav"
            write(temp_wav_file, fs, myrecording)
        except Exception as e:
            print(f"Error during audio recording : {e}")
            speak(f"Error during audio recording: {e}")
            return ""

        print("Transcribing...")
        try:
            result = whisper_model.transcribe(temp_wav_file)
            query = result["text"]
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            speak(f"Error transcribing audio : {e}")
            return ""

        # Clean up the temporary file
        os.remove(temp_wav_file)  # deletes the audio

        print(f"User said: {query}")
        return query

    except Exception as e:
        speak(f"Error processing voice transcription: {e}")
        traceback.print_exc()
        return ""

@app.post("/search/")
async def search_endpoint(text_query: str = Form(...)) -> Dict[str, List[str]]:
    global RAG, chroma_collection
    if RAG is None or chroma_collection is None:
        speak("Model not loaded, please check the server.")  # Speak the error
        raise HTTPException(
            status_code=500, detail="RAG model or ChromaDB not loaded. Check server logs."
        )

    try:
        # Determine the device to use
        device = torch.device("cpu")
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            
        # Ensure the model is on the correct device
        #RAG.to(device)

        # Perform the search using byaldi
        results = RAG.search(text_query, k=3, return_base64_results=True)
        image_base64_list: List[str] = []
        similarity_scores: List[float] = []

        if results:
            print("\n=== Search Results ===")
            for i, result in enumerate(results):
                print(f"Result {i + 1}:")
                print(f"  Base64: {result.base64[:100]}...")  # Print the first 100 characters of the base64 string
                print(f"  Score: {result.score}")  # Print the score
                image_base64_list.append(result.base64)
                similarity_scores.append(result.score)
                print(f"  Metadata: {result.metadata}")  # added the print to analyze and determine the score

            # Print a summary of the scores
            print(f"\nSimilarity Scores Summary: {similarity_scores}")
            print("=== End of Search Results ===\n")  # Added and will help debug the details
            speak(f"Found {len(results)} results for {text_query}.")  # Added spoken confirmation

            return {"image_base64_list": image_base64_list}

        else:
            print("No results found.")
            speak(f"No results found for {text_query}.")  # Speak no results found
            return {"image_base64_list": []}

    except Exception as e:
        speak(f"Error during search: {e}")  # Speak the error
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error during search: {e}")

@app.post("/voice_search/")
async def voice_search_endpoint() -> Dict[str, List[str]]:
    """Endpoint to handle voice-based search queries."""
    try:
        print("Voice search endpoint hit!")  # Add this for debugging
        query = await listen_for_query()
        if not query:
            print("No voice query received.")
            return {"image_base64_list": []}  # Return empty list if no query

        print(f"Voice query: {query}")
        return await search_endpoint(text_query=query)  # Use existing search function
    except Exception as e:
        print(f"Error processing voice search: {e}")
        traceback.print_exc()  # Print the traceback
        speak(f"Error processing voice search: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing voice search: {e}")

# Startup event to initialize models
@app.on_event("startup")
async def startup_event():
    # Load models on server startup
    load_whisper_model()
    load_models(COLPALI_MODEL)
    
    # If regular model loading fails, try with a test PDF
    if RAG is None:
        print("Initial model loading failed, trying with test PDF...")
        try_test_pdf()

# Add code here for testing
# Run this code at compile time first thing.
try:
    import sounddevice as sd
    print(sd.query_devices())  # Try a basic function
    print("sounddevice imported successfully at compile time!")
except Exception as e:
    print(f"Error importing or using sounddevice at compile time: {e}")
print("Check 1 Complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
