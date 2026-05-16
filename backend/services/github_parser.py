import base64
from typing import List, Dict
from github import Github, Auth
from github.GithubException import UnknownObjectException
from backend.core.config import settings

class GitHubRepoFetcher:
    def __init__(self, repo_url: str):
        """
        Establishes a connection to the GitHub repository using the provided URL.
        Uses a personal access token with the updated Auth module to prevent rate limiting.
        """
        # [UPDATED] Initialize GitHub client using the new Auth method to avoid DeprecationWarning
        if settings.GITHUB_TOKEN:
            auth = Auth.Token(settings.GITHUB_TOKEN)
            self.client = Github(auth=auth)
        else:
            self.client = Github()
        
        # Parse the URL to extract 'owner/repo_name'
        try:
            parts = repo_url.rstrip('/').split('/')
            self.repo_name = f"{parts[-2]}/{parts[-1]}"
            self.repo = self.client.get_repo(self.repo_name)
        except Exception as e:
            raise ValueError(f"Invalid GitHub URL or repository does not exist. Details: {str(e)}")

    def fetch_all_code_files(self) -> List[Dict[str, str]]:
        """
        Traverses the repository directory structure using Breadth-First Search (BFS)
        and extracts the content of all supported source code files.
        """
        files_data = []
        # Target extensions to avoid downloading images, videos, or compiled binaries
        allowed_extensions = ('.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.md', '.json')
        
        try:
            # Start at the root directory of the repository
            contents = self.repo.get_contents("")
            
            # Queue for BFS traversal
            while contents:
                file_content = contents.pop(0)
                
                if file_content.type == "dir":
                    # If it's a directory, fetch its contents and add to the queue
                    contents.extend(self.repo.get_contents(file_content.path))
                else:
                    # If it's a file, check its extension and decode the content
                    if file_content.name.endswith(allowed_extensions):
                        try:
                            # GitHub API returns file content encoded in Base64
                            decoded_text = base64.b64decode(file_content.content).decode('utf-8')
                            files_data.append({
                                "path": file_content.path,
                                "content": decoded_text
                            })
                        except Exception as decode_err:
                            print(f"[WARNING] Skipping {file_content.path}: Decoding failed. Reason: {decode_err}")
                            
        except UnknownObjectException:
            print("[ERROR] Repository not found or it is strictly private.")
            
        return files_data

# --- Testing the Module ---
if __name__ == "__main__":
    print("[INFO] Initializing repository fetcher... Please wait.")
    
    # Using a popular open-source repository for testing
    test_url = "https://github.com/psf/requests" 
    
    try:
        fetcher = GitHubRepoFetcher(test_url)
        extracted_files = fetcher.fetch_all_code_files()
        
        print(f"\n[SUCCESS] Successfully fetched {len(extracted_files)} files from the repository.")
        
        if extracted_files:
            print("\n--- Code Snippet Preview ---")
            print(f"File Path: {extracted_files[0]['path']}")
            print("Preview (First 200 characters):\n")
            print(extracted_files[0]['content'][:200] + "...\n")
            print("----------------------------")
            
    except Exception as e:
        print(f"[CRITICAL ERROR] Execution failed: {e}")