# Gemma CPU Optimization Guide

**Goal: Maximum inference speed on CPU (2-4x faster than baseline)**

## Quick Start

### 1. Install Optimization Dependencies

```bash
# Install ONNX Runtime (recommended - best speed)
pip install onnxruntime>=1.16.0

# Install Optimum for easy ONNX conversion
pip install optimum[onnxruntime]>=1.16.0
```

### 2. Run Optimized Test

```bash
python test_gemma3_optimized.py
```

This will automatically:
- Test all available optimization methods
- Benchmark each one (5 iterations)
- Compare speeds side-by-side
- Recommend the fastest method for your CPU

## Optimization Methods

### 1. **ONNX Runtime** (Fastest - Recommended) ⚡
- **Speedup**: 2-4x faster than baseline
- **Memory**: Similar to baseline
- **Setup**: `pip install onnxruntime optimum[onnxruntime]`
- **How it works**: Converts model to ONNX format with optimized CPU kernels

**Best for**: Production deployments, maximum speed

### 2. **PyTorch INT8 Quantization** (Good balance)
- **Speedup**: 1.5-2.5x faster
- **Memory**: 50-60% less (2-3 GB instead of 4-6 GB)
- **Setup**: Built-in, no extra dependencies
- **How it works**: Quantizes weights to 8-bit integers

**Best for**: Limited RAM, good speed without extra dependencies

### 3. **BetterTransformer** (Moderate speedup)
- **Speedup**: 1.2-1.5x faster
- **Memory**: Same as baseline
- **Setup**: Built-in to transformers>=4.36
- **How it works**: Optimized attention mechanism

**Best for**: Easy drop-in optimization, no conversion needed

### 4. **Baseline** (No optimization)
- **Speedup**: 1x (reference)
- **Memory**: 4-6 GB
- **Setup**: Just `pip install transformers torch`

## Expected Performance

### On Modern CPU (8 cores, 16 GB RAM)

| Method | Tokens/sec | Speedup | Memory | Setup Time |
|--------|------------|---------|--------|------------|
| **ONNX Runtime** | 15-25 tok/s | **3-4x** | 4-5 GB | 5 min (first run only) |
| **INT8 Quantization** | 10-18 tok/s | **2-3x** | 2-3 GB | Instant |
| **BetterTransformer** | 7-12 tok/s | **1.5x** | 4-6 GB | Instant |
| **Baseline** | 5-8 tok/s | 1x | 4-6 GB | Instant |

*Note: First run with ONNX takes longer (model export), but subsequent runs are instant*

## Sample Output

```
================================================================================
OPTIMIZATION COMPARISON SUMMARY
================================================================================

Method                    Speed (tok/s)   Avg Time (s)    Speedup
----------------------------------------------------------------------
onnx                      22.45           1.337           3.74x
torch_quantization        14.23           2.108           2.37x
bettertransformer         8.91            3.367           1.48x
baseline                  6.01            4.992           1.00x

🏆 Recommended: onnx
   Speed: 22.45 tokens/sec
   Speedup vs baseline: 3.74x
```

## Installation Guide

### Option 1: Install Everything (Recommended)

```bash
# Install all optimizations for maximum flexibility
pip install -r requirements.txt
pip install onnxruntime optimum[onnxruntime]
```

### Option 2: Minimal Install (No extra dependencies)

```bash
# Just use PyTorch INT8 quantization (no extra deps)
pip install -r requirements.txt
python test_gemma3_optimized.py
```

The script will use INT8 quantization automatically if ONNX is not available.

### Option 3: ONNX Only (Best speed)

```bash
pip install -r requirements.txt
pip install onnxruntime optimum[onnxruntime]
python test_gemma3_optimized.py
```

## Usage Examples

### Compare All Methods

```bash
# Runs all available optimization methods and compares them
python test_gemma3_optimized.py
```

### Test Specific Optimization

```python
from test_gemma3_optimized import OptimizedGemmaRunner

# Use ONNX Runtime
runner = OptimizedGemmaRunner()
runner.load_with_optimum_onnx()
results = runner.benchmark(num_iterations=10)

# Or use INT8 quantization
runner = OptimizedGemmaRunner()
runner.load_with_torch_quantization()
results = runner.benchmark(num_iterations=10)
```

## Advanced: Integration with E-commerce Search

For embedding-based product search (like in your main project):

```python
from test_gemma3_optimized import OptimizedGemmaRunner
import torch

# Load optimized model
runner = OptimizedGemmaRunner()
runner.load_with_torch_quantization()  # or load_with_optimum_onnx()

# Generate embeddings for product search
queries = ["ropa para oficina", "zapatillas running", "vestido elegante"]

with torch.no_grad():
    inputs = runner.tokenizer(queries, return_tensors="pt", padding=True)
    outputs = runner.model(**inputs, output_hidden_states=True)
    embeddings = outputs.hidden_states[-1].mean(dim=1)

# Use embeddings for similarity search
# ... (integrate with your existing search code)
```

## Troubleshooting

### ONNX Export Takes Too Long

First export can take 5-10 minutes. This is normal! The model is being converted and optimized. Subsequent runs will be instant because ONNX caches the converted model.

```bash
# Progress is shown during export:
# "Loading with Optimum ONNX Runtime..."
# "Note: First run will export to ONNX (takes a few minutes)"
```

### ONNX Import Error

```bash
pip install --upgrade onnxruntime optimum
```

If still failing, use INT8 quantization instead (no extra deps needed):
```python
runner.load_with_torch_quantization()
```

### Out of Memory with ONNX

ONNX uses similar memory to baseline. If you need lower memory, use INT8 quantization:

```python
# Uses 50% less memory
runner.load_with_torch_quantization()
```

### Slower Than Expected

1. **Check CPU usage**: Make sure no other apps are using CPU
2. **Set thread count**:
   ```python
   import torch
   torch.set_num_threads(8)  # Use all CPU cores
   ```
3. **Disable turbo boost**: Some CPUs throttle under load
4. **Use ONNX**: It's consistently the fastest

## Performance Tips

### 1. Use Static Batch Sizes
```python
# Faster with consistent batch sizes
inputs = tokenizer(texts, return_tensors="pt", padding="max_length", max_length=512)
```

### 2. Disable Sampling for Speed
```python
# Greedy decoding is faster than sampling
outputs = model.generate(**inputs, do_sample=False, max_new_tokens=30)
```

### 3. Set Optimal Thread Count
```python
import torch
torch.set_num_threads(psutil.cpu_count(logical=False))  # Use physical cores
```

### 4. Reduce Max Length
```python
# Shorter sequences = faster inference
outputs = model.generate(**inputs, max_new_tokens=20)  # Instead of 100
```

## Benchmarking Your System

Run the comparison script to find the best method for YOUR specific CPU:

```bash
python test_gemma3_optimized.py
```

Results vary by:
- CPU architecture (Intel vs AMD)
- Number of cores
- RAM speed
- Background processes

Always benchmark on your target hardware!

## Production Recommendations

For production e-commerce search:

1. **Use ONNX Runtime** for maximum speed
2. **Pre-compute embeddings** for your product catalog
3. **Batch queries** when possible
4. **Cache frequent searches**
5. **Use approximate nearest neighbor** (FAISS, Annoy) for similarity search

Example workflow:
```python
# 1. Load optimized model once at startup
runner = OptimizedGemmaRunner()
runner.load_with_optimum_onnx()

# 2. Pre-compute product embeddings (do this once)
product_embeddings = compute_embeddings(all_products)

# 3. At search time (fast!)
query_embedding = compute_embeddings([user_query])
results = similarity_search(query_embedding, product_embeddings)
```

## Comparison: CPU vs GPU

| Metric | CPU (Optimized) | GPU (A100) |
|--------|----------------|------------|
| Speed | 15-25 tok/s | 200-500 tok/s |
| Cost | $0 (existing hardware) | $2-4/hour cloud |
| Memory | 2-6 GB | 4-6 GB VRAM |
| Latency | 50-100ms | 10-20ms |
| **Best for** | Low-cost, moderate load | High throughput, low latency |

For e-commerce search with < 100 QPS (queries per second), optimized CPU is sufficient and much more cost-effective!

## Next Steps

1. **Run the comparison**: `python test_gemma3_optimized.py`
2. **Note your best method**: Check the summary output
3. **Integrate into your app**: Use the fastest method in production
4. **Monitor performance**: Track tokens/sec in production

## References

- ONNX Runtime: https://onnxruntime.ai/
- Optimum: https://huggingface.co/docs/optimum/
- PyTorch Quantization: https://pytorch.org/docs/stable/quantization.html
- BetterTransformer: https://huggingface.co/docs/transformers/main/en/perf_infer_gpu_one#bettertransformer
