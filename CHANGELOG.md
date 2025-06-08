# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-XX

### Added
- Initial release of Rotator CLI
- Automatic image orientation detection using ML models
- Batch processing with recursive directory scanning
- Progress tracking with tqdm
- Backup file creation before rotation
- Dry-run mode for previewing changes
- Verbose output option
- Support for JPEG, PNG, BMP, TIFF image formats
- Modern Python toolchain with uv, ruff, and pyproject.toml
- Homebrew formula for easy installation
- Comprehensive CLI with click framework

### Features
- Uses check_orientation library for ML-based rotation detection
- Supports 0°, 90°, 180°, 270° rotation corrections
- Cross-platform compatibility (macOS, Linux, Windows)
- Self-contained package suitable for distribution