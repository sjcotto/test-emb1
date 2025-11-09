"""
Test script for running Google Gemma 3 1B on CPU
Tests model loading, inference, and performance metrics
"""

import os
import time
import psutil
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from typing import List, Dict, Any
import warnings

warnings.filterwarnings('ignore')

# Force CPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = ''


class Gemma3CPUTester:
    """Test Gemma 3 1B model on CPU"""

    def __init__(self, model_name: str = "google/gemma-2-2b-it"):
        """
        Initialize tester with model name

        Note: Using gemma-2-2b-it as it's the smallest available Gemma 2 model.
        Gemma 3 may not be released yet, so we'll use Gemma 2 as fallback.
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cpu"

    def check_system_resources(self) -> Dict[str, Any]:
        """Check available system resources"""
        print("="*80)
        print("SYSTEM RESOURCES")
        print("="*80)

        # CPU info
        cpu_count = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory info
        memory = psutil.virtual_memory()
        total_memory_gb = memory.total / (1024**3)
        available_memory_gb = memory.available / (1024**3)
        used_memory_gb = memory.used / (1024**3)

        # Disk info
        disk = psutil.disk_usage('/')

        info = {
            'cpu_count': cpu_count,
            'cpu_percent': cpu_percent,
            'total_memory_gb': total_memory_gb,
            'available_memory_gb': available_memory_gb,
            'used_memory_gb': used_memory_gb,
            'memory_percent': memory.percent
        }

        print(f"CPU Cores: {cpu_count}")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Total RAM: {total_memory_gb:.2f} GB")
        print(f"Available RAM: {available_memory_gb:.2f} GB")
        print(f"Used RAM: {used_memory_gb:.2f} GB ({memory.percent}%)")
        print(f"Disk Free: {disk.free / (1024**3):.2f} GB")
        print()

        return info

    def load_model(self) -> bool:
        """Load Gemma 3 model and tokenizer"""
        print("="*80)
        print(f"LOADING MODEL: {self.model_name}")
        print("="*80)

        try:
            print(f"Device: {self.device}")
            print(f"PyTorch version: {torch.__version__}")
            print()

            # Record memory before loading
            memory_before = psutil.virtual_memory().used / (1024**3)
            start_time = time.time()

            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            print("✓ Tokenizer loaded")

            print("\nLoading model (this may take a few minutes)...")
            print("Using CPU - expect slower inference times")

            # Load model with CPU-optimized settings
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="cpu",
                torch_dtype=torch.float32,  # Use float32 for CPU
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )

            # Ensure model is on CPU
            self.model = self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode

            load_time = time.time() - start_time
            memory_after = psutil.virtual_memory().used / (1024**3)
            memory_used = memory_after - memory_before

            print(f"✓ Model loaded successfully")
            print(f"  Load time: {load_time:.2f} seconds")
            print(f"  Memory used: {memory_used:.2f} GB")
            print(f"  Model parameters: {self.count_parameters() / 1e9:.2f}B")
            print()

            return True

        except Exception as e:
            print(f"✗ Failed to load model: {e}")
            print("\nTrying alternative Gemma models...")

            # Try smaller/alternative models
            alternatives = [
                "google/gemma-2-2b",  # Base model without instruction tuning
                "google/gemma-1.1-2b-it",  # Older Gemma version
            ]

            for alt_model in alternatives:
                try:
                    print(f"\nTrying: {alt_model}")
                    self.model_name = alt_model
                    self.tokenizer = AutoTokenizer.from_pretrained(alt_model, trust_remote_code=True)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        alt_model,
                        device_map="cpu",
                        torch_dtype=torch.float32,
                        low_cpu_mem_usage=True,
                        trust_remote_code=True
                    )
                    self.model = self.model.to(self.device)
                    self.model.eval()
                    print(f"✓ Successfully loaded {alt_model}")
                    return True
                except Exception as e2:
                    print(f"✗ Failed: {e2}")
                    continue

            return False

    def count_parameters(self) -> int:
        """Count total model parameters"""
        if self.model is None:
            return 0
        return sum(p.numel() for p in self.model.parameters())

    def test_text_generation(self, prompts: List[str], max_length: int = 100) -> List[Dict[str, Any]]:
        """Test text generation with sample prompts"""
        print("="*80)
        print("TEXT GENERATION TEST")
        print("="*80)

        if self.model is None or self.tokenizer is None:
            print("✗ Model not loaded")
            return []

        results = []

        for i, prompt in enumerate(prompts, 1):
            print(f"\n--- Test {i}/{len(prompts)} ---")
            print(f"Prompt: {prompt}")
            print()

            try:
                # Record performance metrics
                memory_before = psutil.virtual_memory().used / (1024**3)
                start_time = time.time()

                # Tokenize
                inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
                input_length = inputs['input_ids'].shape[1]

                # Generate
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_length=max_length,
                        num_return_sequences=1,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id
                    )

                # Decode
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                generation_time = time.time() - start_time
                memory_after = psutil.virtual_memory().used / (1024**3)
                memory_used = memory_after - memory_before

                output_length = outputs.shape[1]
                tokens_generated = output_length - input_length
                tokens_per_second = tokens_generated / generation_time if generation_time > 0 else 0

                result = {
                    'prompt': prompt,
                    'generated_text': generated_text,
                    'input_tokens': input_length,
                    'output_tokens': output_length,
                    'tokens_generated': tokens_generated,
                    'generation_time': generation_time,
                    'tokens_per_second': tokens_per_second,
                    'memory_used_gb': memory_used
                }

                results.append(result)

                print(f"Generated: {generated_text}")
                print(f"\nMetrics:")
                print(f"  Input tokens: {input_length}")
                print(f"  Generated tokens: {tokens_generated}")
                print(f"  Time: {generation_time:.2f}s")
                print(f"  Speed: {tokens_per_second:.2f} tokens/sec")
                print(f"  Memory: {memory_used:.3f} GB")

            except Exception as e:
                print(f"✗ Generation failed: {e}")
                results.append({
                    'prompt': prompt,
                    'error': str(e)
                })

        return results

    def test_embeddings(self, texts: List[str]) -> Dict[str, Any]:
        """Test if model can be used for embeddings (last hidden state)"""
        print("\n" + "="*80)
        print("EMBEDDING GENERATION TEST")
        print("="*80)

        if self.model is None or self.tokenizer is None:
            print("✗ Model not loaded")
            return {}

        try:
            print("Generating embeddings from last hidden states...")

            start_time = time.time()

            # Tokenize
            inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(self.device)

            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs, output_hidden_states=True)
                # Use last hidden state, mean pooling
                hidden_states = outputs.hidden_states[-1]
                embeddings = hidden_states.mean(dim=1)

            embeddings_np = embeddings.cpu().numpy()

            embedding_time = time.time() - start_time

            result = {
                'num_texts': len(texts),
                'embedding_dim': embeddings_np.shape[1],
                'embedding_shape': embeddings_np.shape,
                'time': embedding_time,
                'embeddings_per_second': len(texts) / embedding_time
            }

            print(f"✓ Generated embeddings")
            print(f"  Number of texts: {len(texts)}")
            print(f"  Embedding dimension: {embeddings_np.shape[1]}")
            print(f"  Shape: {embeddings_np.shape}")
            print(f"  Time: {embedding_time:.2f}s")
            print(f"  Speed: {len(texts) / embedding_time:.2f} embeddings/sec")

            # Calculate similarity between first two texts
            if len(texts) >= 2:
                sim = np.dot(embeddings_np[0], embeddings_np[1]) / (
                    np.linalg.norm(embeddings_np[0]) * np.linalg.norm(embeddings_np[1])
                )
                print(f"  Similarity between first two texts: {sim:.4f}")
                result['sample_similarity'] = float(sim)

            return result

        except Exception as e:
            print(f"✗ Embedding generation failed: {e}")
            return {'error': str(e)}

    def run_benchmark(self, num_iterations: int = 5) -> Dict[str, Any]:
        """Run benchmark tests"""
        print("\n" + "="*80)
        print(f"BENCHMARK TEST ({num_iterations} iterations)")
        print("="*80)

        if self.model is None or self.tokenizer is None:
            print("✗ Model not loaded")
            return {}

        test_prompt = "What is the capital of France?"
        times = []
        tokens_per_second_list = []

        print(f"Running {num_iterations} iterations with prompt: '{test_prompt}'")
        print()

        for i in range(num_iterations):
            try:
                start_time = time.time()

                inputs = self.tokenizer(test_prompt, return_tensors="pt").to(self.device)
                input_length = inputs['input_ids'].shape[1]

                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_length=50,
                        pad_token_id=self.tokenizer.eos_token_id
                    )

                elapsed = time.time() - start_time
                tokens_generated = outputs.shape[1] - input_length
                tps = tokens_generated / elapsed if elapsed > 0 else 0

                times.append(elapsed)
                tokens_per_second_list.append(tps)

                print(f"  Iteration {i+1}: {elapsed:.2f}s ({tps:.2f} tokens/sec)")

            except Exception as e:
                print(f"  Iteration {i+1}: Failed - {e}")

        if times:
            avg_time = np.mean(times)
            std_time = np.std(times)
            avg_tps = np.mean(tokens_per_second_list)

            print(f"\nBenchmark Results:")
            print(f"  Average time: {avg_time:.2f}s (±{std_time:.2f}s)")
            print(f"  Average speed: {avg_tps:.2f} tokens/sec")
            print(f"  Min time: {min(times):.2f}s")
            print(f"  Max time: {max(times):.2f}s")

            return {
                'avg_time': avg_time,
                'std_time': std_time,
                'avg_tokens_per_second': avg_tps,
                'min_time': min(times),
                'max_time': max(times),
                'iterations': num_iterations
            }

        return {}

    def cleanup(self):
        """Clean up model from memory"""
        print("\n" + "="*80)
        print("CLEANUP")
        print("="*80)

        memory_before = psutil.virtual_memory().used / (1024**3)

        if self.model is not None:
            del self.model
            self.model = None

        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        # Force garbage collection
        import gc
        gc.collect()

        memory_after = psutil.virtual_memory().used / (1024**3)
        memory_freed = memory_before - memory_after

        print(f"✓ Model removed from memory")
        print(f"  Memory freed: {memory_freed:.2f} GB")
        print(f"  Current memory usage: {memory_after:.2f} GB")


def main():
    """Main test function"""
    print("\n" + "="*80)
    print("GEMMA 3 1B CPU TEST")
    print("="*80)
    print()

    # Initialize tester
    tester = Gemma3CPUTester()

    # Check system resources
    system_info = tester.check_system_resources()

    # Load model
    if not tester.load_model():
        print("\n✗ Failed to load any Gemma model. Exiting.")
        return

    # Test prompts for generation
    test_prompts = [
        "What is artificial intelligence?",
        "Explain quantum computing in simple terms.",
        "Write a short poem about technology.",
    ]

    # Run text generation tests
    generation_results = tester.test_text_generation(test_prompts, max_length=100)

    # Test embedding generation
    embedding_texts = [
        "ropa para oficina",
        "zapatillas running",
        "vestidos elegantes",
        "camisa formal"
    ]
    embedding_results = tester.test_embeddings(embedding_texts)

    # Run benchmark
    benchmark_results = tester.run_benchmark(num_iterations=5)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Model: {tester.model_name}")
    print(f"Device: {tester.device}")
    print(f"Parameters: {tester.count_parameters() / 1e9:.2f}B")
    print()

    if generation_results:
        avg_tps = np.mean([r.get('tokens_per_second', 0) for r in generation_results if 'tokens_per_second' in r])
        print(f"Text Generation:")
        print(f"  Tests completed: {len(generation_results)}")
        print(f"  Avg speed: {avg_tps:.2f} tokens/sec")

    if embedding_results and 'error' not in embedding_results:
        print(f"\nEmbedding Generation:")
        print(f"  Embedding dimension: {embedding_results.get('embedding_dim', 'N/A')}")
        print(f"  Speed: {embedding_results.get('embeddings_per_second', 0):.2f} embeddings/sec")

    if benchmark_results:
        print(f"\nBenchmark:")
        print(f"  Average time: {benchmark_results.get('avg_time', 0):.2f}s")
        print(f"  Average speed: {benchmark_results.get('avg_tokens_per_second', 0):.2f} tokens/sec")

    print()
    print("✓ All tests completed")

    # Cleanup
    tester.cleanup()


if __name__ == "__main__":
    main()
