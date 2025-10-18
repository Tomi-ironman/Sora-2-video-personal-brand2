"""
Voice Providers Package
Free voice generation and cloning APIs
"""

# Chatterbox will be available once Python 3.11 environment is set up
try:
    from .chatterbox_provider import ChatterboxProvider
    __all__ = ['ChatterboxProvider']
except ImportError:
    # Chatterbox not installed yet (requires Python 3.11)
    __all__ = []
