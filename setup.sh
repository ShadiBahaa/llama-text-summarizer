#!/bin/bash

# LLaMA Text Summarizer - Automated Setup Script
# This script sets up the entire project environment

echo "🦙 LLaMA Text Summarizer - Setup Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
print_step "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "Found $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    print_status "Found $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Create project directories
print_step "Creating project structure..."
mkdir -p backend
mkdir -p frontend

# Create virtual environment
print_step "Setting up virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
print_step "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
print_step "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 streamlit==1.28.1 requests==2.31.0 python-multipart==0.0.6

# Check if Ollama is installed
print_step "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    print_status "Ollama is already installed"
    
    # Check if LLaMA 2 model is available
    print_step "Checking for LLaMA 2 model..."
    if ollama list | grep -q "llama2"; then
        print_status "LLaMA 2 model is already downloaded"
    else
        print_warning "LLaMA 2 model not found. Downloading now (this may take several minutes)..."
        ollama pull llama2
        if [ $? -eq 0 ]; then
            print_status "LLaMA 2 model downloaded successfully"
        else
            print_error "Failed to download LLaMA 2 model"
            exit 1
        fi
    fi
else
    print_warning "Ollama is not installed."
    echo "Please install Ollama manually:"
    echo "1. Visit https://ollama.com"
    echo "2. Download and install for your operating system"
    echo "3. Run 'ollama pull llama2' to download the model"
    echo "4. Then re-run this setup script"
    exit 1
fi

# Create a run script
print_step "Creating run scripts..."

# Create run script for Unix/Linux/macOS
cat > run.sh << 'EOF'
#!/bin/bash

echo "🦙 Starting LLaMA Text Summarizer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Function to handle cleanup
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "🚀 Starting FastAPI backend..."
uvicorn backend.main:app --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "🎈 Starting Streamlit frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

echo ""
echo "✅ Services started successfully!"
echo "📊 FastAPI backend: http://localhost:8000"
echo "🎈 Streamlit frontend: http://localhost:8501"
echo "📖 API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait
EOF

# Create run script for Windows
cat > run.bat << 'EOF'
@echo off
echo 🦙 Starting LLaMA Text Summarizer...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.sh first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

echo 🚀 Starting FastAPI backend...
start "FastAPI Backend" cmd /k "uvicorn backend.main:app --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo 🎈 Starting Streamlit frontend...
start "Streamlit Frontend" cmd /k "streamlit run frontend/app.py"

echo.
echo ✅ Services started successfully!
echo 📊 FastAPI backend: http://localhost:8000
echo 🎈 Streamlit frontend: http://localhost:8501
echo 📖 API docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
EOF

# Make scripts executable
chmod +x run.sh

print_step "Setup completed successfully!"
echo ""
print_status "🎉 Your LLaMA Text Summarizer is ready to use!"
echo ""
echo "Next steps:"
echo "1. Run the application:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   • Windows: Double-click run.bat OR run './run.bat'"
else
    echo "   • Unix/Linux/macOS: Run './run.sh'"
fi
echo ""
echo "2. Open your browser and visit:"
echo "   • Frontend: http://localhost:8501"
echo "   • API docs: http://localhost:8000/docs"
echo ""
echo "3. Start summarizing your text! 📝"
echo ""
print_warning "Note: Make sure Ollama service is running before starting the application."