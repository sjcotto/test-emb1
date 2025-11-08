#!/bin/bash
# Run the embedding model comparison tests

echo "="
echo "RUNNING EMBEDDING MODEL TESTS"
echo "120 Products | 100 Test Queries"
echo "="

# Run the actual tests
python embedding_tester.py

echo ""
echo "Tests complete! Check evaluation_results.json for results"
