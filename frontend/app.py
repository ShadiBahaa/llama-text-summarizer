import streamlit as st
import requests
import time
import json

# Set page configuration
st.set_page_config(
    page_title="LLaMA Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e88e5;
        padding: 1rem 0;
    }
    .stTextArea > div > div > textarea {
        font-family: 'Arial', sans-serif;
    }
    .summary-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1e88e5;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff4444;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🤖 LLaMA Text Summarizer</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for configuration and information
with st.sidebar:
    st.header("📊 System Status")
    
    # Check API health
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            if health_data["status"] == "healthy":
                st.markdown('<div class="success-box">✅ API: Connected</div>', unsafe_allow_html=True)
                if health_data.get("ollama") == "connected":
                    st.markdown('<div class="success-box">✅ Ollama: Connected</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ Ollama: Disconnected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ API: Disconnected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ API: Error</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="error-box">❌ API: Not reachable</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("📋 Instructions")
    st.markdown("""
    1. **Paste your text** in the text area below
    2. **Click Summarize** to generate a summary
    3. **Copy the result** when ready
    
    **Tips:**
    - Use text with at least 50 characters
    - Longer texts work better for summarization
    - The model may take 10-30 seconds to respond
    """)
    
    st.markdown("---")
    st.header("ℹ️ About")
    st.markdown("""
    This app uses **LLaMA 2** model via **Ollama** to summarize text.
    
    **Tech Stack:**
    - 🦙 LLaMA 2 (via Ollama)
    - ⚡ FastAPI (Backend)
    - 🎈 Streamlit (Frontend)
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Text")
    user_input = st.text_area(
        "Enter your text here:",
        height=300,
        placeholder="Paste the text you want to summarize here...\n\nExample: A long article, research paper, news article, or any text content you'd like to get a summary of.",
        help="Enter at least 50 characters for meaningful summarization"
    )
    
    # Character count
    char_count = len(user_input)
    if char_count > 0:
        if char_count < 50:
            st.warning(f"⚠️ {char_count} characters (minimum 50 needed)")
        else:
            st.success(f"✅ {char_count} characters")
    
    # Summarize button
    summarize_button = st.button("🚀 Summarize Text", type="primary", use_container_width=True)

with col2:
    st.header("📋 Summary")
    
    if summarize_button:
        if not user_input.strip():
            st.error("❌ Please enter some text to summarize!")
        elif len(user_input) < 50:
            st.error("❌ Please enter at least 50 characters for meaningful summarization.")
        else:
            # Show loading spinner
            with st.spinner("🤖 LLaMA is analyzing your text... This may take 10-30 seconds."):
                try:
                    # Make API call
                    start_time = time.time()
                    response = requests.post(
                        "http://localhost:8000/summarize/",
                        data={"text": user_input},
                        timeout=90
                    )
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        result = response.json()
                        summary = result.get("summary", "Error generating summary.")
                        
                        # Display success message
                        st.success(f"✅ Summary generated in {end_time - start_time:.1f} seconds!")
                        
                        # Display summary in a nice box
                        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add copy button functionality
                        st.code(summary, language=None)
                        
                        # Summary statistics
                        original_words = len(user_input.split())
                        summary_words = len(summary.split())
                        compression_ratio = (1 - summary_words/original_words) * 100 if original_words > 0 else 0
                        
                        st.info(f"📊 **Stats:** Original: {original_words} words → Summary: {summary_words} words (📉 {compression_ratio:.1f}% compression)")
                        
                    else:
                        error_detail = response.json().get("detail", "Unknown error occurred")
                        st.error(f"❌ Error: {error_detail}")
                        
                except requests.exceptions.Timeout:
                    st.error("❌ **Timeout Error:** The request took too long. The model might be processing a very large text or the system is overloaded. Please try again with shorter text.")
                    
                except requests.exceptions.ConnectionError:
                    st.error("❌ **Connection Error:** Cannot connect to the API server. Please make sure:")
                    st.markdown("""
                    - The FastAPI backend is running on `localhost:8000`
                    - Ollama is running on `localhost:11434`
                    - The LLaMA2 model is downloaded (`ollama pull llama2`)
                    """)
                    
                except Exception as e:
                    st.error(f"❌ **Unexpected Error:** {str(e)}")
    else:
        st.info("👆 Enter your text and click 'Summarize Text' to get started!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Made with ❤️ using LLaMA 2, FastAPI, and Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)