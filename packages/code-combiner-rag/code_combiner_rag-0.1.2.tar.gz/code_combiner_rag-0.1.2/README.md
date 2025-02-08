# Code Combiner

A command-line tool to combine multiple code files into a single file, with support for exclusion patterns. Useful for preparing codebases for RAG (Retrieval-Augmented Generation) pipelines.

## Installation

```bash
pip install code-combiner-rag
```

## Usage

```bash
# Create a default config file
code-combiner --create-config

# Combine files using the config
code-combiner /path/to/directory --config code_combiner_config.yaml --output combined_code.txt
```

## Configuration

Create a YAML configuration file with exclusion patterns:

```yaml
exclude_files:
  - "/absolute/path/to/file.py"
  - "relative/path/to/file.js"

exclude_patterns:
  - "*.test.js"
  - "__pycache__/"
  - "node_modules/"

exclude_extensions:
  - ".pyc"
  - ".pyo"
```

## Options

- `--output`: Specify output file path (default: combined_code.txt)
- `--config`: Specify config file path (default: code_combiner_config.yaml)
- `--create-config`: Create a default configuration file
- `--version`: Show program version
- `--help`: Show help message
