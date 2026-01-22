"""
Exception classes for the Digital FTE Automation system.
"""

class DigitalFTEError(Exception):
    """Base exception class for Digital FTE Automation system."""
    pass


class FileProcessingError(DigitalFTEError):
    """Raised when file processing fails."""
    pass


class ConfigurationError(DigitalFTEError):
    """Raised when configuration is invalid."""
    pass


class StateTransitionError(DigitalFTEError):
    """Raised when an invalid state transition is attempted."""
    pass