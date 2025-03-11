class KruncherError(Exception):
    """Base exception for Kruncher client errors"""
    pass

class KruncherAPIError(KruncherError):
    """Raised when the API returns an error response"""
    pass

class KruncherClientError(Exception):
    """Base exception for KruncherClient errors."""
    pass

class KruncherAuthError(KruncherClientError):
    """Raised when authentication fails or API key is missing."""
    pass 