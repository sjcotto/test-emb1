"""
E-commerce Embedding Model Comparison Framework
Tests similarity search for products and categories using different embedding models.
"""

import numpy as np
from typing import List, Dict, Tuple, Any
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import time
import json

from catalog_data_extended import CATEGORIES, PRODUCTS, SEARCH_QUERIES


class EmbeddingModel:
    """Base class for embedding models"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load(self):
        """Load the model"""
        raise NotImplementedError

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        raise NotImplementedError

    def get_name(self) -> str:
        """Get model display name"""
        return self.model_name


class QwenEmbedding(EmbeddingModel):
    """Qwen embedding model (using Qwen2.5-0.5B-Instruct for embeddings)"""

    def __init__(self):
        super().__init__("Qwen/Qwen2.5-0.5B-Instruct")

    def load(self):
        print(f"Loading {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        self.model.eval()
        print(f"✓ {self.model_name} loaded")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode texts using mean pooling"""
        all_embeddings = []

        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]

                # Tokenize
                inputs = self.tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt"
                )

                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}

                # Get model outputs
                outputs = self.model(**inputs)

                # Mean pooling
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

                # Normalize
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                all_embeddings.append(embeddings.cpu().numpy())

        return np.vstack(all_embeddings)

    def get_name(self) -> str:
        return "Qwen-0.5B"


class JinaEmbedding(EmbeddingModel):
    """Jina Embeddings v3 Classification Distilled"""

    def __init__(self):
        super().__init__("CISCai/jina-embeddings-v3-classification-distilled")

    def load(self):
        print(f"Loading {self.model_name}...")
        self.model = SentenceTransformer(self.model_name, trust_remote_code=True)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        print(f"✓ {self.model_name} loaded")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode texts using SentenceTransformer"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        return embeddings

    def get_name(self) -> str:
        return "Jina-v3-Classification"


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
            model.load()
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
    print("E-COMMERCE EMBEDDING MODEL COMPARISON")
    print("="*80)
    print("\nModels to test:")
    print("  1. Qwen 2.5 0.5B Instruct (used for embeddings)")
    print("  2. Jina Embeddings v3 Classification Distilled")
    print(f"\nCatalog size:")
    print(f"  - {len(PRODUCTS)} products")
    print(f"  - {len(CATEGORIES)} main categories")
    print(f"\nTest queries: {len(SEARCH_QUERIES)}")

    # Initialize models
    models = [
        QwenEmbedding(),
        JinaEmbedding()
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
        'num_queries': len(SEARCH_QUERIES)
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


if __name__ == "__main__":
    main()
