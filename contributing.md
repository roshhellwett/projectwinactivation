# Contributing to projectwinactivation

Thank you for your interest in contributing to **projectwinactivation**! We welcome contributions from the community. This guide will help you get started with development.

---

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Building the Package](#building-the-package)
- [Coding Standards](#coding-standards)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Review Criteria](#code-review-criteria)
- [Project Structure](#project-structure)
- [Questions?](#questions)

---

## Ways to Contribute

- **Bug Reports:** Report bugs via GitHub Issues
- **Feature Requests:** Suggest new features or improvements
- **Code Contributions:** Submit pull requests with bug fixes or new features
- **Documentation:** Improve or translate documentation
- **Testing:** Test the toolkit on different Windows versions

---

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Windows 10/11
- Git
- pip (Python package manager)

### Setup Instructions

### 1. Fork the Repository

```bash
git clone https://github.com/your-username/projectwinactivation.git
cd projectwinactivation
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install in development mode with all dev tools
pip install -e ".[dev]"
```

### 4. Install Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

---

## Running Tests

```bash
# Run all tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=src/projectwinactivation

# Run specific test file
pytest tests/test_utils.py -v
```

---

## Building the Package

### Build Distribution Packages

```bash
# Install build tools
pip install build

# Build the package
python -m build

# The packages will be in the 'dist/' directory
```

### Build Outputs

After building, you'll find:
- `dist/projectwinactivation-1.0.0-py3-none-any.whl` — Wheel package
- `dist/projectwinactivation-1.0.0.tar.gz` — Source distribution

### Install Locally for Testing

```bash
# Install from local build
pip install dist/projectwinactivation-1.0.0-py3-none-any.whl

# Or install in editable mode
pip install -e .
```

---

## Coding Standards

### General Guidelines

1. **Follow PEP 8** — Use consistent Python style
2. **Type Hints** — Add type hints where possible
3. **Docstrings** — Document functions and classes using Google-style docstrings
4. **Tests** — Write tests for new functionality

### Code Style Example

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something goes wrong.
    """
    # Implementation
    return True
```

### File Organization

- Keep functions small and focused
- Group related functionality in modules
- Use descriptive variable names
- Remove unused imports

---

## Branch Naming

Use the following conventions:

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/` | `feature/new-network-tool` |
| Bug Fix | `fix/` | `fix/service-manager-error` |
| Documentation | `docs/` | `docs/update-readme` |
| Refactor | `refactor/` | `refactor/clean-utils` |
| Hotfix | `hotfix/` | `hotfix/urgent-fix` |

---

## Commit Messages

Use clear, descriptive commit messages:

```
type: Brief description (50 chars max)

Detailed explanation if needed (wrap at 72 chars)

Closes #123
```

### Common Types

```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Formatting, missing semi colons, etc
refactor: Code refactoring
test:     Adding tests
chore:    Maintenance tasks
```

### Examples

```
feat: Add network diagnostics module
fix: Correct driver listing timeout
docs: Update README with installation steps
refactor: Improve error handling in activation module
test: Add tests for system_info module
```

---

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: Add new utility module"
```

### 3. Push to Your Fork

```bash
git push origin feature/my-new-feature
```

### 4. Open a Pull Request

- Use a clear title and description
- Reference any related issues (e.g., "Closes #123")
- Include screenshots for UI changes
- Wait for review

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
Describe how you tested the changes.

## Checklist
- [ ] Code follows PEP 8
- [ ] Type hints added
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Works on Windows 10/11
```

---

## Code Review Criteria

Your code will be reviewed based on:

| Criteria | Description |
|----------|-------------|
| **Functionality** | Does it work as intended? |
| **Code Quality** | Is it clean and well-organized? |
| **Testing** | Are there adequate tests? |
| **Documentation** | Is it properly documented? |
| **Compatibility** | Does it work on Windows 10/11? |
| **Performance** | Does it handle resources efficiently? |

---

## Project Structure

```
projectwinactivation/
├── src/
│   └── projectwinactivation/
│       ├── __init__.py           # Package initialization
│       ├── __main__.py           # Entry point
│       ├── __version__.py        # Version info
│       ├── cli.py                # CLI interface
│       ├── assets/
│       │   └── banners.py        # ASCII banners
│       └── utils/
│           ├── __init__.py       # Utils initialization
│           ├── activation.py      # Windows activation
│           ├── disk.py            # Disk cleanup
│           ├── drivers.py         # Driver management
│           ├── firewall.py        # Firewall management
│           ├── network.py         # Network diagnostics
│           ├── processes.py       # Process monitor
│           ├── product_key.py     # Product key finder
│           ├── services.py        # Service manager
│           ├── startup.py         # Startup manager
│           ├── system_info.py     # System information
│           └── updates.py         # Windows update
├── tests/
│   └── test_utils.py            # Unit tests
├── pyproject.toml               # Package configuration
├── README.md                    # User documentation
├── LICENSE                      # MIT License
├── security.md                  # Security policy
└── contributing.md              # This file
```

---

## Questions?

If you have questions, feel free to:

- Open an issue for discussion
- Email: roshhellwett@icloud.com

---

## License

By contributing to projectwinactivation, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! Your contributions help make this project better for everyone.

**Happy coding!**

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/)
