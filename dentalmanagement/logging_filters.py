"""
Custom logging filters to suppress HTTPS error messages
"""

import logging

class SuppressHTTPSErrors(logging.Filter):
    """Filter to suppress HTTPS-related error messages in development"""
    
    def filter(self, record):
        # Suppress messages about HTTPS on development server
        message = record.getMessage()
        
        # List of patterns to suppress
        suppress_patterns = [
            "You're accessing the development server over HTTPS",
            "Bad request version",
            "Bad request syntax",
            "Bad HTTP/0.9 request type",
        ]
        
        # Check if message contains any suppress pattern
        for pattern in suppress_patterns:
            if pattern in message:
                return False  # Don't log this message
        
        return True  # Log all other messages
