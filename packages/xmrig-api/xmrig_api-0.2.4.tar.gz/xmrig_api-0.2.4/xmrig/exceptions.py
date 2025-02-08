"""
XMRig Exceptions module.

This module provides custom exception classes for handling specific XMRig API errors.
It includes:

- XMRigAPIError: General error with the XMRig API.
- XMRigAuthorizationError: Authorization error with the XMRig API.
- XMRigConnectionError: Connection error with the XMRig API.
- XMRigDatabaseError: Database error with the XMRig API.
- XMRigManagerError: Manager error with the XMRig API.
"""
class XMRigAPIError(Exception):
    """
    Exception raised when a general error occurs with the XMRig API.

    Attributes:
        error (str): Specific error message.
        traceback (str): Traceback of the error.
        message (str): Error message explaining the API issue.
    """
    def __init__(self, error = None, traceback = None, message = "An error occurred with the XMRig API:"):
        """
        Initialize the API error.

        Args:
            error (str, optional): Specific error message. Defaults to None.
            traceback (str, optional): Traceback of the error. Defaults to None.
            message (str): Error message explaining the API issue. Defaults to a generic API error message.
        """
        error_message = f" {error}" if error else ""
        traceback_message = f"\n{traceback}" if traceback else ""
        self.message = message + error_message + traceback_message
        super().__init__(self.message)

class XMRigAuthorizationError(XMRigAPIError):
    """
    Exception raised when an authorization error occurs with the XMRig API.
    """
    def __init__(self, error = None, traceback = None, message = "Access token is required but not provided. Please provide a valid access token."):
        super().__init__(error, traceback, message)

class XMRigConnectionError(XMRigAPIError):
    """
    Exception raised when a connection error occurs with the XMRig API.
    """
    def __init__(self, error = None, traceback = None, message = "Failed to connect to the XMRig API. Please check the IP, port, and network connection."):
        super().__init__(error, traceback, message)

class XMRigDatabaseError(XMRigAPIError):
    """
    Exception raised when a database error occurs with the XMRig API.
    """
    def __init__(self, error = None, traceback = None, message = "An error occurred with the XMRig database. Please check the database configuration."):
        super().__init__(error, traceback, message)

class XMRigManagerError(XMRigAPIError):
    """
    Exception raised when a manager error occurs with the XMRig API.
    """
    def __init__(self, error = None, traceback = None, message = "An error occurred with the XMRig manager."):
        super().__init__(error, traceback, message)

# Define the public interface of the module
__all__ = ["XMRigAPIError", "XMRigAuthorizationError", "XMRigConnectionError", "XMRigDatabaseError", "XMRigManagerError"]