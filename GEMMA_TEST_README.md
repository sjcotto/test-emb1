# Gemma 3 1B CPU Test Script

Comprehensive test script for running Google Gemma 3 1B (or Gemma 2 fallback) on CPU with performance metrics.

## Features

- **System Resource Monitoring**: CPU, RAM, and disk usage tracking
- **Model Loading**: Automatic download and loading with fallback to alternative models
- **Text Generation Tests**: Multiple prompts with performance metrics
- **Embedding Generation**: Test extracting embeddings from hidden states
- **Benchmark Suite**: Multiple iterations to measure average performance
- **Memory Tracking**: Monitor memory usage throughout testing
- **CPU Optimization**: Configured specifically for CPU inference

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `transformers` - HuggingFace model loading
- `torch` - PyTorch backend
- `psutil` - System resource monitoring
- `numpy` - Numerical operations

### 2. Run the Test Script

```bash
python test_gemma3_1b_cpu.py
```

**Note**: First run will download the model (~4-5 GB), which may take 5-10 minutes depending on your connection.

## What Gets Tested

### 1. System Resources
- CPU cores and usage
- Total, available, and used RAM
- Disk space

### 2. Model Loading
- Automatic model download from HuggingFace
- Memory usage during loading
- Load time measurement
- Parameter count verification
- Fallback to alternative models if needed

### 3. Text Generation
Tests three different prompts:
- "What is artificial intelligence?"
- "Explain quantum computing in simple terms."
- "Write a short poem about technology."

Metrics tracked:
- Input/output token counts
- Generation time
- Tokens per second
- Memory usage per generation

### 4. Embedding Generation
Tests embedding extraction with Spanish e-commerce queries:
- "ropa para oficina"
- "zapatillas running"
- "vestidos elegantes"
- "camisa formal"

Metrics tracked:
- Embedding dimensions
- Generation speed
- Similarity calculations

### 5. Benchmark
5 iterations of the same prompt to measure:
- Average generation time
- Standard deviation
- Average tokens per second
- Min/max times

## Expected Performance (CPU)

### System Requirements
- **Minimum RAM**: 8 GB
- **Recommended RAM**: 16 GB
- **Disk Space**: 10 GB (for model storage)
- **CPU**: Modern multi-core processor (4+ cores recommended)

### Typical Performance Metrics
- **Model Load Time**: 30-60 seconds
- **Generation Speed**: 2-10 tokens/second (CPU dependent)
- **Memory Usage**: 4-6 GB for model + overhead
- **Embedding Speed**: 0.5-2 embeddings/second

*Note: CPU performance is significantly slower than GPU (20-50x slower)*

## Output Example

```
================================================================================
GEMMA 3 1B CPU TEST
================================================================================

================================================================================
SYSTEM RESOURCES
================================================================================
CPU Cores: 8
CPU Usage: 15.2%
Total RAM: 16.00 GB
Available RAM: 8.45 GB
Used RAM: 7.55 GB (47.2%)
Disk Free: 125.34 GB

================================================================================
LOADING MODEL: google/gemma-2-2b-it
================================================================================
Device: cpu
PyTorch version: 2.1.0

Loading tokenizer...
✓ Tokenizer loaded

Loading model (this may take a few minutes)...
Using CPU - expect slower inference times
✓ Model loaded successfully
  Load time: 45.23 seconds
  Memory used: 4.52 GB
  Model parameters: 2.51B

================================================================================
TEXT GENERATION TEST
================================================================================

--- Test 1/3 ---
Prompt: What is artificial intelligence?

Generated: What is artificial intelligence? Artificial intelligence (AI) is the simulation of human intelligence processes by machines...

Metrics:
  Input tokens: 8
  Generated tokens: 45
  Time: 8.34s
  Speed: 5.40 tokens/sec
  Memory: 0.125 GB

...

================================================================================
TEST SUMMARY
================================================================================
Model: google/gemma-2-2b-it
Device: cpu
Parameters: 2.51B

Text Generation:
  Tests completed: 3
  Avg speed: 5.23 tokens/sec

Embedding Generation:
  Embedding dimension: 2048
  Speed: 0.85 embeddings/sec

Benchmark:
  Average time: 7.89s
  Average speed: 5.18 tokens/sec

✓ All tests completed
```

## Troubleshooting

### Model Download Fails

```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/large/disk
python test_gemma3_1b_cpu.py
```

### Out of Memory

If you see memory errors:
1. Close other applications
2. The script will try smaller fallback models automatically
3. Consider using a system with more RAM

### Slow Performance

CPU inference is inherently slower than GPU:
- **Expected on CPU**: 2-10 tokens/second
- **Expected on GPU**: 50-200 tokens/second

This is normal behavior and not a bug.

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Model Not Found

The script tries these models in order:
1. `google/gemma-2-2b-it` (instruction-tuned, 2B params)
2. `google/gemma-2-2b` (base model, 2B params)
3. `google/gemma-1.1-2b-it` (older version, 2B params)

If all fail, check:
- Internet connection
- HuggingFace hub status: https://status.huggingface.co/
- Your HuggingFace token (if using gated models)

## Advanced Usage

### Test with Custom Prompts

Edit the `test_prompts` list in `test_gemma3_1b_cpu.py`:

```python
test_prompts = [
    "Your custom prompt here",
    "Another prompt",
    "And another",
]
```

### Adjust Generation Parameters

Modify the `generate()` call parameters:

```python
outputs = self.model.generate(
    **inputs,
    max_length=200,        # Increase for longer outputs
    temperature=0.9,       # Higher = more creative (0.1-1.0)
    do_sample=True,        # Set False for deterministic output
    top_p=0.9,            # Nucleus sampling
    top_k=50,             # Top-k sampling
)
```

### Change Benchmark Iterations

```python
benchmark_results = tester.run_benchmark(num_iterations=10)  # More iterations
```

### Use Different Model

Change the model name in initialization:

```python
tester = Gemma3CPUTester(model_name="google/gemma-7b-it")  # Larger model
```

## Model Information

### Gemma 2 (2B) - Current Default
- **Parameters**: 2.5 billion
- **Context Length**: 8,192 tokens
- **Architecture**: Decoder-only transformer
- **Training**: Instruction-tuned variant available
- **License**: Gemma License (commercial use allowed)

### Why Gemma 2 instead of Gemma 3?

As of November 2024, Gemma 3 1B is not yet released. The script uses Gemma 2 2B as the closest alternative. When Gemma 3 1B becomes available, simply update the model name:

```python
tester = Gemma3CPUTester(model_name="google/gemma-3-1b")
```

## Integration with Main Project

This test script can be integrated with the existing embedding comparison framework:

1. **Add to embedding_tester.py**: Create a `GemmaEmbedding` class
2. **Use for product search**: Extract embeddings from hidden states
3. **Compare performance**: Benchmark against Jina and E5 models

See `embedding_tester.py` for the comparison framework structure.

## Performance Optimization Tips

### For CPU
1. **Use float32** (already configured)
2. **Set threads**: `torch.set_num_threads(8)`
3. **Enable MKL**: Install `mkl` package for Intel CPUs
4. **Reduce batch size**: Process fewer items at once
5. **Limit max_length**: Shorter generations are faster

### Example Optimizations

```python
import torch
torch.set_num_threads(8)  # Use 8 CPU threads
torch.set_num_interop_threads(2)  # Parallelism between ops

# Use in script before loading model
```

## References

- **Gemma Models**: https://huggingface.co/google
- **Gemma Documentation**: https://ai.google.dev/gemma
- **Transformers Docs**: https://huggingface.co/docs/transformers/
- **PyTorch CPU Performance**: https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html

## License

Same as main project (MIT License).

## Contributing

To improve this test script:
1. Add more comprehensive benchmarks
2. Test additional models
3. Add visualization of results
4. Implement model quantization for faster CPU inference
5. Add support for ONNX Runtime for better CPU performance
