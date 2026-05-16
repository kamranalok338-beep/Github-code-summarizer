import streamlit as st
import requests

# Page setup for premium responsive layout
st.set_page_config(page_title="GitHub Code Summarizer AI", page_icon="🤖", layout="wide")

# Injecting custom enterprise CSS styling
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# UI Headers and Branding updates
st.title("🚀 GitHub Code Summarizer AI")
st.markdown("Paste any public GitHub repository link below, and our Gemini 2.5 AI will scan the entire codebase using AST parsing to generate a technical summary instantly.")

st.markdown("---")

# User repository URL entry field
repo_url = st.text_input("🔗 GitHub Repository URL", placeholder="e.g., https://github.com/karpathy/micrograd")

# Core Execution Flow Block
if st.button("Generate AI Summary", type="primary"):
    if not repo_url:
        st.warning("Please enter a valid GitHub repository URL to execute analysis.")
    else:
        # User feedback interface state trigger
        with st.spinner("AI engine is mapping dependencies and generating summaries... Please hold."):
            try:
                # Dispatched HTTP payload transfer to backend service framework
                api_url = "http://127.0.0.1:8000/api/analyze"
                response = requests.post(api_url, json={"repo_url": repo_url})
                
                # Dynamic rendering based on processing feedback metrics
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"🎉 Analysis Successful! Processed {data['total_files_analyzed']} production code files.")
                    st.markdown("---")
                    
                    # Output rendering block
                    st.markdown(data['documentation_generated'])
                else:
                    error_detail = response.json().get('detail', 'Unknown API Exception Encountered')
                    st.error(f"Backend Server Process Error: {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Refused! Verify that the FastAPI backend Uvicorn server is active on port 8000.")
            except Exception as e:
                st.error(f"An unexpected frontend processing error occurred: {e}")