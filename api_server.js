/**
 * Express API server for Gemma 3 270M ONNX inference
 * Fast CPU inference with REST API endpoints
 */

import express from 'express';
import cors from 'cors';
import { pipeline } from '@huggingface/transformers';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Global model instance (loaded once at startup)
let generator = null;
let modelLoaded = false;
let loadingStartTime = null;
let modelLoadTime = null;

// Load model at startup
async function loadModel() {
  console.log('='*80);
  console.log('GEMMA 3 270M ONNX API SERVER');
  console.log('='*80);
  console.log();
  console.log('Loading model: onnx-community/gemma-3-270m-it-ONNX');
  console.log('Please wait, this may take 1-2 minutes...');
  console.log();

  loadingStartTime = Date.now();

  try {
    generator = await pipeline(
      'text-generation',
      'onnx-community/gemma-3-270m-it-ONNX',
      { dtype: 'fp32' }
    );

    modelLoadTime = (Date.now() - loadingStartTime) / 1000;
    modelLoaded = true;

    console.log(`✓ Model loaded successfully in ${modelLoadTime.toFixed(2)}s`);
    console.log(`✓ API server ready on http://localhost:${PORT}`);
    console.log();
    console.log('Available endpoints:');
    console.log(`  GET  /health         - Check server health`);
    console.log(`  GET  /model/info     - Get model information`);
    console.log(`  POST /generate       - Generate text`);
    console.log(`  POST /chat           - Chat completion`);
    console.log(`  POST /benchmark      - Run benchmark`);
    console.log();
  } catch (error) {
    console.error('✗ Failed to load model:', error);
    process.exit(1);
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    modelLoaded,
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage(),
  });
});

// Model info endpoint
app.get('/model/info', (req, res) => {
  res.json({
    name: 'Gemma 3 270M ONNX',
    modelId: 'onnx-community/gemma-3-270m-it-ONNX',
    parameters: '270M',
    format: 'ONNX fp32',
    platform: 'Node.js',
    nodeVersion: process.version,
    loaded: modelLoaded,
    loadTime: modelLoadTime ? `${modelLoadTime.toFixed(2)}s` : null,
  });
});

// Text generation endpoint
app.post('/generate', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({
      error: 'Model not loaded yet',
      message: 'Please wait for model to finish loading',
    });
  }

  try {
    const { prompt, maxTokens = 100, temperature = 0.7, system = 'You are a helpful assistant.' } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    const messages = [
      { role: 'system', content: system },
      { role: 'user', content: prompt },
    ];

    const startTime = Date.now();

    const output = await generator(messages, {
      max_new_tokens: maxTokens,
      do_sample: temperature > 0,
      temperature: temperature,
    });

    const inferenceTime = (Date.now() - startTime) / 1000;
    const generatedText = output[0].generated_text.at(-1).content;
    const roughTokens = Math.round(generatedText.split(' ').length * 1.3);
    const tokensPerSecond = roughTokens / inferenceTime;

    res.json({
      success: true,
      generated: generatedText,
      metrics: {
        inferenceTime: `${inferenceTime.toFixed(3)}s`,
        tokensPerSecond: tokensPerSecond.toFixed(1),
        roughTokenCount: roughTokens,
      },
      params: {
        maxTokens,
        temperature,
      },
    });
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({
      error: 'Generation failed',
      message: error.message,
    });
  }
});

// Chat completion endpoint (for multi-turn conversations)
app.post('/chat', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({
      error: 'Model not loaded yet',
    });
  }

  try {
    const { messages, maxTokens = 100, temperature = 0.7 } = req.body;

    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'Messages array is required' });
    }

    const startTime = Date.now();

    const output = await generator(messages, {
      max_new_tokens: maxTokens,
      do_sample: temperature > 0,
      temperature: temperature,
    });

    const inferenceTime = (Date.now() - startTime) / 1000;
    const generatedText = output[0].generated_text.at(-1).content;
    const roughTokens = Math.round(generatedText.split(' ').length * 1.3);
    const tokensPerSecond = roughTokens / inferenceTime;

    res.json({
      success: true,
      message: {
        role: 'assistant',
        content: generatedText,
      },
      metrics: {
        inferenceTime: `${inferenceTime.toFixed(3)}s`,
        tokensPerSecond: tokensPerSecond.toFixed(1),
        roughTokenCount: roughTokens,
      },
    });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({
      error: 'Chat failed',
      message: error.message,
    });
  }
});

// Benchmark endpoint
app.post('/benchmark', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({ error: 'Model not loaded yet' });
  }

  try {
    const { iterations = 5 } = req.body;

    const benchmarkMessages = [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'What is artificial intelligence?' },
    ];

    const times = [];
    const tokensPerSecondList = [];

    console.log(`Running benchmark (${iterations} iterations)...`);

    for (let i = 0; i < iterations; i++) {
      const startTime = Date.now();

      const output = await generator(benchmarkMessages, {
        max_new_tokens: 30,
        do_sample: false,
      });

      const time = (Date.now() - startTime) / 1000;
      const generatedText = output[0].generated_text.at(-1).content;
      const tokens = Math.round(generatedText.split(' ').length * 1.3);
      const tps = tokens / time;

      times.push(time);
      tokensPerSecondList.push(tps);
    }

    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    const avgTps = tokensPerSecondList.reduce((a, b) => a + b, 0) / tokensPerSecondList.length;

    // Remove warmup
    const timesNoWarmup = times.slice(1);
    const tpsNoWarmup = tokensPerSecondList.slice(1);
    const avgTpsNoWarmup = tpsNoWarmup.reduce((a, b) => a + b, 0) / tpsNoWarmup.length;

    res.json({
      success: true,
      results: {
        iterations,
        warmupTime: `${times[0].toFixed(3)}s`,
        avgTime: `${avgTime.toFixed(3)}s`,
        avgSpeed: `${avgTps.toFixed(1)} tokens/sec`,
        avgSpeedNoWarmup: `${avgTpsNoWarmup.toFixed(1)} tokens/sec`,
        minTime: `${Math.min(...times).toFixed(3)}s`,
        maxTime: `${Math.max(...times).toFixed(3)}s`,
      },
      allTimes: times.map(t => `${t.toFixed(3)}s`),
      allSpeeds: tokensPerSecondList.map(s => `${s.toFixed(1)} tok/s`),
    });
  } catch (error) {
    console.error('Benchmark error:', error);
    res.status(500).json({
      error: 'Benchmark failed',
      message: error.message,
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    availableEndpoints: ['/health', '/model/info', '/generate', '/chat', '/benchmark'],
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Starting server on port ${PORT}...`);
  loadModel();
});
