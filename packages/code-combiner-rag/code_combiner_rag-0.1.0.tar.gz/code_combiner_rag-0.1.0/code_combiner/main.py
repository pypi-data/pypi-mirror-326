import os
import fnmatch
from pathlib import Path
import argparse
import yaml
import sys

def load_config(config_path):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        return {'exclude_patterns': [], 'exclude_extensions': [], 'exclude_files': []}
    
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"Error reading config file: {e}", file=sys.stderr)
        sys.exit(1)

def should_exclude(path, config, base_dir):
    """Check if path should be excluded based on config patterns."""
    path_str = str(path)
    relative_path = str(path.relative_to(base_dir))
    
    # Check specific files (both absolute and relative paths)
    exclude_files = config.get('exclude_files', [])
    if any(Path(exclude_file).resolve() == path.resolve() for exclude_file in exclude_files):
        return True
    
    # Check file extensions
    if any(path_str.endswith(ext) for ext in config.get('exclude_extensions', [])):
        return True
    
    # Check patterns
    for pattern in config.get('exclude_patterns', []):
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(relative_path, pattern):
            return True
        if pattern.endswith('/'):
            if fnmatch.fnmatch(path_str + '/', pattern) or fnmatch.fnmatch(relative_path + '/', pattern):
                return True
    
    return False

def get_files_content(directory, output_file, config):
    """
    Get content of all files in the specified directory and write to output file,
    excluding files based on config.
    """
    try:
        directory = Path(directory).resolve()
        if not directory.exists():
            print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        with open(output_file, 'w', encoding='utf-8') as out:
            for root, dirs, files in os.walk(directory):
                # Remove excluded directories
                dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, config, directory)]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip if file should be excluded
                    if should_exclude(file_path, config, directory):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Write file path as comment and then content
                        relative_path = file_path.relative_to(directory)
                        out.write(f"### File: {relative_path}\n\n")
                        out.write(content)
                        out.write("\n\n")
                    except (UnicodeDecodeError, IOError) as e:
                        print(f"Warning: Skipping {file_path}: {str(e)}", file=sys.stderr)
                        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def create_default_config(path):
    """Create a default configuration file."""
    default_config = {
        'exclude_files': [
            # Add specific files to exclude
            "config.json",
            "secret.key"
        ],
        'exclude_patterns': [
            "*.test.js",
            "__pycache__/",
            "node_modules/",
            ".git/",
            "*.log"
        ],
        'exclude_extensions': [
            ".pyc",
            ".pyo",
            ".pyd",
            ".so",
            ".dll",
            ".class",
            ".exe"
        ]
    }
    
    try:
        with open(path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        print(f"Created default configuration file at: {path}")
    except Exception as e:
        print(f"Error creating default config: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Combine code files from a directory into a single file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('directory', help='Directory containing the code', nargs='?' if '--create-config' in sys.argv else None)
    parser.add_argument('--output', default='combined_code.txt', help='Output file path')
    parser.add_argument('--config', default='code_combiner_config.yaml', help='Configuration file path')
    parser.add_argument('--create-config', action='store_true', help='Create a default configuration file')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_default_config(args.config)
        return
    
    # Load configuration
    config = load_config(args.config)
    
    # Combine files
    get_files_content(args.directory, args.output, config)
    print(f"Combined code written to: {args.output}")

if __name__ == '__main__':
    main()