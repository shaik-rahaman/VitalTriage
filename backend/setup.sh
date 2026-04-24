#!/bin/bash

# Setup script for VitalTriage Backend
# This script sets up the complete development environment

set -e

echo "🏥 VitalTriage Backend - Setup Script"
echo "====================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "📤 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Setup .env file
echo ""
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (please update with your values)"
else
    echo "✓ .env file already exists"
fi

# Check MongoDB
echo ""
echo "🗄️  Checking MongoDB..."
if command -v mongod &> /dev/null; then
    echo "✓ MongoDB is installed"
    echo ""
    echo "📌 To start MongoDB locally:"
    echo "   brew services start mongodb-community"
    echo ""
    echo "Or use Docker:"
    echo "   docker-compose up -d"
else
    echo "⚠️  MongoDB not found in PATH"
    echo "📌 Install using:"
    echo "   brew tap mongodb/brew && brew install mongodb-community"
    echo ""
    echo "Or use Docker:"
    echo "   docker-compose up -d"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Start MongoDB (see instructions above)"
echo "2. Update .env file with your configuration"
echo "3. Run the development server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "📖 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "📧 To load demo patients:"
echo "   python demo_data.py"
echo ""
