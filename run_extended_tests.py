"""
Run embedding model tests with extended catalog
120 products and 100 test queries
"""

import sys
import os

# Import from extended catalog
from catalog_data_extended import CATEGORIES, PRODUCTS, SEARCH_QUERIES

# Temporarily modify the embedding_tester imports
import importlib.util

def run_tests():
    """Run the complete test suite"""
    print("\n" + "="*80)
    print("EXTENDED EMBEDDING MODEL TEST")
    print("="*80)
    print(f"\nTest Configuration:")
    print(f"  Products: {len(PRODUCTS)}")
    print(f"  Categories: {len(CATEGORIES)}")
    print(f"  Main Categories: {len(CATEGORIES)}")
    subcats_total = sum(len(cat['subcategories']) for cat in CATEGORIES.values())
    print(f"  Subcategories: {subcats_total}")
    print(f"  Test Queries: {len(SEARCH_QUERIES)}")

    print(f"\nModels to test:")
    print(f"  1. Qwen 2.5 0.5B Instruct (for embeddings)")
    print(f"  2. Jina Embeddings v3 Classification Distilled")

    # Load the embedding tester module dynamically and patch it
    import embedding_tester

    # Replace the imports in embedding_tester
    embedding_tester.CATEGORIES = CATEGORIES
    embedding_tester.PRODUCTS = PRODUCTS
    embedding_tester.SEARCH_QUERIES = SEARCH_QUERIES

    # Run the main function
    embedding_tester.main()


if __name__ == "__main__":
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nError running tests: {e}")
        import traceback
        traceback.print_exc()
