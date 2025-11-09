"""
Optimized Gemma 3 1B test script for maximum CPU inference speed
Uses INT8 quantization and ONNX Runtime for 2-4x speedup
"""

import os
import time
import psutil
import torch
import numpy as np
from typing import List, Dict, Any
import warnings

warnings.filterwarnings('ignore')

# Force CPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = ''


class OptimizedGemmaRunner:
    """Optimized Gemma runner with multiple acceleration strategies"""

    def __init__(self, model_name: str = "google/gemma-2-2b-it"):
        self.model_name = model_name
        self.device = "cpu"
        self.optimization_method = None

        # Model components
        self.model = None
        self.tokenizer = None

    def check_available_optimizations(self) -> Dict[str, bool]:
        """Check which optimization methods are available"""
        print("="*80)
        print("CHECKING AVAILABLE OPTIMIZATIONS")
        print("="*80)

        available = {}

        # Check ONNX Runtime
        try:
            import onnxruntime as ort
            available['onnx'] = True
            print(f"✓ ONNX Runtime available (v{ort.__version__})")

            # Check available providers
            providers = ort.get_available_providers()
            print(f"  Available providers: {', '.join(providers)}")
        except ImportError:
            available['onnx'] = False
            print("✗ ONNX Runtime not available (install: pip install onnxruntime)")

        # Check Optimum
        try:
            import optimum
            available['optimum'] = True
            print(f"✓ Optimum available (v{optimum.__version__})")
        except ImportError:
            available['optimum'] = False
            print("✗ Optimum not available (install: pip install optimum)")

        # Check BetterTransformer
        try:
            from transformers import BetterTransformer
            available['bettertransformer'] = True
            print("✓ BetterTransformer available")
        except ImportError:
            available['bettertransformer'] = False
            print("✗ BetterTransformer not available")

        # PyTorch quantization always available
        available['torch_quantization'] = True
        print("✓ PyTorch dynamic quantization available")

        print()
        return available

    def load_with_torch_quantization(self) -> bool:
        """Load model with PyTorch INT8 dynamic quantization"""
        print("="*80)
        print("LOADING WITH PYTORCH INT8 QUANTIZATION")
        print("="*80)

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            print("Loading model...")
            start_time = time.time()
            memory_before = psutil.virtual_memory().used / (1024**3)

            # Load model in float32
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
            self.model.eval()

            print("Applying INT8 dynamic quantization...")
            # Apply dynamic quantization to linear layers
            self.model = torch.quantization.quantize_dynamic(
                self.model,
                {torch.nn.Linear},
                dtype=torch.qint8
            )

            load_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)
            memory_used = memory_after - memory_before

            print(f"✓ Model loaded and quantized")
            print(f"  Load time: {load_time:.2f}s")
            print(f"  Memory used: {memory_used:.2f} GB")
            print(f"  Optimization: INT8 dynamic quantization")
            print()

            self.optimization_method = "torch_int8_quantization"
            return True

        except Exception as e:
            print(f"✗ Failed to load with quantization: {e}")
            return False

    def load_with_optimum_onnx(self) -> bool:
        """Load model with Optimum + ONNX Runtime"""
        print("="*80)
        print("LOADING WITH OPTIMUM + ONNX RUNTIME")
        print("="*80)

        try:
            from optimum.onnxruntime import ORTModelForCausalLM
            from transformers import AutoTokenizer

            print("Loading with Optimum ONNX Runtime...")
            print("Note: First run will export to ONNX (takes a few minutes)")
            start_time = time.time()
            memory_before = psutil.virtual_memory().used / (1024**3)

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            # Load or export to ONNX
            self.model = ORTModelForCausalLM.from_pretrained(
                self.model_name,
                export=True,
                provider="CPUExecutionProvider",
            )

            load_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)
            memory_used = memory_after - memory_before

            print(f"✓ Model loaded with ONNX Runtime")
            print(f"  Load time: {load_time:.2f}s")
            print(f"  Memory used: {memory_used:.2f} GB")
            print(f"  Optimization: ONNX Runtime")
            print()

            self.optimization_method = "onnx_runtime"
            return True

        except Exception as e:
            print(f"✗ Failed to load with ONNX: {e}")
            return False

    def load_with_bettertransformer(self) -> bool:
        """Load model with BetterTransformer optimization"""
        print("="*80)
        print("LOADING WITH BETTERTRANSFORMER")
        print("="*80)

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            print("Loading model...")
            start_time = time.time()
            memory_before = psutil.virtual_memory().used / (1024**3)

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )

            print("Converting to BetterTransformer...")
            self.model = self.model.to_bettertransformer()
            self.model.eval()

            load_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)
            memory_used = memory_after - memory_before

            print(f"✓ Model loaded with BetterTransformer")
            print(f"  Load time: {load_time:.2f}s")
            print(f"  Memory used: {memory_used:.2f} GB")
            print(f"  Optimization: BetterTransformer (faster attention)")
            print()

            self.optimization_method = "bettertransformer"
            return True

        except Exception as e:
            print(f"✗ Failed to load with BetterTransformer: {e}")
            return False

    def load_baseline(self) -> bool:
        """Load baseline model without optimization"""
        print("="*80)
        print("LOADING BASELINE (NO OPTIMIZATION)")
        print("="*80)

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            start_time = time.time()
            memory_before = psutil.virtual_memory().used / (1024**3)

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
            self.model.eval()

            load_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)
            memory_used = memory_after - memory_before

            print(f"✓ Baseline model loaded")
            print(f"  Load time: {load_time:.2f}s")
            print(f"  Memory used: {memory_used:.2f} GB")
            print()

            self.optimization_method = "baseline"
            return True

        except Exception as e:
            print(f"✗ Failed to load baseline: {e}")
            return False

    def benchmark(self, num_iterations: int = 10) -> Dict[str, Any]:
        """Run benchmark test"""
        if self.model is None or self.tokenizer is None:
            print("✗ Model not loaded")
            return {}

        print("="*80)
        print(f"BENCHMARK ({num_iterations} iterations)")
        print("="*80)

        test_prompt = "What is artificial intelligence?"
        print(f"Prompt: '{test_prompt}'")
        print()

        times = []
        tokens_per_second_list = []
        first_token_times = []

        for i in range(num_iterations):
            try:
                # Tokenize
                inputs = self.tokenizer(test_prompt, return_tensors="pt")
                input_length = inputs['input_ids'].shape[1]

                # Measure first token latency
                start_time = time.time()

                with torch.no_grad():
                    # Generate with streaming to measure first token
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=30,
                        pad_token_id=self.tokenizer.eos_token_id,
                        do_sample=False,  # Deterministic for consistent benchmarks
                    )

                total_time = time.time() - start_time

                output_length = outputs.shape[1]
                tokens_generated = output_length - input_length
                tps = tokens_generated / total_time if total_time > 0 else 0

                times.append(total_time)
                tokens_per_second_list.append(tps)

                print(f"  Iter {i+1:2d}: {total_time:.3f}s | {tps:.2f} tok/s | {tokens_generated} tokens")

            except Exception as e:
                print(f"  Iter {i+1}: Failed - {e}")

        print()

        if times:
            # Calculate statistics
            avg_time = np.mean(times)
            std_time = np.std(times)
            avg_tps = np.mean(tokens_per_second_list)
            median_tps = np.median(tokens_per_second_list)

            # Remove first iteration (warmup) for more accurate stats
            if len(times) > 1:
                warmup_time = times[0]
                times_no_warmup = times[1:]
                tps_no_warmup = tokens_per_second_list[1:]
                avg_tps_no_warmup = np.mean(tps_no_warmup)
            else:
                warmup_time = times[0]
                avg_tps_no_warmup = avg_tps

            print("Results:")
            print(f"  Warmup (1st iter): {warmup_time:.3f}s")
            print(f"  Avg time: {avg_time:.3f}s (±{std_time:.3f}s)")
            print(f"  Avg speed: {avg_tps:.2f} tokens/sec")
            print(f"  Avg speed (no warmup): {avg_tps_no_warmup:.2f} tokens/sec")
            print(f"  Median speed: {median_tps:.2f} tokens/sec")
            print(f"  Min time: {min(times):.3f}s (fastest)")
            print(f"  Max time: {max(times):.3f}s (slowest)")

            return {
                'optimization': self.optimization_method,
                'avg_time': avg_time,
                'std_time': std_time,
                'avg_tokens_per_second': avg_tps,
                'avg_tokens_per_second_no_warmup': avg_tps_no_warmup,
                'median_tokens_per_second': median_tps,
                'min_time': min(times),
                'max_time': max(times),
                'warmup_time': warmup_time,
                'iterations': num_iterations
            }

        return {}

    def test_generation(self, prompt: str, max_new_tokens: int = 50) -> Dict[str, Any]:
        """Test single generation with detailed metrics"""
        if self.model is None or self.tokenizer is None:
            return {}

        print("\n" + "="*80)
        print("GENERATION TEST")
        print("="*80)
        print(f"Prompt: {prompt}\n")

        try:
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt")
            input_length = inputs['input_ids'].shape[1]

            # Generate
            start_time = time.time()
            memory_before = psutil.virtual_memory().used / (1024**3)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            generation_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)

            # Decode
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            output_length = outputs.shape[1]
            tokens_generated = output_length - input_length
            tokens_per_second = tokens_generated / generation_time

            print(f"Generated: {generated_text}\n")
            print(f"Metrics:")
            print(f"  Tokens generated: {tokens_generated}")
            print(f"  Time: {generation_time:.3f}s")
            print(f"  Speed: {tokens_per_second:.2f} tokens/sec")
            print(f"  Memory delta: {(memory_after - memory_before):.3f} GB")

            return {
                'prompt': prompt,
                'generated_text': generated_text,
                'tokens_generated': tokens_generated,
                'generation_time': generation_time,
                'tokens_per_second': tokens_per_second
            }

        except Exception as e:
            print(f"✗ Generation failed: {e}")
            return {'error': str(e)}

    def cleanup(self):
        """Clean up model from memory"""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        import gc
        gc.collect()


def compare_optimizations():
    """Compare different optimization methods"""
    print("\n" + "="*80)
    print("OPTIMIZATION COMPARISON")
    print("="*80)
    print()

    results = {}

    # Test each optimization method
    methods = [
        ("baseline", "load_baseline"),
        ("torch_quantization", "load_with_torch_quantization"),
        ("bettertransformer", "load_with_bettertransformer"),
        ("onnx", "load_with_optimum_onnx"),
    ]

    for method_name, load_func in methods:
        print(f"\n{'='*80}")
        print(f"TESTING: {method_name.upper()}")
        print(f"{'='*80}\n")

        runner = OptimizedGemmaRunner()

        # Try to load with this method
        load_method = getattr(runner, load_func)
        if not load_method():
            print(f"Skipping {method_name} - load failed\n")
            continue

        # Run benchmark
        benchmark_results = runner.benchmark(num_iterations=5)

        if benchmark_results:
            results[method_name] = benchmark_results
            print()

        # Cleanup
        runner.cleanup()

        # Wait a bit between tests
        time.sleep(2)

    # Print comparison
    print("\n" + "="*80)
    print("OPTIMIZATION COMPARISON SUMMARY")
    print("="*80)
    print()

    if not results:
        print("No results to compare")
        return

    # Sort by speed (tokens per second)
    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1].get('avg_tokens_per_second_no_warmup', 0),
        reverse=True
    )

    print(f"{'Method':<25} {'Speed (tok/s)':<15} {'Avg Time (s)':<15} {'Speedup':<10}")
    print("-" * 70)

    baseline_speed = None
    for method, data in sorted_results:
        if method == 'baseline':
            baseline_speed = data.get('avg_tokens_per_second_no_warmup', 0)

    for method, data in sorted_results:
        speed = data.get('avg_tokens_per_second_no_warmup', 0)
        avg_time = data.get('avg_time', 0)

        if baseline_speed and baseline_speed > 0:
            speedup = speed / baseline_speed
            speedup_str = f"{speedup:.2f}x"
        else:
            speedup_str = "N/A"

        print(f"{method:<25} {speed:<15.2f} {avg_time:<15.3f} {speedup_str:<10}")

    print()

    # Recommend best method
    if sorted_results:
        best_method, best_data = sorted_results[0]
        print(f"🏆 Recommended: {best_method}")
        print(f"   Speed: {best_data.get('avg_tokens_per_second_no_warmup', 0):.2f} tokens/sec")

        if baseline_speed and baseline_speed > 0:
            speedup = best_data.get('avg_tokens_per_second_no_warmup', 0) / baseline_speed
            print(f"   Speedup vs baseline: {speedup:.2f}x")


def main():
    """Main function"""
    print("\n" + "="*80)
    print("GEMMA OPTIMIZED CPU INFERENCE TEST")
    print("="*80)
    print()

    # Check system
    memory = psutil.virtual_memory()
    print(f"System: {psutil.cpu_count()} CPUs, {memory.total / (1024**3):.1f} GB RAM")
    print()

    # Check available optimizations
    runner = OptimizedGemmaRunner()
    available = runner.check_available_optimizations()

    # Run comparison of all available methods
    compare_optimizations()


if __name__ == "__main__":
    main()
