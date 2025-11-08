"""
Download embedding models from HuggingFace
"""

import os
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer

# Set environment variables to help with downloads
os.environ['HF_HUB_OFFLINE'] = '0'
os.environ['TRANSFORMERS_OFFLINE'] = '0'

def download_jina_model():
    """Download Jina embeddings v3 classification distilled"""
    print("="*80)
    print("Downloading Jina Embeddings v3 Classification Distilled")
    print("="*80)

    model_name = "jinaai/jina-embeddings-v3"

    try:
        print(f"\nAttempting to download: {model_name}")
        print("This may take a few minutes (model size: ~500MB)...\n")

        model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
            device='cpu'
        )

        print(f"✓ Successfully downloaded {model_name}")
        print(f"✓ Model saved to cache")

        # Test encoding
        test_text = ["ropa para oficina", "zapatillas running"]
        embeddings = model.encode(test_text)
        print(f"✓ Test encoding successful - embedding dimension: {embeddings.shape[1]}")

        return True

    except Exception as e:
        print(f"✗ Failed to download {model_name}")
        print(f"Error: {e}")

        # Try alternative model name
        alt_model_name = "CISCai/jina-embeddings-v3-classification-distilled"
        print(f"\nTrying alternative: {alt_model_name}")

        try:
            model = SentenceTransformer(
                alt_model_name,
                trust_remote_code=True,
                device='cpu'
            )
            print(f"✓ Successfully downloaded {alt_model_name}")

            # Test encoding
            embeddings = model.encode(test_text)
            print(f"✓ Test encoding successful - embedding dimension: {embeddings.shape[1]}")
            return True

        except Exception as e2:
            print(f"✗ Also failed with alternative name")
            print(f"Error: {e2}")
            return False


def download_multilingual_model():
    """Download a multilingual model as fallback"""
    print("\n" + "="*80)
    print("Downloading Multilingual E5 Model")
    print("="*80)

    model_name = "intfloat/multilingual-e5-small"

    try:
        print(f"\nAttempting to download: {model_name}")
        print("This may take a few minutes...\n")

        model = SentenceTransformer(model_name, device='cpu')

        print(f"✓ Successfully downloaded {model_name}")

        # Test encoding
        test_text = ["query: ropa para oficina", "query: zapatillas running"]
        embeddings = model.encode(test_text)
        print(f"✓ Test encoding successful - embedding dimension: {embeddings.shape[1]}")

        return True

    except Exception as e:
        print(f"✗ Failed to download {model_name}")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("\nStarting model downloads...\n")

    # Try Jina model
    jina_success = download_jina_model()

    # Try multilingual model
    multilingual_success = download_multilingual_model()

    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"Jina model: {'✓ Success' if jina_success else '✗ Failed'}")
    print(f"Multilingual E5: {'✓ Success' if multilingual_success else '✗ Failed'}")

    if jina_success or multilingual_success:
        print("\n✓ At least one model downloaded successfully!")
        print("You can now run the embedding tests.")
    else:
        print("\n✗ All downloads failed.")
        print("Please check your internet connection or HuggingFace API access.")
