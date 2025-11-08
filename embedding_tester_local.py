"""
E-commerce Embedding Model Comparison Framework - Local Implementation
Tests similarity search using locally computed embeddings (no external models needed)
"""

import numpy as np
from typing import List, Dict, Tuple, Any
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import time
import json
import re

from catalog_data_extended import CATEGORIES, PRODUCTS, SEARCH_QUERIES


class EmbeddingModel:
    """Base class for embedding models"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_fitted = False

    def fit(self, texts: List[str]):
        """Fit the model on corpus"""
        raise NotImplementedError

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        raise NotImplementedError

    def get_name(self) -> str:
        """Get model display name"""
        return self.model_name


class TfidfEmbedding(EmbeddingModel):
    """TF-IDF based embeddings"""

    def __init__(self, max_features=1000, ngram_range=(1, 2)):
        super().__init__(f"TF-IDF-{max_features}")
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=1,
            lowercase=True,
            strip_accents='unicode',
            token_pattern=r'\b\w+\b'
        )

    def fit(self, texts: List[str]):
        """Fit TF-IDF on corpus"""
        print(f"  Fitting {self.model_name} on {len(texts)} documents...")
        self.vectorizer.fit(texts)
        self.is_fitted = True
        print(f"  ✓ Vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using TF-IDF"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        vectors = self.vectorizer.transform(texts).toarray()
        # Normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        return vectors / norms

    def get_name(self) -> str:
        return self.model_name


class BM25Embedding(EmbeddingModel):
    """BM25-style embeddings (improved TF-IDF)"""

    def __init__(self, k1=1.5, b=0.75, max_features=1000):
        super().__init__(f"BM25-k{k1}")
        self.k1 = k1
        self.b = b
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 3),  # Include trigrams for better matching
            min_df=1,
            lowercase=True,
            strip_accents='unicode',
            token_pattern=r'\b\w+\b',
            sublinear_tf=True  # Use log scaling
        )

    def fit(self, texts: List[str]):
        """Fit BM25 on corpus"""
        print(f"  Fitting {self.model_name} on {len(texts)} documents...")
        self.vectorizer.fit(texts)
        self.is_fitted = True
        print(f"  ✓ Vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using BM25-style weighting"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")

        # Get TF-IDF vectors
        vectors = self.vectorizer.transform(texts).toarray()

        # Apply BM25-style normalization
        # BM25 uses document length normalization
        doc_lens = np.sum(vectors > 0, axis=1, keepdims=True)
        avg_doc_len = np.mean(doc_lens)

        # BM25 formula: score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len/avg_doc_len))
        # We'll use a simplified version for efficiency
        norm_factor = 1 - self.b + self.b * (doc_lens / avg_doc_len)
        vectors_bm25 = vectors / (1 + self.k1 * norm_factor)

        # Normalize to unit length
        norms = np.linalg.norm(vectors_bm25, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors_bm25 / norms

    def get_name(self) -> str:
        return self.model_name


class CharNGramEmbedding(EmbeddingModel):
    """Character n-gram based embeddings for fuzzy matching"""

    def __init__(self, max_features=2000, ngram_range=(2, 4)):
        super().__init__(f"CharNGram-{ngram_range}")
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=1,
            lowercase=True,
            strip_accents='unicode',
            analyzer='char_wb'  # Character n-grams within word boundaries
        )

    def fit(self, texts: List[str]):
        """Fit character n-gram model on corpus"""
        print(f"  Fitting {self.model_name} on {len(texts)} documents...")
        self.vectorizer.fit(texts)
        self.is_fitted = True
        print(f"  ✓ Char n-gram vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using character n-grams"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        vectors = self.vectorizer.transform(texts).toarray()
        # Normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors / norms

    def get_name(self) -> str:
        return self.model_name


class CatalogSearchEngine:
    """Search engine for products and categories using embeddings"""

    def __init__(self, embedding_model: EmbeddingModel):
        self.model = embedding_model
        self.products = PRODUCTS
        self.categories = CATEGORIES

        # Prepare text representations
        self.product_texts = []
        self.product_ids = []
        self.category_texts = []
        self.category_keys = []

        self._prepare_catalog()

        # Embeddings
        self.product_embeddings = None
        self.category_embeddings = None

    def _prepare_catalog(self):
        """Prepare text representations for products and categories"""
        # Products: combine name, category, subcategory, description, and tags
        for product in self.products:
            text = f"{product['name']}. {product['description']}. "
            text += f"Categoría: {product['category']} - {product['subcategory']}. "
            text += f"Tags: {', '.join(product['tags'])}"
            self.product_texts.append(text)
            self.product_ids.append(product['id'])

        # Categories: combine category name, subcategories, and description
        for cat_name, cat_data in self.categories.items():
            text = f"{cat_name}. {cat_data['description']}. "
            text += f"Subcategorías: {', '.join(cat_data['subcategories'])}"
            self.category_texts.append(text)
            self.category_keys.append(cat_name)

            # Also add subcategories as separate entries
            for subcat in cat_data['subcategories']:
                subcat_text = f"{cat_name} - {subcat}. {cat_data['description']}"
                self.category_texts.append(subcat_text)
                self.category_keys.append(f"{cat_name} > {subcat}")

    def build_index(self):
        """Build embeddings for all products and categories"""
        print(f"\nBuilding index with {self.model.get_name()}...")

        # Fit model on combined corpus
        all_texts = self.product_texts + self.category_texts
        self.model.fit(all_texts)

        print(f"  - Encoding {len(self.product_texts)} products...")
        self.product_embeddings = self.model.encode(self.product_texts)

        print(f"  - Encoding {len(self.category_texts)} categories...")
        self.category_embeddings = self.model.encode(self.category_texts)
        print("✓ Index built")

    def search_products(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """Search for products similar to query"""
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.product_embeddings)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(self.product_ids[idx], float(similarities[idx])) for idx in top_indices]
        return results

    def search_categories(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for categories similar to query"""
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.category_embeddings)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(self.category_keys[idx], float(similarities[idx])) for idx in top_indices]
        return results


class EmbeddingEvaluator:
    """Evaluate and compare embedding models on search tasks"""

    def __init__(self, models: List[EmbeddingModel]):
        self.models = models
        self.search_engines = {}

    def setup(self):
        """Load models and build indices"""
        for model in self.models:
            engine = CatalogSearchEngine(model)
            engine.build_index()
            self.search_engines[model.get_name()] = engine

    def evaluate_product_search(self, top_k: int = 10) -> Dict[str, Any]:
        """Evaluate product search performance"""
        print("\n" + "="*80)
        print("EVALUATING PRODUCT SEARCH")
        print("="*80)

        results = {}

        for model_name, engine in self.search_engines.items():
            print(f"\nTesting {model_name}...")

            hits_at_k = []
            mrr_scores = []
            avg_similarities = []

            for test in tqdm(SEARCH_QUERIES, desc=f"{model_name} product search"):
                query = test['query']
                expected_products = test.get('expected_products', [])

                if not expected_products:
                    continue

                # Search
                search_results = engine.search_products(query, top_k=top_k)
                found_ids = [pid for pid, _ in search_results]

                # Metrics
                # Hit@K: is any expected product in top-k?
                hit = any(pid in expected_products for pid in found_ids)
                hits_at_k.append(1 if hit else 0)

                # MRR: reciprocal rank of first relevant result
                rank = None
                for i, pid in enumerate(found_ids, 1):
                    if pid in expected_products:
                        rank = i
                        break
                mrr_scores.append(1.0 / rank if rank else 0.0)

                # Average similarity of top results
                avg_sim = np.mean([sim for _, sim in search_results])
                avg_similarities.append(avg_sim)

            results[model_name] = {
                'hit_rate': np.mean(hits_at_k) if hits_at_k else 0,
                'mrr': np.mean(mrr_scores) if mrr_scores else 0,
                'avg_similarity': np.mean(avg_similarities) if avg_similarities else 0,
                'num_queries': len(hits_at_k)
            }

            print(f"  Hit Rate@{top_k}: {results[model_name]['hit_rate']:.3f}")
            print(f"  MRR: {results[model_name]['mrr']:.3f}")
            print(f"  Avg Similarity: {results[model_name]['avg_similarity']:.3f}")

        return results

    def evaluate_category_search(self, top_k: int = 5) -> Dict[str, Any]:
        """Evaluate category search performance"""
        print("\n" + "="*80)
        print("EVALUATING CATEGORY SEARCH")
        print("="*80)

        results = {}

        for model_name, engine in self.search_engines.items():
            print(f"\nTesting {model_name}...")

            hits_at_k = []
            mrr_scores = []
            avg_similarities = []

            for test in tqdm(SEARCH_QUERIES, desc=f"{model_name} category search"):
                query = test['query']
                expected_categories = test.get('expected_categories', [])

                if not expected_categories:
                    continue

                # Search
                search_results = engine.search_categories(query, top_k=top_k)
                found_cats = [cat for cat, _ in search_results]

                # Metrics
                # Hit@K: is any expected category in top-k?
                hit = any(cat in expected_categories for cat in found_cats)
                hits_at_k.append(1 if hit else 0)

                # MRR
                rank = None
                for i, cat in enumerate(found_cats, 1):
                    if cat in expected_categories:
                        rank = i
                        break
                mrr_scores.append(1.0 / rank if rank else 0.0)

                # Average similarity
                avg_sim = np.mean([sim for _, sim in search_results])
                avg_similarities.append(avg_sim)

            results[model_name] = {
                'hit_rate': np.mean(hits_at_k) if hits_at_k else 0,
                'mrr': np.mean(mrr_scores) if mrr_scores else 0,
                'avg_similarity': np.mean(avg_similarities) if avg_similarities else 0,
                'num_queries': len(hits_at_k)
            }

            print(f"  Hit Rate@{top_k}: {results[model_name]['hit_rate']:.3f}")
            print(f"  MRR: {results[model_name]['mrr']:.3f}")
            print(f"  Avg Similarity: {results[model_name]['avg_similarity']:.3f}")

        return results

    def compare_side_by_side(self, sample_queries: List[str], top_k: int = 5):
        """Show side-by-side comparison for sample queries"""
        print("\n" + "="*80)
        print("SIDE-BY-SIDE COMPARISON")
        print("="*80)

        for query in sample_queries:
            print(f"\n{'='*80}")
            print(f"Query: '{query}'")
            print(f"{'='*80}")

            # Product search
            print(f"\n--- PRODUCT SEARCH (Top {top_k}) ---")
            for model_name, engine in self.search_engines.items():
                results = engine.search_products(query, top_k=top_k)
                print(f"\n{model_name}:")
                for i, (pid, score) in enumerate(results, 1):
                    product = next(p for p in PRODUCTS if p['id'] == pid)
                    print(f"  {i}. [{score:.3f}] {product['name']} ({product['category']} > {product['subcategory']})")

            # Category search
            print(f"\n--- CATEGORY SEARCH (Top {top_k}) ---")
            for model_name, engine in self.search_engines.items():
                results = engine.search_categories(query, top_k=top_k)
                print(f"\n{model_name}:")
                for i, (cat, score) in enumerate(results, 1):
                    print(f"  {i}. [{score:.3f}] {cat}")


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("E-COMMERCE EMBEDDING MODEL COMPARISON (LOCAL)")
    print("="*80)
    print("\nModels to test:")
    print("  1. TF-IDF with unigrams and bigrams")
    print("  2. BM25-style embeddings (improved TF-IDF)")
    print("  3. Character N-gram embeddings (fuzzy matching)")
    print(f"\nCatalog size:")
    print(f"  - {len(PRODUCTS)} products")
    print(f"  - {len(CATEGORIES)} main categories")
    print(f"\nTest queries: {len(SEARCH_QUERIES)}")

    # Initialize models
    models = [
        TfidfEmbedding(max_features=1500, ngram_range=(1, 2)),
        BM25Embedding(k1=1.5, b=0.75, max_features=2000),
        CharNGramEmbedding(max_features=2000, ngram_range=(2, 4))
    ]

    # Setup evaluator
    evaluator = EmbeddingEvaluator(models)
    evaluator.setup()

    # Run evaluations
    product_results = evaluator.evaluate_product_search(top_k=10)
    category_results = evaluator.evaluate_category_search(top_k=5)

    # Save results
    results_summary = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'product_search': product_results,
        'category_search': category_results,
        'num_products': len(PRODUCTS),
        'num_categories': len(CATEGORIES),
        'num_queries': len(SEARCH_QUERIES),
        'models': [m.get_name() for m in models]
    }

    with open('evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, indent=2, ensure_ascii=False)

    print("\n✓ Results saved to evaluation_results.json")

    # Show side-by-side comparisons for interesting queries
    sample_queries = [
        "ropa para oficina",
        "zapatillas running",
        "ropa deportiva",
        "vestidos elegantes",
        "regalo ejecutivo"
    ]

    evaluator.compare_side_by_side(sample_queries, top_k=5)

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    print("\n--- Product Search Performance ---")
    for model_name, metrics in product_results.items():
        print(f"\n{model_name}:")
        print(f"  Hit Rate@10: {metrics['hit_rate']:.1%}")
        print(f"  MRR: {metrics['mrr']:.3f}")
        print(f"  Avg Similarity: {metrics['avg_similarity']:.3f}")

    print("\n--- Category Search Performance ---")
    for model_name, metrics in category_results.items():
        print(f"\n{model_name}:")
        print(f"  Hit Rate@5: {metrics['hit_rate']:.1%}")
        print(f"  MRR: {metrics['mrr']:.3f}")
        print(f"  Avg Similarity: {metrics['avg_similarity']:.3f}")

    # Determine winner
    print("\n" + "="*80)
    print("WINNER ANALYSIS")
    print("="*80)

    best_product_model = max(product_results.items(), key=lambda x: x[1]['hit_rate'])
    best_category_model = max(category_results.items(), key=lambda x: x[1]['hit_rate'])

    print(f"\nBest for Product Search: {best_product_model[0]}")
    print(f"  Hit Rate: {best_product_model[1]['hit_rate']:.1%}")

    print(f"\nBest for Category Search: {best_category_model[0]}")
    print(f"  Hit Rate: {best_category_model[1]['hit_rate']:.1%}")


if __name__ == "__main__":
    main()
