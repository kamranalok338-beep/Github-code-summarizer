class GitHubSummarizerException(Exception):
    """Base exception class for the GitHub Code Summarizer application."""
    pass

class RepositoryFetchError(GitHubSummarizerException):
    """Raised when the system fails to fetch or decode files from GitHub."""
    pass

class AIAnalysisError(GitHubSummarizerException):
    """Raised when the Gemini AI model encounters an error generating summaries."""
    pass