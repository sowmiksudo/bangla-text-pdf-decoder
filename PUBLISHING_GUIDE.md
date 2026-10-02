# Step-by-Step Guide: Publishing `bangla-pdf-decoder` to PyPI

This guide walks you through building, testing, and publishing your package to **PyPI (Python Package Index)** so that anyone can install it with:

```bash
pip install bangla-pdf-decoder
```

---

## 1. Prerequisites

Make sure you have the standard packaging tools installed:

```bash
pip install --upgrade build twine
```

* `build`: Builds the source distribution (`.tar.gz`) and binary wheel (`.whl`).
* `twine`: Securely uploads your distribution files to PyPI via HTTPS.

---

## 2. Test Locally Before Publishing

Before uploading to PyPI, verify that the package installs cleanly on your machine:

```powershell
cd bangla-pdf-decoder

# Install the package in editable mode
pip install -e .

# Run the test suite to ensure all 24 tests pass
pytest

# Test the CLI tool
bangla-pdf-decoder --text "চূড়াĢ Ïভাটার তািলকা, অûল: চÿগ্রাম, কÔবাজার"
```

Expected output:
```text
চূড়ান্ত ভোটার তালিকা, অঞ্চল: চট্টগ্রাম, কক্সবাজার
```

---

## 3. Build the Package Distribution

Generate the distribution files:

```powershell
# Inside bangla-pdf-decoder directory:
python -m build
```

This creates a `dist/` folder containing two files:
1. `bangla_pdf_decoder-0.1.0-py3-none-any.whl` (Binary wheel)
2. `bangla_pdf_decoder-0.1.0.tar.gz` (Source archive)

Check the build files with `twine`:

```powershell
twine check dist/*
```

Expected output:
```text
Checking dist/bangla_pdf_decoder-0.1.0-py3-none-any.whl: PASSED
Checking dist/bangla_pdf_decoder-0.1.0.tar.gz: PASSED
```

---

## 4. Set Up PyPI Accounts & API Tokens

### Step A: Create an Account on PyPI
1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/) and create an account.
2. Verify your email address.
3. Enable **Two-Factor Authentication (2FA)** (required by PyPI).

### Step B: Create an API Token
1. Go to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/).
2. Set **Token name**: `bangla-pdf-decoder-publish`.
3. Set **Scope**: `Entire account` (since the package does not exist on PyPI yet).
4. Click **Generate token**.
5. Copy the token (starts with `pypi-AgEI...`). **Save it securely**, you will not see it again!

---

## 5. (Optional but Recommended) Test on TestPyPI First

TestPyPI is a sandbox environment where you can test your upload without affecting the live PyPI index.

1. Register on [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/).
2. Generate an API token on TestPyPI.
3. Upload to TestPyPI:

```powershell
twine upload --repository testpypi dist/*
```
* **Username:** `__token__`
* **Password:** *(Paste your TestPyPI API token including `pypi-...`)*

4. Test installing from TestPyPI in a fresh virtualenv:

```powershell
pip install --index-url https://test.pypi.org/simple/ --no-deps bangla-pdf-decoder
```

---

## 6. Publish to Production PyPI 🚀

When you are ready for the official release:

```powershell
twine upload dist/*
```

Prompts:
* **Username:** `__token__`
* **Password:** *(Paste your PyPI API token starting with `pypi-...`)*

Once uploaded, your package will be immediately live at:
👉 **`https://pypi.org/project/bangla-pdf-decoder/`**

Now anyone in the world can run:
```bash
pip install bangla-pdf-decoder
```

---

## 7. How to Release Future Updates (v0.1.1, v0.2.0, etc.)

Whenever you add new ligature mappings or bug fixes:

1. Update the version in `pyproject.toml` and `src/bangla_pdf_decoder/__init__.py`:
   ```toml
   version = "0.1.1"
   ```
2. Delete old build artifacts:
   ```powershell
   Remove-Item -Recurse -Force dist, build
   ```
3. Rebuild and upload:
   ```powershell
   python -m build
   twine upload dist/*
   ```

---

## 8. Automate with GitHub Actions (Optional)

You can automatically publish to PyPI whenever you push a Git release tag (e.g. `v0.1.0`).

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  pypi-publish:
    name: Build and publish Python 🐍 distributions 📦 to PyPI
    runs-on: ubuntu-latest
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build

      - name: Build package
        run: |
          cd bangla-pdf-decoder
          python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: bangla-pdf-decoder/dist/
```
