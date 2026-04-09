
# py_prettier_xethhung12

A powerful CLI tool to format XML, HTML, and JSON with support for multiple input and output sources.

## Features

- **Format Support**: XML, HTML, and JSON
- **Input Sources**: 
  - stdin (default)
  - File (`-f`, `--file`)
  - Clipboard (`--from-clip`)
- **Output Destinations**:
  - stdout (default)
  - Clipboard (`--clip`)
  - File (`-o`, `--output`)
- **Unicode Support**: Proper UTF-8 handling, especially for Windows environments

## Installation

```bash
pip install py-prettier-xethhung12
```

Or install from source:
```bash
pip install -e .
```

## Usage

### Basic Usage

Format JSON from stdin to stdout:
```bash
cat input.json | py-prettier-xethhung12 json
```

### Input Options

**From stdin (default):**
```bash
py-prettier-xethhung12 json < input.json
py-prettier-xethhung12 json --stdin < input.json
```

**From file:**
```bash
py-prettier-xethhung12 xml -f input.xml
py-prettier-xethhung12 html --file messy.html
```

**From clipboard:**
```bash
py-prettier-xethhung12 json --from-clip
```

### Output Options

**To stdout (default):**
```bash
py-prettier-xethhung12 json < input.json
py-prettier-xethhung12 json --stdout < input.json
```

**To clipboard:**
```bash
py-prettier-xethhung12 xml -f input.xml --clip
```

**To file:**
```bash
py-prettier-xethhung12 json -f messy.json -o formatted.json
py-prettier-xethhung12 html --file input.html --output output.html
```

### Combined Examples

Format file and copy to clipboard:
```bash
py-prettier-xethhung12 xml -f input.xml --clip
```

Format clipboard content and save to file:
```bash
py-prettier-xethhung12 json --from-clip -o formatted.json
```

Re-format clipboard content (clipboard to clipboard):
```bash
py-prettier-xethhung12 xml --from-clip --clip
```

### Help

```bash
py-prettier-xethhung12 -h
py-prettier-xethhung12 json -h
py-prettier-xethhung12 xml -h
py-prettier-xethhung12 html -h
```

## Running the Application

### Through Python module:
```bash
python -m py_prettier_xethhung12 -h
```

### Through installed script:
```bash
py-prettier-xethhung12 -h
```

## Development

The project requires `python` 3.11+ and `pip` for dependency management.

### Setup

Install development dependencies:
```bash
./install-dependencies.sh
```

This script installs:
- Dependencies from `dev-requirements.txt` (build and deployment tools)
- Dependencies from `requirements.txt` (runtime dependencies)

### Build

```bash
./build.sh
```

### Build and Deploy

```bash
./build-and-deploy.sh
```

## Scripts

| Name | Type | Description |
|------|------|-------------|
| install-dependencies.sh | Shell script | Install dev and runtime dependencies |
| build.sh | Shell script | Build the package |
| build-and-deploy.sh | Shell script | Build and deploy the package |

## Project Versioning

This project uses the [`xh-py-project-versioning`](https://github.com/xh-dev/xh-py-project-versioning) package for version management.

### Update Patch Version (dev):
```bash
python -m xh_py_project_versioning --patch
```
Example: `0.0.1` → `0.0.2-dev+000`

### Promote Dev to Official Release:
```bash
python -m xh_py_project_versioning -r
```
Example: `0.0.2-dev+000` → `0.0.2`

### Update Patch Version (direct):
```bash
python -m xh_py_project_versioning --patch -d
```
Example: `0.0.1` → `0.0.2`

### Update Minor Version (direct):
```bash
python -m xh_py_project_versioning --minor -d
```
Example: `0.0.1` → `0.1.0`

### Update Major Version (direct):
```bash
python -m xh_py_project_versioning --major -d
```
Example: `0.0.1` → `1.0.0`

## Dependencies

- **j-vault-http-client-xethhung12** (>= 0.1.1) - HTTP client library
- **beautifulsoup4** (>= 4.12.0) - HTML/XML parsing
- **pyperclip** (>= 1.8.2) - Clipboard support

## License

GPL-3.0-only

## Author

Xeth Hung (admin@xethh.me)

