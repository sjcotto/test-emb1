/**
 * Test Gemma 3 270M ONNX model with Node.js
 * Ultra-fast CPU inference with streaming support
 */

import { pipeline, TextStreamer } from "@huggingface/transformers";

console.log("="*80);
console.log("GEMMA 3 270M ONNX - NODE.JS TEST");
console.log("="*80);
console.log();

async function testGeneration() {
  console.log("Loading model: onnx-community/gemma-3-270m-it-ONNX");
  console.log("Model size: 270M parameters (ultra-lightweight!)");
  console.log("Format: ONNX fp32 (optimized for CPU)");
  console.log();

  const startLoad = Date.now();

  // Create a text generation pipeline
  const generator = await pipeline(
    "text-generation",
    "onnx-community/gemma-3-270m-it-ONNX",
    { dtype: "fp32" }
  );

  const loadTime = (Date.now() - startLoad) / 1000;
  console.log(`✓ Model loaded in ${loadTime.toFixed(2)}s`);
  console.log();

  // Test 1: Simple generation with streaming
  console.log("="*80);
  console.log("TEST 1: Text Generation with Streaming");
  console.log("="*80);
  console.log();

  const messages1 = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Write a short poem about machine learning." },
  ];

  console.log("Prompt: Write a short poem about machine learning.");
  console.log("\nGenerated text (streaming):");
  console.log("-".repeat(80));

  const start1 = Date.now();

  const output1 = await generator(messages1, {
    max_new_tokens: 100,
    do_sample: false,
    streamer: new TextStreamer(generator.tokenizer, {
      skip_prompt: true,
      skip_special_tokens: true,
    }),
  });

  const time1 = (Date.now() - start1) / 1000;
  const generatedText1 = output1[0].generated_text.at(-1).content;

  console.log("-".repeat(80));
  console.log(`\n✓ Generated ${generatedText1.split(' ').length} words in ${time1.toFixed(2)}s`);
  console.log();

  // Test 2: E-commerce query (Spanish)
  console.log("="*80);
  console.log("TEST 2: E-commerce Product Description (Spanish)");
  console.log("="*80);
  console.log();

  const messages2 = [
    { role: "system", content: "Eres un asistente de una tienda online. Responde en español." },
    { role: "user", content: "Describe zapatillas running profesionales." },
  ];

  console.log("Prompt: Describe zapatillas running profesionales.");
  console.log("\nGenerating...");

  const start2 = Date.now();

  const output2 = await generator(messages2, {
    max_new_tokens: 80,
    do_sample: false,
  });

  const time2 = (Date.now() - start2) / 1000;
  const generatedText2 = output2[0].generated_text.at(-1).content;

  console.log("\nGenerated:");
  console.log(generatedText2);
  console.log(`\n✓ Time: ${time2.toFixed(2)}s`);
  console.log();

  // Test 3: Benchmark (multiple runs)
  console.log("="*80);
  console.log("TEST 3: Benchmark (5 iterations)");
  console.log("="*80);
  console.log();

  const benchmarkMessages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is artificial intelligence?" },
  ];

  const times = [];
  const tokensPerSecondList = [];

  console.log("Running benchmark...\n");

  for (let i = 0; i < 5; i++) {
    const startBench = Date.now();

    const outputBench = await generator(benchmarkMessages, {
      max_new_tokens: 30,
      do_sample: false,
    });

    const timeBench = (Date.now() - startBench) / 1000;
    const generatedTextBench = outputBench[0].generated_text.at(-1).content;

    // Rough token count (words * 1.3)
    const tokens = Math.round(generatedTextBench.split(' ').length * 1.3);
    const tps = tokens / timeBench;

    times.push(timeBench);
    tokensPerSecondList.push(tps);

    console.log(`  Iteration ${i + 1}: ${timeBench.toFixed(3)}s | ${tps.toFixed(1)} tok/s | ${tokens} tokens`);
  }

  const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
  const avgTps = tokensPerSecondList.reduce((a, b) => a + b, 0) / tokensPerSecondList.length;
  const minTime = Math.min(...times);
  const maxTime = Math.max(...times);

  // Remove warmup (first iteration)
  const timesNoWarmup = times.slice(1);
  const tpsNoWarmup = tokensPerSecondList.slice(1);
  const avgTpsNoWarmup = tpsNoWarmup.reduce((a, b) => a + b, 0) / tpsNoWarmup.length;

  console.log("\nBenchmark Results:");
  console.log(`  Warmup (1st iter): ${times[0].toFixed(3)}s`);
  console.log(`  Avg time: ${avgTime.toFixed(3)}s`);
  console.log(`  Avg speed: ${avgTps.toFixed(1)} tokens/sec`);
  console.log(`  Avg speed (no warmup): ${avgTpsNoWarmup.toFixed(1)} tokens/sec`);
  console.log(`  Min time: ${minTime.toFixed(3)}s (fastest)`);
  console.log(`  Max time: ${maxTime.toFixed(3)}s (slowest)`);
  console.log();

  // Summary
  console.log("="*80);
  console.log("SUMMARY");
  console.log("="*80);
  console.log(`Model: Gemma 3 270M ONNX`);
  console.log(`Size: 270M parameters`);
  console.log(`Format: ONNX fp32`);
  console.log(`Platform: Node.js ${process.version}`);
  console.log(`Load time: ${loadTime.toFixed(2)}s`);
  console.log(`Avg speed: ${avgTpsNoWarmup.toFixed(1)} tokens/sec`);
  console.log();
  console.log("✓ All tests completed successfully!");
  console.log();
}

// Run tests
testGeneration().catch(console.error);
