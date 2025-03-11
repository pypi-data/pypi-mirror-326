class SDKException(Exception):
    """Base exception for SDK errors"""
    pass

class AuthenticationError(SDKException):
    """Raised when authentication fails"""
    pass

class APIError(SDKException):
    """Raised when the API returns an error"""
    pass 