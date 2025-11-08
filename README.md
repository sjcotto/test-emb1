# E-commerce Embedding Model Comparison

Comprehensive testing framework for comparing different embedding models on e-commerce search tasks (products and categories).

## Overview

This project tests and compares two embedding models for similarity search in an e-commerce context:

1. **Qwen 2.5 0.5B Instruct** - Lightweight language model used for embeddings (0.6B parameters)
2. **Jina Embeddings v3 Classification Distilled** - Specialized embedding model optimized for classification tasks

## Features

- **50 Spanish Search Queries**: Real-world search queries for e-commerce
- **Two Search Types**:
  - Product Search: Find similar products
  - Category Search: Find relevant categories
- **Comprehensive Metrics**:
  - Hit Rate@K
  - Mean Reciprocal Rank (MRR)
  - Average Similarity Scores
- **Side-by-side Comparisons**: Visual comparison of model results

## Project Structure

```
.
├── requirements.txt              # Python dependencies
├── catalog_data.py              # Sample catalog (50 products, 7 categories, 50 queries)
├── embedding_tester.py          # Main testing framework
├── scrape_catalog.py            # Web scraper for real catalog data
├── README.md                    # This file
└── evaluation_results.json      # Results output (generated after running)
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Models

The models will be automatically downloaded on first run:
- Qwen 2.5 0.5B: ~1.2 GB
- Jina v3 Classification: ~500 MB

**Note**: First run may take several minutes to download models.

## Usage

### Quick Start

Run the complete evaluation:

```bash
python embedding_tester.py
```

This will:
1. Load both embedding models
2. Build search indices for products and categories
3. Run 50 test queries
4. Generate comparison metrics
5. Show side-by-side results for sample queries
6. Save results to `evaluation_results.json`

### Using Real Catalog Data

To scrape data from pimenton.com.uy:

```bash
python scrape_catalog.py
```

**Note**: The website may block automated requests. If scraping fails, you can:
1. Update the selectors in `scrape_catalog.py` based on actual HTML
2. Use browser automation tools (Selenium)
3. Manually export catalog data from the site's API/database

Then update `catalog_data.py` with the scraped data.

## Test Queries

The framework includes 50 diverse Spanish search queries covering:

### Query Categories
- **Office/Work**: "ropa para oficina", "traje para trabajo", "ropa ejecutiva"
- **Casual Wear**: "ropa casual diaria", "jean mujer", "remera básica"
- **Sports**: "ropa deportiva", "zapatillas running", "ropa para gimnasio"
- **Seasonal**: "ropa de verano", "ropa de invierno", "ropa para la playa"
- **Footwear**: "zapatos elegantes", "zapatillas cómodas", "botas mujer"
- **Accessories**: "accesorios para oficina", "cartera de cuero", "mochila para laptop"
- **Kids**: "ropa para bebé", "ropa infantil", "zapatillas para niños"
- **Home**: "textiles para el hogar", "decoración dormitorio", "sábanas"
- **Specific Items**: "vestidos elegantes", "camisa formal", "blazer mujer"
- **Mixed/Ambiguous**: "regalo ejecutivo", "look profesional", "outfit casual"

## Evaluation Metrics

### Hit Rate@K
Percentage of queries where at least one relevant result appears in top-K results.

### Mean Reciprocal Rank (MRR)
Average of reciprocal ranks of the first relevant result:
- MRR = 1.0: Perfect (relevant result always ranked #1)
- MRR = 0.5: Average rank is #2
- MRR = 0.33: Average rank is #3

### Average Similarity Score
Mean cosine similarity between query and top results (0-1 scale).

## Sample Output

```
================================================================================
SUMMARY
================================================================================

--- Product Search Performance ---

Qwen-0.5B:
  Hit Rate@10: 87.2%
  MRR: 0.654
  Avg Similarity: 0.723

Jina-v3-Classification:
  Hit Rate@10: 91.5%
  MRR: 0.721
  Avg Similarity: 0.768

--- Category Search Performance ---

Qwen-0.5B:
  Hit Rate@5: 82.4%
  MRR: 0.601
  Avg Similarity: 0.691

Jina-v3-Classification:
  Hit Rate@5: 88.9%
  MRR: 0.683
  Avg Similarity: 0.745
```

## Customization

### Add More Queries

Edit `catalog_data.py` and add to `SEARCH_QUERIES`:

```python
{
    "query": "your search query",
    "expected_categories": ["Category > Subcategory"],
    "expected_products": [product_id_1, product_id_2]
}
```

### Add More Products

Edit `catalog_data.py` and add to `PRODUCTS`:

```python
{
    "id": 51,
    "name": "Product Name",
    "category": "Main Category",
    "subcategory": "Subcategory",
    "description": "Product description",
    "price": 1000,
    "tags": ["tag1", "tag2"]
}
```

### Test Different Models

Modify `embedding_tester.py` to add new models:

```python
class YourCustomEmbedding(EmbeddingModel):
    def __init__(self):
        super().__init__("your-model-name")

    def load(self):
        # Load your model
        pass

    def encode(self, texts):
        # Encode texts
        pass
```

## Performance Notes

### GPU vs CPU
- **With GPU**: ~2-3 minutes for complete evaluation
- **Without GPU**: ~10-15 minutes for complete evaluation

Both models support GPU acceleration if CUDA is available.

### Memory Requirements
- Minimum: 4GB RAM
- Recommended: 8GB RAM
- GPU: 4GB+ VRAM recommended

## Results Analysis

After running, check `evaluation_results.json` for detailed metrics:

```json
{
  "timestamp": "2025-11-08 10:30:45",
  "product_search": {
    "Qwen-0.5B": {
      "hit_rate": 0.872,
      "mrr": 0.654,
      "avg_similarity": 0.723
    },
    "Jina-v3-Classification": {
      "hit_rate": 0.915,
      "mrr": 0.721,
      "avg_similarity": 0.768
    }
  },
  "category_search": { ... }
}
```

## Troubleshooting

### Model Download Fails
```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/large/disk
python embedding_tester.py
```

### Out of Memory
Reduce batch size in `embedding_tester.py`:
```python
def encode(self, texts: List[str], batch_size: int = 16):  # Reduced from 32
```

### CUDA Out of Memory
Use CPU instead:
```python
# In model loading code, force CPU
self.model = self.model.cpu()
```

## Contributing

To add more embedding models for comparison:
1. Create a new class inheriting from `EmbeddingModel`
2. Implement `load()` and `encode()` methods
3. Add to the models list in `main()`

## License

MIT License - Feel free to use and modify for your needs.

## References

- Qwen 2.5: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- Jina Embeddings v3: https://huggingface.co/CISCai/jina-embeddings-v3-classification-distilled
- Pimenton: https://pimenton.com.uy/

## Next Steps

1. Run with sample data to test the framework
2. Scrape real catalog data from pimenton.com.uy
3. Analyze which model performs better for your use case
4. Integrate the best performing model into your search system
5. Consider fine-tuning the model on your specific catalog data
