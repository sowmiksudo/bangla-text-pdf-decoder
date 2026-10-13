# Bangla PDF Decoder Agent Guide

## Overview
This repository contains the standalone, high-performance Bengali PDF font decoder (`bangla-pdf-decoder`). It decodes legacy, hybrid, and subsetted Bengali TrueType font encodings (such as `VOXLMY+Bangla`, `SQDAUS+Bangla`, and Sutonny-in-PDF exports from the Bangladesh Election Commission and BD Government databases) into clean Unicode UTF-8 (NFC).

## Architecture & Pipeline
1. **`src/bangla_pdf_decoder/decoder.py`**:
   - `LIGATURE_MAP`: Complete, empirically verified mapping for high-byte CIDs (0x80 - 0x2FF) including all rare conjuncts (`ক্ষ্ম`, `শু`, `চ্ছ`, `ক্ক`, `ব্ব`, `ন্দু`, `ঞ্ছ`, `ড়`, `য়`, `্ল`, etc.).
   - Multi-pass regex engine:
     - Reph (`Î`) and Oi-kar (`Ð`) prefix conversions.
     - Vowel repositioning (o-kar, au-kar, e-kar, visual i-kar swap).
     - Modifier swap: Corrects misplaced Chandrabindu, Anusvara, and Visarga (e.g. `দঁাত` -> `দাঁত`, `তেজগঁাও` -> `তেজগাঁও`).
     - Precomposed Nukta canonicalization: `\u09af\u09bc` -> `য়`, `\u09a1\u09bc` -> `ড়`, `\u09a2\u09bc` -> `ঢ়`.
     - Standard Unicode NFC normalization.
2. **`src/bangla_pdf_decoder/cli.py`**: CLI utility for decoding raw text, files, and batch streams.
3. **`tests/test_decoder.py`**: Full unit test suite (24 tests) validating conjuncts and edge cases.

## Development Commands
```powershell
# Run unit tests
python -m pytest -o pythonpath=src -v

# Build package distribution
python -m build

# Validate package distribution
python -m twine check dist/*

# Publish to PyPI
python -m twine upload dist/*
```
