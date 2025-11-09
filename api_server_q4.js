/**
 * Ultra-fast API server with Gemma 3 270M Q4
 * Target: 100+ tokens/second on CPU
 */

import express from 'express';
import cors from 'cors';
import { pipeline } from '@huggingface/transformers';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

let generator = null;
let modelLoaded = false;
let modelLoadTime = null;

async function loadModel() {
  console.log('='*80);
  console.log('ULTRA-FAST GEMMA 3 270M Q4 API');
  console.log('Target: 100+ tokens/second');
  console.log('='*80);
  console.log();
  console.log('Loading model with Q4 quantization...');

  const startTime = Date.now();

  try {
    generator = await pipeline(
      'text-generation',
      'onnx-community/gemma-3-270m-it-ONNX',
      { dtype: 'q4' }  // 4-bit quantization for maximum speed
    );

    modelLoadTime = (Date.now() - startTime) / 1000;
    modelLoaded = true;

    console.log(`✓ Model loaded in ${modelLoadTime.toFixed(2)}s`);
    console.log(`✓ Using Q4 (4-bit) quantization - 8x faster than FP32!`);
    console.log(`✓ API server ready on http://localhost:${PORT}`);
    console.log();
    console.log('Endpoints:');
    console.log('  GET  /health');
    console.log('  GET  /model/info');
    console.log('  POST /generate');
    console.log('  POST /chat');
    console.log('  POST /benchmark');
    console.log();
  } catch (error) {
    console.error('✗ Failed to load model:', error);
    process.exit(1);
  }
}

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    modelLoaded,
    uptime: process.uptime(),
    memory: {
      rss: `${(process.memoryUsage().rss / 1024 / 1024).toFixed(0)} MB`,
      heapUsed: `${(process.memoryUsage().heapUsed / 1024 / 1024).toFixed(0)} MB`,
    }
  });
});

app.get('/model/info', (req, res) => {
  res.json({
    name: 'Gemma 3 270M Q4',
    modelId: 'onnx-community/gemma-3-270m-it-ONNX',
    parameters: '270M',
    quantization: 'Q4 (4-bit)',
    format: 'ONNX',
    targetSpeed: '100+ tokens/sec',
    platform: 'Node.js',
    nodeVersion: process.version,
    loaded: modelLoaded,
    loadTime: modelLoadTime ? `${modelLoadTime.toFixed(2)}s` : null,
  });
});

app.post('/generate', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({ error: 'Model not loaded yet' });
  }

  try {
    const {
      prompt,
      maxTokens = 50,
      temperature = 0.7,
      system = 'You are a helpful assistant.'
    } = req.body;

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
        hit100Target: tokensPerSecond >= 100,
      },
      params: {
        maxTokens,
        temperature,
        quantization: 'Q4',
      },
    });
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({ error: 'Generation failed', message: error.message });
  }
});

app.post('/chat', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({ error: 'Model not loaded yet' });
  }

  try {
    const { messages, maxTokens = 50, temperature = 0.7 } = req.body;

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
        hit100Target: tokensPerSecond >= 100,
      },
    });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: 'Chat failed', message: error.message });
  }
});

app.post('/benchmark', async (req, res) => {
  if (!modelLoaded) {
    return res.status(503).json({ error: 'Model not loaded yet' });
  }

  try {
    const { iterations = 10 } = req.body;

    const benchmarkMessages = [
      { role: 'system', content: 'You are helpful.' },
      { role: 'user', content: 'What is AI?' },
    ];

    const times = [];
    const tpsList = [];

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
      tpsList.push(tps);

      console.log(`  Iter ${i+1}: ${time.toFixed(3)}s | ${tps.toFixed(1)} tok/s`);
    }

    // Remove warmup
    const timesNoWarmup = times.slice(1);
    const tpsNoWarmup = tpsList.slice(1);

    const avgTime = timesNoWarmup.reduce((a, b) => a + b, 0) / timesNoWarmup.length;
    const avgTps = tpsNoWarmup.reduce((a, b) => a + b, 0) / tpsNoWarmup.length;
    const maxTps = Math.max(...tpsNoWarmup);
    const minTps = Math.min(...tpsNoWarmup);

    console.log(`\nAvg speed: ${avgTps.toFixed(1)} tok/s`);

    res.json({
      success: true,
      results: {
        iterations,
        warmupTime: `${times[0].toFixed(3)}s`,
        avgTime: `${avgTime.toFixed(3)}s`,
        avgSpeed: `${avgTps.toFixed(1)} tokens/sec`,
        maxSpeed: `${maxTps.toFixed(1)} tokens/sec`,
        minSpeed: `${minTps.toFixed(1)} tokens/sec`,
        hit100Target: avgTps >= 100,
      },
      quantization: 'Q4 (4-bit)',
      targetSpeed: '100 tokens/sec',
      allSpeeds: tpsList.map(s => `${s.toFixed(1)} tok/s`),
    });
  } catch (error) {
    console.error('Benchmark error:', error);
    res.status(500).json({ error: 'Benchmark failed', message: error.message });
  }
});

app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    availableEndpoints: ['/health', '/model/info', '/generate', '/chat', '/benchmark'],
  });
});

app.listen(PORT, () => {
  console.log(`Starting ultra-fast API on port ${PORT}...`);
  loadModel();
});
