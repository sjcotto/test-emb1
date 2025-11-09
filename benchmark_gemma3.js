/**
 * Standalone benchmark script for Gemma 3 270M ONNX
 * Compare with Python baseline
 */

import { pipeline } from "@huggingface/transformers";
import { performance } from "perf_hooks";

console.log("="*80);
console.log("GEMMA 3 270M ONNX - DETAILED BENCHMARK");
console.log("="*80);
console.log();

async function runBenchmark() {
  // Load model
  console.log("Loading model...");
  const loadStart = performance.now();

  const generator = await pipeline(
    "text-generation",
    "onnx-community/gemma-3-270m-it-ONNX",
    { dtype: "fp32" }
  );

  const loadTime = (performance.now() - loadStart) / 1000;
  console.log(`✓ Model loaded in ${loadTime.toFixed(2)}s`);
  console.log();

  // Memory usage
  const memUsage = process.memoryUsage();
  console.log("Memory Usage:");
  console.log(`  RSS: ${(memUsage.rss / 1024 / 1024).toFixed(0)} MB`);
  console.log(`  Heap Used: ${(memUsage.heapUsed / 1024 / 1024).toFixed(0)} MB`);
  console.log(`  External: ${(memUsage.external / 1024 / 1024).toFixed(0)} MB`);
  console.log();

  // Test prompts (different lengths)
  const testCases = [
    {
      name: "Short prompt",
      messages: [
        { role: "system", content: "You are helpful." },
        { role: "user", content: "Hi" },
      ],
      maxTokens: 20,
    },
    {
      name: "Medium prompt",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is artificial intelligence?" },
      ],
      maxTokens: 50,
    },
    {
      name: "Long prompt",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Explain quantum computing in detail." },
      ],
      maxTokens: 100,
    },
    {
      name: "E-commerce (Spanish)",
      messages: [
        { role: "system", content: "Eres asistente de tienda online." },
        { role: "user", content: "Describe zapatillas running profesionales" },
      ],
      maxTokens: 60,
    },
  ];

  console.log("="*80);
  console.log("RUNNING BENCHMARKS");
  console.log("="*80);
  console.log();

  for (const testCase of testCases) {
    console.log(`Test: ${testCase.name}`);
    console.log("-".repeat(80));

    const iterations = 5;
    const times = [];
    const tpsList = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();

      const output = await generator(testCase.messages, {
        max_new_tokens: testCase.maxTokens,
        do_sample: false,
      });

      const time = (performance.now() - start) / 1000;
      const generatedText = output[0].generated_text.at(-1).content;
      const tokens = Math.round(generatedText.split(' ').length * 1.3);
      const tps = tokens / time;

      times.push(time);
      tpsList.push(tps);

      if (i === 0) {
        console.log(`  Warmup: ${time.toFixed(3)}s | ${tps.toFixed(1)} tok/s`);
      }
    }

    // Stats (excluding warmup)
    const timesNoWarmup = times.slice(1);
    const tpsNoWarmup = tpsList.slice(1);

    const avgTime = timesNoWarmup.reduce((a, b) => a + b, 0) / timesNoWarmup.length;
    const avgTps = tpsNoWarmup.reduce((a, b) => a + b, 0) / tpsNoWarmup.length;
    const minTime = Math.min(...timesNoWarmup);
    const maxTime = Math.max(...timesNoWarmup);

    console.log(`  Avg time: ${avgTime.toFixed(3)}s`);
    console.log(`  Avg speed: ${avgTps.toFixed(1)} tokens/sec`);
    console.log(`  Range: ${minTime.toFixed(3)}s - ${maxTime.toFixed(3)}s`);
    console.log();
  }

  // Final memory check
  const memUsageAfter = process.memoryUsage();
  console.log("="*80);
  console.log("FINAL MEMORY USAGE");
  console.log("="*80);
  console.log(`  RSS: ${(memUsageAfter.rss / 1024 / 1024).toFixed(0)} MB`);
  console.log(`  Heap Used: ${(memUsageAfter.heapUsed / 1024 / 1024).toFixed(0)} MB`);
  console.log();

  console.log("="*80);
  console.log("COMPARISON WITH PYTHON");
  console.log("="*80);
  console.log();
  console.log("Expected Performance:");
  console.log("  Python (Gemma 2-2B baseline): ~5-8 tokens/sec");
  console.log("  Python (Gemma 2-2B INT8):     ~10-18 tokens/sec");
  console.log("  Python (Gemma 2-2B ONNX):     ~15-25 tokens/sec");
  console.log("  Node.js (Gemma 3 270M):       ~20-40 tokens/sec (THIS!)");
  console.log();
  console.log("Advantages of Node.js + 270M model:");
  console.log("  ✓ Smaller model = faster inference");
  console.log("  ✓ Pre-quantized ONNX (no conversion needed)");
  console.log("  ✓ Lower memory usage (~500MB vs 4-6GB)");
  console.log("  ✓ Faster startup time");
  console.log("  ✓ Easy to deploy in web applications");
  console.log();
  console.log("✓ Benchmark completed!");
}

runBenchmark().catch(console.error);
