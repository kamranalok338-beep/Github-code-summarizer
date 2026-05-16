from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.github_parser import GitHubRepoFetcher
from backend.services.llm_explainer import CodeExplainer
from backend.utils.text_cleaner import TextCleaner
from backend.core.exceptions import RepositoryFetchError, AIAnalysisError

# Initialize the router for the API
router = APIRouter()

# Pydantic models for request and response validation
class RepoRequest(BaseModel):
    repo_url: str

class AnalysisResponse(BaseModel):
    status: str
    total_files_analyzed: int
    documentation_generated: str

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: RepoRequest):
    """
    API Endpoint to process a GitHub URL, parse code files via AST,
    and generate structured summaries using Gemini AI.
    """
    print(f"[INFO] API received request to analyze repository: {request.repo_url}")
    
    try:
        # Step 1: Fetch and parse code files from GitHub
        print("[INFO] Launching GitHub repository fetching pipeline...")
        try:
            fetcher = GitHubRepoFetcher(request.repo_url)
            files = fetcher.fetch_all_code_files()
        except Exception as e:
            raise RepositoryFetchError(f"Failed to access GitHub repository. Details: {str(e)}")
        
        if not files:
            raise HTTPException(status_code=404, detail="No supported source code files found in this repository.")
        
        # Step 2: Initialize the generative AI core engine
        print("[INFO] Activating Gemini Generative AI core engine...")
        try:
            explainer = CodeExplainer()
        except Exception as e:
            raise AIAnalysisError(f"Failed to initialize Gemini AI engine. Details: {str(e)}")
        
        # Initializing the summary document structure
        documentation = f"# 🤖 AI System Architecture & Summary\n**Repository:** `{request.repo_url}`\n\n---\n\n"
        
        # Step 3: Iterate and analyze files sequentially
        for file_data in files:
            print(f"[PROCESS] Analyzing deep logical structure for: {file_data['path']}...")
            raw_explanation = explainer.generate_explanation(file_data['path'], file_data['content'])
            
            # Sanitize and format the AI markdown output
            clean_explanation = TextCleaner.clean_markdown_output(raw_explanation)
            
            # Appending file documentation block
            documentation += f"## 📄 File: `{file_data['path']}`\n\n"
            documentation += f"{clean_explanation}\n\n<br>\n\n---\n\n"
            
        print("[SUCCESS] Repository analysis pipeline completed successfully.")
        
        return AnalysisResponse(
            status="success",
            total_files_analyzed=len(files),
            documentation_generated=documentation
        )
        
    except RepositoryFetchError as e:
        print(f"[EXCEPTION] Handled Repository Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except AIAnalysisError as e:
        print(f"[EXCEPTION] Handled AI Core Error: {e}")
        raise HTTPException(status_code=502, detail=str(e))
        
    except Exception as e:
        print(f"[CRITICAL] Unexpected error encountered in route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred within the analysis engine.")