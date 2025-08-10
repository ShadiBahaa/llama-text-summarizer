# 🦙 LLaMA Text Summarizer

This is a powerful AI-powered text summarization application that uses the LLaMA 2 model (via Ollama) to generate concise summaries of your text content.
![Description](https://private-user-images.githubusercontent.com/33010011/476349164-7f6bd980-3b0c-413c-8550-8e932df6a344.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4MjQ0MDMsIm5iZiI6MTc1NDgyNDEwMywicGF0aCI6Ii8zMzAxMDAxMS80NzYzNDkxNjQtN2Y2YmQ5ODAtM2IwYy00MTNjLTg1NTAtOGU5MzJkZjZhMzQ0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDExMDgyM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWZkZDlkN2QyNDQzZThmYTI5MzllMDRlMzc1OWU0YjY3YjZmMjQzNTI0NDZhN2VkOTA3NGVhM2ViMWM4NTU4MGEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0._zyl9aSfXpxZakSm_wI6ur-zeAQDSHoVMcH88nwL9I0)


## 🚀 Features

- **Local AI Processing**: Uses LLaMA 2 model running locally via Ollama
- **FastAPI Backend**: Robust REST API with error handling and health checks
- **Streamlit Frontend**: Beautiful, responsive web interface
- **Real-time Status**: Shows connection status for API and Ollama services
- **Smart Validation**: Ensures meaningful input for better summarization
- **Performance Metrics**: Shows processing time and compression statistics

## 🛠️ Tech Stack

- **🦙 LLaMA 2**: State-of-the-art language model for text summarization
- **⚡ FastAPI**: Modern, fast web framework for building APIs
- **🎈 Streamlit**: Easy-to-use framework for creating web apps
- **🔧 Ollama**: Tool for running large language models locally
- **📚 Git/GitHub**: Version control and repository hosting

## 📋 Prerequisites

Before running this project, make sure you have:

- Python 3.8 or higher
- Git
- At least 8GB of RAM (recommended for LLaMA 2)

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llama-text-summarizer.git
cd llama-text-summarizer
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install and Configure Ollama

1. **Download Ollama**: Visit [ollama.com](https://ollama.com) and download for your OS
2. **Install Ollama** following the platform-specific instructions
3. **Pull the LLaMA 2 model**:
   ```bash
   ollama pull llama2
   ```

### 4. Project Structure


```
llama-text-summarizer/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── venv/
├── requirements.txt
└── README.md
```

## 🚀 Running the Application

### Step 1: Start Ollama Service

Make sure Ollama is running in the background. It should automatically start after installation, but you can verify by running:

```bash
ollama list
```

### Step 2: Start the FastAPI Backend

Open a terminal and run:

```bash
uvicorn backend.main:app --reload
```

The API will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Step 3: Start the Streamlit Frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

The web app will be available at: `http://localhost:8501`

## 💡 Usage

1. **Open the web app** in your browser (`http://localhost:8501`)
2. **Check system status** in the sidebar to ensure all services are connected
3. **Paste your text** in the input area (minimum 50 characters)
4. **Click "Summarize Text"** and wait for the AI to process
5. **View your summary** with performance statistics
6. **Copy the result** using the code block

## 🔍 API Endpoints

- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check for API and Ollama service
- `POST /summarize/` - Main summarization endpoint

## 🛠️ Troubleshooting

### Common Issues

**1. "Cannot connect to Ollama service"**
- Ensure Ollama is installed and running
- Check if the LLaMA 2 model is downloaded: `ollama list`
- Verify Ollama is accessible: `curl http://localhost:11434/api/tags`

**2. "API Not reachable"**
- Make sure the FastAPI backend is running on port 8000
- Check for port conflicts
- Verify the backend is accessible: `curl http://localhost:8000/health`

**3. "Request timeout"**
- The LLaMA model might be processing large text
- Try with shorter text (under 1000 words)
- Ensure sufficient system resources (RAM/CPU)

### Performance Tips

- **Text Length**: Works best with 100-5000 words
- **System Resources**: Ensure at least 8GB RAM available
- **Multiple Requests**: Allow time between requests for better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all services are running properly
3. Check the logs in both terminal windows
4. Open an issue on GitHub with details about the error

## 🔮 Future Enhancements

- [ ] Support for multiple LLaMA model variants
- [ ] Batch text processing
- [ ] Export summaries to different formats
- [ ] Advanced summarization options (length, style)
- [ ] User authentication and saved summaries
- [ ] Integration with document upload (PDF, DOCX)

---


**Happy Summarizing!** 🚀


