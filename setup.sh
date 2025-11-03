#!/bin/bash
# setup.sh - Quick setup script for OUVC clean foundation

echo "🚀 Setting up OUVC Clean Foundation..."
echo "====================================="

# Check Python version
if ! python3 --version &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv ouvc_env
    source ouvc_env/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Setting up environment file..."
    cp .env.template .env
    echo "✅ Created .env file from template"
    echo "💡 Edit .env file to add your API keys"
else
    echo "✅ .env file already exists"
fi

# Create secure_config directory
echo "🔐 Setting up secure configuration..."
mkdir -p secure_config
chmod 700 secure_config

# Create API keys file if it doesn't exist
if [ ! -f secure_config/api_keys.env ]; then
    cat > secure_config/api_keys.env << EOF
# API Keys Storage
# Add your API keys here

# Crypto APIs
COINGECKO_API_KEY=your_coingecko_api_key_here

# Dubai Property APIs
BAYUT_API_KEY=your_rapidapi_bayut_key_here
DLD_API_KEY=your_dubai_land_department_key_here
EOF
    chmod 600 secure_config/api_keys.env
    echo "✅ Created secure API keys file"
fi

# Test the setup
echo ""
echo "🧪 Testing setup..."
if python3 -c "import requests, pandas, numpy; print('✅ Core modules imported successfully')"; then
    echo "✅ Setup test passed"
else
    echo "❌ Setup test failed - check dependencies"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env or secure_config/api_keys.env with your API keys"
echo "2. Run: python3 main.py"
echo "3. Try demo mode (option 3) to test without API keys"
echo ""
echo "🔗 Get API keys:"
echo "  - Bayut: https://rapidapi.com/apidojo/api/bayut/"
echo "  - CoinGecko: https://coingecko.com/en/api"
echo ""
echo "🚀 Ready to analyze crypto and Dubai properties!"