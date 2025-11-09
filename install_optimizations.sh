#!/bin/bash
# Install optimization dependencies for faster CPU inference

echo "=================================================="
echo "Gemma CPU Optimization Setup"
echo "=================================================="
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip not found. Please install Python and pip first."
    exit 1
fi

echo "Installing optimization libraries..."
echo ""

# Function to install and check
install_package() {
    local package=$1
    local name=$2

    echo "📦 Installing $name..."
    if pip install "$package" --quiet; then
        echo "   ✅ $name installed successfully"
    else
        echo "   ❌ Failed to install $name"
        return 1
    fi
}

# Install ONNX Runtime
echo ""
echo "1️⃣  Installing ONNX Runtime (for 2-4x speedup)"
echo "────────────────────────────────────────────────"
install_package "onnxruntime>=1.16.0" "ONNX Runtime"

# Install Optimum
echo ""
echo "2️⃣  Installing Optimum (for easy ONNX conversion)"
echo "────────────────────────────────────────────────"
install_package "optimum[onnxruntime]>=1.16.0" "HuggingFace Optimum"

echo ""
echo "=================================================="
echo "✅ Installation Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Run the optimization comparison:"
echo "     python test_gemma3_optimized.py"
echo ""
echo "  2. See which method is fastest on your CPU"
echo ""
echo "Expected speedup: 2-4x faster than baseline!"
echo ""
