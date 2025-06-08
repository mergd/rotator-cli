# Rotator CLI

A command-line tool for automatically detecting and fixing image orientation using machine learning.

## Features

- =
 Automatic image orientation detection using ML models
- = Batch processing of directories (recursive or single-level)
- =� Automatic backup creation before rotation
- <� Dry-run mode to preview changes
- =� Progress tracking with detailed summaries
- <� Support for common image formats (JPEG, PNG, BMP, TIFF)

## Installation

### Homebrew (macOS/Linux)

```bash
# Once published to Homebrew
brew install rotator-cli
```

### PyPI

```bash
# Once published to PyPI
pip install rotator-cli
```

### From source

```bash
git clone https://github.com/mergd/rotator-cli
cd rotator-cli
make install
```

### Development installation

```bash
git clone https://github.com/mergd/rotator-cli
cd rotator-cli
make install-dev
```

## Usage

### Basic usage

```bash
# Process all images in a directory
rotator /path/to/images

# Preview changes without modifying files
rotator --dry-run /path/to/images

# Process only current directory (no subdirectories)
rotator --no-recursive /path/to/images

# Skip backup file creation
rotator --no-backup /path/to/images

# Verbose output
rotator --verbose /path/to/images
```

### Advanced options

```bash
# Use a different ML model
rotator --model swsl_resnext50_32x4d /path/to/images

# Combine options
rotator --dry-run --verbose --no-backup /path/to/images
```

## How it works

1. **Scans** the specified directory for supported image files
2. **Detects** rotation using the `check_orientation` ML model
3. **Rotates** images that need correction (0�, 90�, 180�, 270�)
4. **Creates backups** (unless disabled) before modifying originals
5. **Reports** processing results and statistics

## Development

### Setup

```bash
# Clone and setup development environment
git clone https://github.com/mergd/rotator-cli
cd rotator-cli
make install-dev

# Run linting and formatting
make lint
make format

# Run tests
make test

# Build distribution
make build
```

### Code quality

This project uses modern Python tooling:

- **uv** for dependency management and builds
- **ruff** for linting and formatting
- **pyproject.toml** for configuration
- **Makefile** for common tasks

### Publishing to Homebrew

1. Create a GitHub release with a tag (e.g., `v0.1.0`)
2. Update the Homebrew formula in `rotator_cli/homebrew_formula.rb` with correct SHA256 values
3. Submit a PR to the [homebrew-core](https://github.com/Homebrew/homebrew-core) repository

### Distribution checklist

- [ ] Update version in `pyproject.toml` and `rotator_cli/__init__.py`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Run tests: `make test`
- [ ] Build package: `make build`  
- [ ] Create GitHub release with built artifacts
- [ ] Update Homebrew formula with release SHA256
- [ ] Publish to PyPI: `make publish`

## License

MIT License - see LICENSE file for details.