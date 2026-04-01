# Contributing to projectwinactivation

Thank you for your interest in contributing to projectwinactivation! We welcome contributions from the community.

## Ways to Contribute

- **Bug Reports:** Report bugs via GitHub Issues
- **Feature Requests:** Suggest new features or improvements
- **Code Contributions:** Submit pull requests with bug fixes or new features
- **Documentation:** Improve or translate documentation
- **Testing:** Test the toolkit on different Windows versions

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Windows 10/11
- Git

### Setup Instructions

1. **Fork the Repository**

```bash
git clone https://github.com/your-username/projectwinactivation.git
cd projectwinactivation
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -e ".[dev]"
```

4. **Install Pre-commit Hooks** (optional)

```bash
pip install pre-commit
pre-commit install
```

## Making Changes

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring

### Coding Standards

1. **Follow PEP 8** - Use consistent Python style
2. **Type Hints** - Add type hints where possible
3. **Docstrings** - Document functions and classes
4. **Tests** - Write tests for new functionality

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add network diagnostics module
fix: Correct driver listing timeout
docs: Update README with installation steps
refactor: Improve error handling in activation module
```

## Pull Request Process

1. **Create a Feature Branch**

```bash
git checkout -b feature/my-new-feature
```

2. **Make Your Changes**

```bash
git add .
git commit -m "Describe your changes"
```

3. **Push to Your Fork**

```bash
git push origin feature/my-new-feature
```

4. **Open a Pull Request**

- Use a clear title and description
- Reference any related issues
- Wait for review

## Code Review Criteria

Your code will be reviewed based on:

- [ ] Functionality - Does it work as intended?
- [ ] Code Quality - Is it clean and well-organized?
- [ ] Testing - Are there adequate tests?
- [ ] Documentation - Is it properly documented?
- [ ] Compatibility - Does it work on Windows 10/11?

## Project Structure

```
projectwinactivation/
├── src/
│   └── projectwinactivation/
│       ├── __init__.py
│       ├── __main__.py
│       ├── __version__.py
│       ├── cli.py
│       ├── utils/                  # Utility modules
│       │   ├── activation.py
│       │   ├── system_info.py
│       │   ├── drivers.py
│       │   └── ...
│       └── assets/                # Assets
│           └── banners.py
├── tests/                         # Test files
├── pyproject.toml
└── README.md
```

## Questions?

If you have questions, feel free to:

- Open an issue for discussion
- Email: roshhellwett@icloud.com

## License

By contributing to projectwinactivation, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🚀

© 2026 Zenith Open Source Projects
