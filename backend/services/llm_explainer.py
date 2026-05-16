from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings

class CodeExplainer:
    def __init__(self):
        """
        Initializes the Google Gemini AI Model.
        """
        # Hum yahan 'gemini-1.5-flash' use kar rahe hain jo fast aur smart hai
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.2 # Low temperature rakhi hai taake AI strictly technical baat kare
            )
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to initialize Gemini: {e}")

    def generate_explanation(self, file_path: str, code_content: str) -> str:
        """
        Takes a code file and returns a highly professional explanation.
        """
        # Ye wo strict instruction (Prompt) hai jo AI ko batayegi ke behave kaise karna hai
        prompt = f"""
        You are a highly experienced Senior Software Engineer and System Architect.
        Analyze the following code file from a GitHub repository.

        File Path: {file_path}
        
        Code Content:
        ```
        {code_content}
        ```

        Please provide a highly professional, structured explanation of this file. 
        Format your response using Markdown with the following sections:
        1. **Executive Summary**: 1-2 sentences explaining the main purpose of this file.
        2. **Core Components**: Bullet points of main classes/functions and what they do.
        3. **Technical Insights**: Mention any notable design patterns, algorithms, or Time/Space complexity (if applicable).
        
        Keep it concise, technical, and ready for a professional documentation page.
        """
        
        try:
            # AI ko prompt bhejna aur response lena
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"[ERROR] AI failed to explain {file_path}. Reason: {e}"

# --- Testing the AI Module ---
if __name__ == "__main__":
    print("[INFO] Booting up the Gemini AI Engine...")
    
    # Ek dummy code banate hain test karne ke liye
    test_file_path = "utils/math_operations.py"
    test_code = """
def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
    """
    
    explainer = CodeExplainer()
    print("[INFO] Analyzing code and generating explanation...\n")
    
    # AI se explanation mangte hain
    result = explainer.generate_explanation(test_file_path, test_code)
    
    print("================ AI GENERATED DOCUMENTATION ================\n")
    print(result)
    print("\n============================================================")