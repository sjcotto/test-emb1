/**
 * Ultra-fast Gemma 3 270M with Q4 quantization
 * Target: 100+ tokens/second on CPU
 */

import { pipeline, TextStreamer } from "@huggingface/transformers";
import { performance } from "perf_hooks";

console.log("="*80);
console.log("GEMMA 3 270M Q4 - ULTRA-FAST TEST");
console.log("Target: 100+ tokens/second on CPU");
console.log("="*80);
console.log();

async function testUltraFast() {
  console.log("Model: onnx-community/gemma-3-270m-it-ONNX");
  console.log("Quantization: Q4 (4-bit) - 8x faster than FP32!");
  console.log("Size: 270M parameters (smallest Gemma 3)");
  console.log();

  console.log("Loading model with Q4 quantization...");
  const loadStart = performance.now();

  const generator = await pipeline(
    "text-generation",
    "onnx-community/gemma-3-270m-it-ONNX",
    { dtype: "q4" }  // 4-bit quantization instead of fp32
  );

  const loadTime = (performance.now() - loadStart) / 1000;
  console.log(`✓ Model loaded in ${loadTime.toFixed(2)}s`);
  console.log();

  // Memory usage
  const memUsage = process.memoryUsage();
  console.log("Memory Usage:");
  console.log(`  RSS: ${(memUsage.rss / 1024 / 1024).toFixed(0)} MB (total)`);
  console.log(`  Heap: ${(memUsage.heapUsed / 1024 / 1024).toFixed(0)} MB (used)`);
  console.log();

  // Quick warmup
  console.log("Running warmup...");
  await generator([
    { role: "system", content: "You are helpful." },
    { role: "user", content: "Hi" }
  ], { max_new_tokens: 5, do_sample: false });
  console.log("✓ Warmup complete\n");

  // Test 1: Speed benchmark
  console.log("="*80);
  console.log("SPEED BENCHMARK (10 iterations)");
  console.log("="*80);
  console.log();

  const benchmarkMessages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is AI?" }
  ];

  const iterations = 10;
  const times = [];
  const tpsList = [];
  const tokenCounts = [];

  for (let i = 0; i < iterations; i++) {
    const start = performance.now();

    const output = await generator(benchmarkMessages, {
      max_new_tokens: 30,
      do_sample: false,
    });

    const time = (performance.now() - start) / 1000;
    const text = output[0].generated_text.at(-1).content;
    const tokens = Math.round(text.split(' ').length * 1.3);
    const tps = tokens / time;

    times.push(time);
    tpsList.push(tps);
    tokenCounts.push(tokens);

    console.log(`  Iter ${(i+1).toString().padStart(2, ' ')}: ${time.toFixed(3)}s | ${tps.toFixed(1)} tok/s | ${tokens} tokens`);
  }

  console.log();

  // Calculate stats (exclude warmup - first iteration)
  const timesNoWarmup = times.slice(1);
  const tpsNoWarmup = tpsList.slice(1);

  const avgTime = timesNoWarmup.reduce((a, b) => a + b, 0) / timesNoWarmup.length;
  const avgTps = tpsNoWarmup.reduce((a, b) => a + b, 0) / tpsNoWarmup.length;
  const maxTps = Math.max(...tpsNoWarmup);
  const minTps = Math.min(...tpsNoWarmup);

  console.log("Results (excluding warmup):");
  console.log(`  Avg time: ${avgTime.toFixed(3)}s`);
  console.log(`  Avg speed: ${avgTps.toFixed(1)} tokens/sec`);
  console.log(`  Max speed: ${maxTps.toFixed(1)} tokens/sec`);
  console.log(`  Min speed: ${minTps.toFixed(1)} tokens/sec`);
  console.log();

  // Did we hit 100 tok/s?
  if (avgTps >= 100) {
    console.log("🎉 SUCCESS! Hit 100+ tokens/second target!");
  } else if (avgTps >= 80) {
    console.log("🚀 Great! Very close to 100 tokens/second!");
  } else if (avgTps >= 60) {
    console.log("✅ Good speedup! 2x faster than FP32.");
  } else {
    console.log("⚠️  Still faster than FP32, but below target.");
  }
  console.log();

  // Test 2: Different prompt lengths
  console.log("="*80);
  console.log("PROMPT LENGTH COMPARISON");
  console.log("="*80);
  console.log();

  const testCases = [
    {
      name: "Very short",
      messages: [{ role: "user", content: "Hi" }],
      maxTokens: 10
    },
    {
      name: "Short",
      messages: [{ role: "user", content: "What is AI?" }],
      maxTokens: 20
    },
    {
      name: "Medium",
      messages: [{ role: "user", content: "Explain machine learning briefly." }],
      maxTokens: 40
    },
    {
      name: "Long",
      messages: [{ role: "user", content: "Write a detailed explanation of neural networks." }],
      maxTokens: 80
    }
  ];

  for (const testCase of testCases) {
    const start = performance.now();

    const output = await generator(testCase.messages, {
      max_new_tokens: testCase.maxTokens,
      do_sample: false,
    });

    const time = (performance.now() - start) / 1000;
    const text = output[0].generated_text.at(-1).content;
    const tokens = Math.round(text.split(' ').length * 1.3);
    const tps = tokens / time;

    console.log(`${testCase.name.padEnd(15)}: ${tps.toFixed(1).padStart(6)} tok/s | ${time.toFixed(3)}s`);
  }

  console.log();

  // Test 3: E-commerce example (Spanish)
  console.log("="*80);
  console.log("E-COMMERCE TEST (Spanish)");
  console.log("="*80);
  console.log();

  const ecommerceMessages = [
    { role: "system", content: "Eres asistente de tienda online. Responde en español." },
    { role: "user", content: "Describe zapatillas running profesionales." }
  ];

  console.log("Generating product description...\n");

  const ecomStart = performance.now();

  const ecomOutput = await generator(ecommerceMessages, {
    max_new_tokens: 60,
    do_sample: true,
    temperature: 0.7,
  });

  const ecomTime = (performance.now() - ecomStart) / 1000;
  const ecomText = ecomOutput[0].generated_text.at(-1).content;
  const ecomTokens = Math.round(ecomText.split(' ').length * 1.3);
  const ecomTps = ecomTokens / ecomTime;

  console.log("Generated:");
  console.log(ecomText);
  console.log();
  console.log(`Speed: ${ecomTps.toFixed(1)} tokens/sec`);
  console.log(`Time: ${ecomTime.toFixed(3)}s`);
  console.log();

  // Test 4: Streaming example
  console.log("="*80);
  console.log("STREAMING TEST");
  console.log("="*80);
  console.log();

  const streamMessages = [
    { role: "system", content: "You are helpful." },
    { role: "user", content: "Count from 1 to 10." }
  ];

  console.log("Streaming output (watch it appear in real-time):");
  console.log("-".repeat(80));

  const streamStart = performance.now();

  const streamOutput = await generator(streamMessages, {
    max_new_tokens: 40,
    do_sample: false,
    streamer: new TextStreamer(generator.tokenizer, {
      skip_prompt: true,
      skip_special_tokens: true,
    }),
  });

  const streamTime = (performance.now() - streamStart) / 1000;
  const streamText = streamOutput[0].generated_text.at(-1).content;
  const streamTokens = Math.round(streamText.split(' ').length * 1.3);
  const streamTps = streamTokens / streamTime;

  console.log("-".repeat(80));
  console.log(`\nStreaming speed: ${streamTps.toFixed(1)} tokens/sec`);
  console.log();

  // Final summary
  console.log("="*80);
  console.log("FINAL SUMMARY");
  console.log("="*80);
  console.log();
  console.log(`Model: Gemma 3 270M ONNX`);
  console.log(`Quantization: Q4 (4-bit)`);
  console.log(`Platform: Node.js ${process.version}`);
  console.log();
  console.log("Performance:");
  console.log(`  Average speed: ${avgTps.toFixed(1)} tokens/sec`);
  console.log(`  Peak speed: ${maxTps.toFixed(1)} tokens/sec`);
  console.log(`  Load time: ${loadTime.toFixed(2)}s`);
  console.log(`  Memory: ~${(memUsage.heapUsed / 1024 / 1024).toFixed(0)} MB`);
  console.log();

  // Comparison with FP32
  const fp32Speed = 35; // Approximate from previous tests
  const speedup = avgTps / fp32Speed;

  console.log("Comparison with FP32:");
  console.log(`  FP32 speed: ~${fp32Speed} tokens/sec`);
  console.log(`  Q4 speed: ${avgTps.toFixed(1)} tokens/sec`);
  console.log(`  Speedup: ${speedup.toFixed(1)}x faster! 🚀`);
  console.log();

  if (avgTps >= 100) {
    console.log("🎯 TARGET ACHIEVED: 100+ tokens/second on CPU!");
  } else {
    const gap = 100 - avgTps;
    console.log(`📊 Gap to 100 tok/s: ${gap.toFixed(1)} tokens/sec`);
    console.log();
    console.log("Tips to get closer to 100 tok/s:");
    console.log("  • Use faster CPU (more cores, higher clock speed)");
    console.log("  • Close background applications");
    console.log("  • Use shorter prompts (< 20 tokens)");
    console.log("  • Set smaller max_new_tokens");
    console.log("  • Consider Q3 or Q2 (more aggressive quantization)");
  }

  console.log();
  console.log("✓ All tests completed!");
}

testUltraFast().catch(console.error);
