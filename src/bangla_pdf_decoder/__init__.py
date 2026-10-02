"""
bangla-pdf-decoder: High-speed decoder for legacy & hybrid Bengali PDF font encodings.
"""

from .decoder import (
    decode_bangla_pdf_text,
    decode_bengali_text,
    LIGATURE_MAP,
    WORD_FIXES,
)

__version__ = "0.1.0"
__author__ = "Sowmik"
__all__ = [
    "decode_bangla_pdf_text",
    "decode_bengali_text",
    "LIGATURE_MAP",
    "WORD_FIXES",
    "__version__",
]
