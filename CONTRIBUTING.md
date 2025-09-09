# Contributing to Base Converter

Thank you for your interest in contributing to Base Converter! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

- **Bug Reports**: Report issues or unexpected behavior
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Improve documentation and examples
- **Testing**: Help test on different platforms or edge cases
- **Feedback**: Provide user feedback and suggestions

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Environment Information**:
   - Operating System (Windows/macOS/Linux)
   - Python version
   - Base Converter version

2. **Steps to Reproduce**:
   - Clear, step-by-step instructions
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Additional Information**:
   - Error messages or logs
   - Minimal example code
   - Any relevant context

**Template**:
```markdown
## Environment
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Base Converter: [e.g., 1.0.0]

## Description
Brief description of the issue.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Additional Context
Any other relevant information.
```

## 💡 Feature Requests

For feature requests, please:

1. Check if the feature already exists
2. Search existing issues to avoid duplicates
3. Provide a clear description of the feature
4. Explain the use case and benefits
5. Consider implementation complexity

## 🔧 Development Setup

### Prerequisites
- Python 3.7 or higher
- git
- A code editor (VS Code, PyCharm, etc.)

### Setting up the Development Environment

1. **Fork and Clone**:
```bash
git clone https://github.com/yourusername/base-converter.git
cd base-converter
```

2. **Create Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:
```bash
pip install -e .
pip install pytest pytest-cov pytest-mock pyinstaller
pip install flake8 black isort mypy  # For code quality
```

4. **Verify Installation**:
```bash
python -m src.cli --help
python -m src.gui  # Test GUI (may not work in headless environments)
pytest tests/
```

## 🏗️ Development Workflow

### Code Style Guidelines

We follow these coding standards:

- **PEP 8** for Python code style
- **Type hints** for function signatures
- **Docstrings** for all public functions and classes
- **Clear variable names** and comments for complex logic

### Code Formatting

We use automated tools for consistent formatting:

```bash
# Format code
black src/ tests/

# Sort imports  
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Writing Tests

All new features should include tests:

1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test component interactions
3. **CLI Tests**: Test command-line interface
4. **GUI Tests**: Test graphical interface (where possible)

**Test Structure**:
```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test input"
    expected = "expected result"
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected
```

**Running Tests**:
```bash
# All tests
pytest

# Specific test file
pytest tests/test_converter.py

# With coverage
pytest --cov=src --cov-report=html

# Specific test categories
pytest -m unit
pytest -m integration
```

### Adding New Features

1. **Create Feature Branch**:
```bash
git checkout -b feature/new-feature-name
```

2. **Implement Feature**:
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation

3. **Test Thoroughly**:
```bash
pytest tests/
python build.py  # Test building
```

4. **Commit Changes**:
```bash
git add .
git commit -m "feat: add new feature description"
```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples**:
```
feat: add support for base 64 encoding
fix: resolve GUI crash on invalid input
docs: update installation instructions
test: add tests for arithmetic operations
```

## 📝 Pull Request Process

1. **Create Pull Request**:
   - Use a descriptive title
   - Reference related issues
   - Provide clear description of changes

2. **Pull Request Template**:
```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Existing tests pass
- [ ] New tests added (if applicable)
- [ ] Tested on multiple platforms

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors

## Related Issues
Closes #123
Related to #456
```

3. **Review Process**:
   - Automated CI checks must pass
   - Code review by maintainers
   - Address feedback and requested changes
   - Maintain clean commit history

## 🧪 Testing Guidelines

### Test Categories

- **Unit Tests** (`@pytest.mark.unit`): Test individual functions
- **Integration Tests** (`@pytest.mark.integration`): Test component interactions
- **CLI Tests** (`@pytest.mark.cli`): Test command-line interface
- **GUI Tests** (`@pytest.mark.gui`): Test graphical interface

### Test Best Practices

1. **Clear Test Names**: Use descriptive test function names
2. **Arrange-Act-Assert**: Follow the AAA pattern
3. **Test Edge Cases**: Include boundary conditions and error cases
4. **Mock External Dependencies**: Use mocks for file I/O, network calls, etc.
5. **Parametrized Tests**: Use `@pytest.mark.parametrize` for multiple inputs

### Example Test:
```python
import pytest
from src.converter import BaseConverter

class TestBaseConverter:
    def setup_method(self):
        self.converter = BaseConverter()
    
    @pytest.mark.parametrize("number,base,expected", [
        ("1010", 2, 10),
        ("FF", 16, 255),
        ("777", 8, 511),
    ])
    def test_base_to_decimal(self, number, base, expected):
        """Test conversion from various bases to decimal."""
        result = self.converter.base_to_decimal(number, base)
        assert result == expected
```

## 📚 Documentation Guidelines

### Code Documentation

- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Include type hints for all function parameters
- **Comments**: Explain complex logic and algorithms
- **Examples**: Include usage examples in docstrings

**Docstring Example**:
```python
def convert_base(self, number: str, source_base: int, target_base: int) -> str:
    """
    Convert a number from one base to another.
    
    Args:
        number: The number string to convert
        source_base: The source base (2-36)
        target_base: The target base (2-36)
        
    Returns:
        The converted number in target base
        
    Raises:
        ValueError: If the number is invalid for the source base
        
    Example:
        >>> converter = BaseConverter()
        >>> converter.convert_base("1010", 2, 10)
        "10"
    """
```

### User Documentation

- **README**: Keep the main README updated
- **Examples**: Provide practical examples
- **Troubleshooting**: Document common issues and solutions
- **API Reference**: Document public APIs

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

1. Update version numbers in:
   - `setup.py`
   - `pyproject.toml`
   - `src/__init__.py`

2. Update `CHANGELOG.md` with new version

3. Create and push version tag:
```bash
git tag v1.1.0
git push origin v1.1.0
```

4. GitHub Actions will automatically:
   - Run tests
   - Build executables
   - Create GitHub release
   - Upload assets

## 🌟 Recognition

Contributors are recognized in several ways:

- **Contributors Section**: Listed in README
- **Changelog**: Contributions noted in version history
- **GitHub**: Contributor statistics and graphs
- **Releases**: Major contributors mentioned in release notes

## 📞 Getting Help

If you need help with development:

1. **Check Documentation**: README, API docs, and code comments
2. **Search Issues**: Existing issues might have solutions
3. **Create Discussion**: Use GitHub Discussions for questions
4. **Contact Maintainers**: Reach out via GitHub issues

## 📄 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you agree to uphold this code.

## 🙏 Thank You

Thank you for contributing to Base Converter! Your contributions help make this tool better for everyone.

---

For questions about contributing, please create an issue or discussion on GitHub.
