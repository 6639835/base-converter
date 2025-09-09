# Base Converter

[![CI](https://github.com/6639835/base-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/6639835/base-converter/actions/workflows/ci.yml)
[![Build](https://github.com/6639835/base-converter/actions/workflows/build.yml/badge.svg)](https://github.com/6639835/base-converter/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/6639835/base-converter/branch/main/graph/badge.svg)](https://codecov.io/gh/6639835/base-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A comprehensive, cross-platform base conversion utility with both command-line and graphical interfaces. Convert numbers between any bases from 2 to 36, perform arithmetic operations, and process batch conversions with ease.

## ✨ Features

### 🔢 **Comprehensive Base Support**
- Convert between **any bases from 2 to 36**
- Support for **Binary (2), Octal (8), Decimal (10), Hexadecimal (16)** and all intermediate bases
- Automatic base detection from prefixes (`0x`, `0b`, `0o`)
- Input validation with helpful error messages

### 🖥️ **Dual Interface**
- **Graphical Interface**: User-friendly GUI built with tkinter
- **Command-Line Interface**: Powerful CLI for automation and scripting
- **Interactive Mode**: Real-time conversion in terminal

### ⚡ **Advanced Operations**
- **Arithmetic Operations**: Add, subtract, multiply, divide in any base
- **Batch Processing**: Convert multiple numbers from files
- **Conversion Tables**: View numbers in all common bases simultaneously
- **Format Options**: Add prefixes, separators, and control case

### 🔍 **Smart Features**
- **Input Validation**: Comprehensive error checking and suggestions
- **Base Detection**: Automatic detection of number base
- **History Tracking**: Keep track of conversion history
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

#### Option 1: Download Pre-built Executables
1. Go to [Releases](https://github.com/6639835/base-converter/releases)
2. Download the appropriate package for your platform:
   - **Windows**: `base-converter-windows-x64.zip`
   - **macOS**: `base-converter-macos-x64.tar.gz` (Intel) or `base-converter-macos-arm64.tar.gz` (Apple Silicon)
   - **Linux**: `base-converter-linux-x64.tar.gz`
3. Extract and run the installer script

#### Option 2: Install from Source
```bash
git clone https://github.com/6639835/base-converter.git
cd base-converter
pip install -e .
```

#### Option 3: Install via pip (when available)
```bash
pip install base-converter
```

### Basic Usage

#### Graphical Interface
```bash
base-converter --gui
```

#### Command Line Examples
```bash
# Convert binary to decimal
base-converter 1010 -f 2 -t 10
# Output: 1010 (base 2) = 10 (base 10)

# Convert hex to binary
base-converter FF -f 16 -t 2
# Output: FF (base 16) = 11111111 (base 2)

# Show conversion table
base-converter 255 --table
# Shows 255 in binary, octal, decimal, and hex

# Interactive mode
base-converter --interactive
```

## 📖 Detailed Usage

### Command Line Interface

#### Basic Conversion
```bash
base-converter <number> -f <from_base> -t <to_base>
```

#### Options
- `-f, --from-base`: Source base (2-36, default: 10)
- `-t, --to-base`: Target base (2-36, default: 2)
- `--table`: Show conversion table for common bases
- `--format`: Add digit separators for readability
- `--prefix`: Add standard prefixes (0x, 0b, 0o)
- `--detect-base`: Automatically detect input base
- `--validate`: Validate conversion by converting back
- `--info`: Show detailed conversion information
- `--interactive`: Start interactive mode
- `--quiet`: Show only the result
- `--verbose`: Show detailed output

#### Advanced Features

**Arithmetic Operations**
```bash
# Add two binary numbers
base-converter 1010 --arithmetic + --second-number 1100 -f 2
# Result: 10110

# Multiply hex numbers
base-converter A --arithmetic * --second-number B -f 16
# Result: 6E
```

**Batch Processing**
```bash
# Convert numbers from file
base-converter --batch numbers.txt -f 10 -t 16

# File format (numbers.txt):
# 255
# 256
# 1024
```

**Base Detection**
```bash
base-converter 0xFF --detect-base -t 2
# Detects hex, converts to binary: 11111111
```

### Graphical Interface

Launch the GUI with `base-converter --gui` for:

- **Visual number input** with real-time validation
- **Base selection** via dropdown menus or quick buttons
- **Conversion history** with export functionality
- **Arithmetic calculator** for operations in any base
- **Batch converter** with file import
- **Formatting options** for output customization

## 📊 Examples

### Common Conversions

```bash
# Binary to Decimal
base-converter 1111 -f 2 -t 10        # Result: 15

# Decimal to Hex
base-converter 255 -f 10 -t 16        # Result: FF

# Octal to Binary
base-converter 777 -f 8 -t 2          # Result: 111111111

# Custom base conversion
base-converter ZZ -f 36 -t 10         # Result: 1295
```

### Advanced Examples

```bash
# With formatting and prefixes
base-converter 255 -f 10 -t 2 --format --prefix
# Result: 0b1111_1111

# Conversion table
base-converter 42 --table
# Shows:
# Binary:      101010
# Octal:       52
# Decimal:     42
# Hexadecimal: 2A

# Arithmetic with validation
base-converter 1010 --arithmetic + --second-number 0110 -f 2 --validate
# Shows calculation and validates result
```

## 🛠️ Development

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)
- Optional: pytest for running tests

### Building from Source

1. **Clone the repository**
```bash
git clone https://github.com/6639835/base-converter.git
cd base-converter
```

2. **Install development dependencies**
```bash
pip install -e .
pip install pytest pytest-cov pyinstaller
```

3. **Run tests**
```bash
pytest tests/ -v --cov=src
```

4. **Build executable**
```bash
python build.py
```

### Project Structure
```
base-converter/
├── src/                    # Source code
│   ├── converter.py       # Core conversion logic
│   ├── validation.py      # Input validation
│   ├── cli.py            # Command-line interface
│   ├── gui.py            # Graphical interface
│   └── main.py           # Main entry point
├── tests/                 # Test suite
├── .github/workflows/     # CI/CD pipelines
├── build.py              # Build script
└── README.md            # Documentation
```

## 🧪 Testing

The project includes comprehensive tests covering:

- **Unit tests** for all core functions
- **Integration tests** for CLI and GUI components
- **Cross-platform compatibility** tests
- **Error handling** and validation tests

Run tests with:
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m cli          # CLI tests only
```

## 🔧 Configuration

### Environment Variables
- `DISPLAY`: For GUI on Linux systems (automatically handled)

### Configuration Files
- `pytest.ini`: Test configuration
- `pyproject.toml`: Project metadata
- `.github/workflows/`: CI/CD configuration

## 🚦 CI/CD Pipeline

The project uses GitHub Actions for:

1. **Continuous Integration**
   - Tests on Python 3.7-3.11
   - Cross-platform testing (Windows, macOS, Linux)
   - Code quality checks (linting, formatting, security)

2. **Automated Building**
   - Creates executables for all platforms
   - Packages with installers
   - Uploads artifacts

3. **Release Automation**
   - Creates GitHub releases
   - Uploads platform-specific packages
   - Updates version numbers

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and add tests
4. **Run the test suite** (`pytest`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines
- Write tests for new features
- Follow the existing code style
- Update documentation as needed
- Ensure cross-platform compatibility

## 📋 Supported Bases

| Base | Name | Digits | Example |
|------|------|---------|---------|
| 2 | Binary | 0-1 | 1010 |
| 8 | Octal | 0-7 | 777 |
| 10 | Decimal | 0-9 | 255 |
| 16 | Hexadecimal | 0-9, A-F | FF |
| 36 | Base36 | 0-9, A-Z | ZZ |

*All bases from 2 to 36 are supported*

## 🐛 Troubleshooting

### Common Issues

**GUI doesn't start on Linux**
```bash
# Install tkinter
sudo apt-get install python3-tk

# For headless systems
export DISPLAY=:0
```

**Permission denied on Unix systems**
```bash
chmod +x base-converter
```

**Import errors**
```bash
# Ensure all dependencies are installed
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Built with Python and tkinter for cross-platform compatibility
- Inspired by the need for a comprehensive, user-friendly base converter
- Thanks to all contributors and users who provide feedback

## 🔗 Links

- **Repository**: [https://github.com/6639835/base-converter](https://github.com/6639835/base-converter)
- **Issues**: [https://github.com/6639835/base-converter/issues](https://github.com/6639835/base-converter/issues)
- **Releases**: [https://github.com/6639835/base-converter/releases](https://github.com/6639835/base-converter/releases)

---

**Made with ❤️ by [6639835](https://github.com/6639835)**
