# Tox - Multi-Environment Testing in Python

A comprehensive guide and practical examples for using **Tox** to automate testing across multiple Python environments and configurations.

## What is Tox?

Tox is a command-line tool that automates and standardizes testing in Python projects. It creates isolated virtual environments, installs your package and its dependencies, and runs your test suite across different Python versions and configurations.

### Key Benefits:
- **Environment Isolation**: Each test runs in a clean virtual environment
- **Multi-Version Testing**: Test across different Python versions simultaneously
- **Reproducible Results**: Same testing environment every time
- **CI/CD Integration**: Perfect for automated pipelines
- **Standardization**: Consistent testing workflow for teams

## How Tox Works

```
1. Reads configuration from tox.ini or pyproject.toml
2. Creates virtual environments for each test environment
3. Installs your package and dependencies
4. Runs specified commands (usually tests)
5. Reports results for all environments
```

## Project Structure

```
tox/
├── math_utils/                 # Basic example project demonstrating Tox usage
│   ├── app/
│   │   ├── __init__.py
│   │   └── calculator.py       # Simple calculator functions
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_calculator.py  # Comprehensive test suite
│   ├── pyproject.toml          # Modern Python project config with Tox
│   ├── requirements.txt
│   └── README.md               # Detailed project documentation
├── math_utils_api/             # Advanced Flask API project with Tox
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py             # Flask REST API endpoints
│   │   └── calculator.py      # Calculator business logic
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py        # API endpoint tests
│   │   └── test_calculator.py # Unit tests
│   ├── pyproject.toml         # Advanced Tox config with multiple environments
│   ├── requirements.txt
│   └── README.md              # Complete API documentation
└── README.md                  # This file
```

## Installation

### Method 1: Using pipx (Recommended)
```bash
# Install pipx first if you don't have it
python -m pip install --user pipx

# Install tox in isolated environment
pipx install tox

# Verify installation
tox --version
```

### Method 2: Using pip
```bash
# Install tox globally
pip install tox

# Or in a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install tox
```

## Configuration

### Using pyproject.toml (Modern Approach)
```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py38,py39,py310,py311
isolated_build = true
skip_missing_interpreters = true

[testenv]
deps =
    pytest>=7.0.0
    pytest-cov
commands =
    pytest tests/ -v --cov=app

[testenv:lint]
deps =
    flake8
    black
    isort
commands =
    flake8 app tests
    black --check app tests
    isort --check-only app tests

[testenv:docs]
deps =
    sphinx
    sphinx-rtd-theme
commands =
    sphinx-build -b html docs docs/_build/html
"""
```

### Using tox.ini (Traditional Approach)
```ini
[tox]
envlist = py38,py39,py310,py311
isolated_build = true
skip_missing_interpreters = true

[testenv]
deps =
    pytest>=7.0.0
    pytest-cov
commands =
    pytest tests/ -v --cov=app

[testenv:lint]
deps =
    flake8
    black
    isort
commands =
    flake8 app tests
    black --check app tests
    isort --check-only app tests

[testenv:docs]
deps =
    sphinx
    sphinx-rtd-theme
commands =
    sphinx-build -b html docs docs/_build/html
```

## Usage Examples

### Basic Commands

```bash
# Run all configured environments
tox

# Run specific environment
tox -e py39

# Run multiple specific environments
tox -e py38,py39

# List available environments
tox -l

# Run with verbose output
tox -v

# Recreate environments (clean install)
tox -r
```

### Advanced Usage

```bash
# Run specific environment with custom commands
tox -e py39 -- --maxfail=1

# Run tests in parallel
tox -p auto

# Skip missing Python interpreters
tox --skip-missing-interpreters

# Run only specific test environments
tox -e lint,py39

# Run with coverage report
tox -e py39 -- --cov-report=html
```

## Common Configuration Patterns

### 1. Multi-Python Version Testing
```ini
[tox]
envlist = py37,py38,py39,py310,py311

[testenv]
deps = pytest
commands = pytest tests/
```

### 2. Different Test Configurations
```ini
[tox]
envlist = py39,py39-django32,py39-django40

[testenv]
deps = pytest

[testenv:py39-django32]
deps =
    pytest
    django>=3.2,<3.3

[testenv:py39-django40]
deps =
    pytest
    django>=4.0,<4.1
commands = pytest tests/
```

### 3. Quality Assurance Suite
```ini
[tox]
envlist = py39,lint,type-check,security

[testenv]
deps = pytest
commands = pytest tests/

[testenv:lint]
deps =
    flake8
    black
    isort
commands =
    flake8 src tests
    black --check src tests
    isort --check-only src tests

[testenv:type-check]
deps =
    mypy
    types-requests
commands = mypy src

[testenv:security]
deps = bandit
commands = bandit -r src/
```

### 4. Documentation Building
```ini
[testenv:docs]
deps =
    sphinx>=4.0
    sphinx-rtd-theme
    myst-parser
commands =
    sphinx-build -b html docs docs/_build/html
    sphinx-build -b linkcheck docs docs/_build/linkcheck
```

## Environment Variables

```ini
[testenv]
# Set environment variables
setenv =
    PYTHONPATH = {toxinidir}/src
    DJANGO_SETTINGS_MODULE = myproject.settings.test

# Pass through environment variables from host
passenv =
    HOME
    USER
    CI
    GITHUB_*
```

## Integration with CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install tox
      run: pip install tox
    - name: Run tox
      run: tox -e py
```

### GitLab CI
```yaml
test:
  image: python:3.9
  script:
    - pip install tox
    - tox
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
```

## 📊 Best Practices

### 1. **Environment Naming**
- Use descriptive names: `py39-django32`, `py38-minimal`
- Follow consistent patterns
- Include version numbers when relevant

### 2. **Dependency Management**
```ini
[testenv]
deps =
    # Exact versions for reproducible builds
    pytest==7.1.2
    requests>=2.28.0,<3.0.0

    # Or use requirements files
    -r requirements/test.txt
```

### 3. **Performance Optimization**
```ini
[tox]
# Skip missing interpreters instead of failing
skip_missing_interpreters = true

# Enable parallel execution
parallel_show_output = true

[testenv]
# Skip package installation for faster runs
skip_install = true

# Use wheelhouse for faster installs
pip_pre = true
```

### 4. **Isolated Builds**
```ini
[tox]
isolated_build = true  # Use PEP 517/518 build system
```

### 5. **Custom Commands**
```ini
[testenv:format]
skip_install = true
deps =
    black
    isort
commands =
    black src tests
    isort src tests
```

## Troubleshooting

### Common Issues:

**1. "Python interpreter not found"**
```bash
# Install missing Python version or skip
tox --skip-missing-interpreters
```

**2. "Package installation fails"**
```bash
# Recreate environments
tox -r

# Check dependency conflicts
tox -e py39 -- --no-deps
```

**3. "Tests pass locally but fail in tox"**
- Check environment isolation
- Verify all dependencies are listed
- Ensure no reliance on system packages

**4. "Slow execution"**
```bash
# Use parallel execution
tox -p auto

# Skip reinstalls when possible
tox --skip-pkg-install
```

## Advanced Features

### 1. **Conditional Dependencies**
```ini
[testenv]
deps =
    pytest
    coverage
    {py38,py39}: typing-extensions
    {py310,py311}: newer-package>=2.0
```

### 2. **Factor-Conditional Settings**
```ini
[tox]
envlist = py{38,39,310}-django{32,40}

[testenv]
deps =
    pytest
    django32: django>=3.2,<3.3
    django40: django>=4.0,<4.1
```

### 3. **Custom Test Runners**
```ini
[testenv]
runner = pytest-xdist
commands = pytest -n auto tests/
```

## 🎓 Learning Projects

### math_utils - Basic Tox Usage
The `math_utils/` directory contains a foundational example project demonstrating:
- Basic Tox configuration in `pyproject.toml`
- Simple calculator functions with comprehensive tests
- Error handling and edge case testing
- Python package structure best practices

**Quick Start:**
```bash
cd math_utils/
tox                    # Run all tests
tox -e py             # Run in current Python version
tox -l                # List available environments
```

### math_utils_api - Advanced Tox with Flask API
The `math_utils_api/` directory showcases advanced Tox usage with a production-ready Flask API:
- **Multi-Environment Testing**: Different Python versions and dependency combinations
- **Code Quality Pipeline**: Integrated linting, formatting, and coverage
- **Flask API Testing**: Comprehensive endpoint and error handling tests
- **Production Features**: Health checks, error handlers, input validation
- **Advanced Tox Config**: Lint, coverage, and formatting environments

**Key Features:**
- REST API endpoints for mathematical operations
- Comprehensive error handling and validation
- 86% test coverage with detailed reporting
- Multi-environment testing (py38-311 with different dependency versions)
- Code quality tools (flake8, black, isort)
- Production-ready Flask application

**Quick Start:**
```bash
cd math_utils_api/

# Run all test environments
tox

# Run specific environments
tox -e py39-reqslatest    # Test with latest dependencies
tox -e lint               # Code quality checks
tox -e coverage           # Coverage reporting
tox -e format             # Format code

# Run the Flask API
export FLASK_APP=app.api
flask run                 # API available at http://localhost:5000
```

**API Endpoints:**
- `POST /add` - Addition
- `POST /subtract` - Subtraction  
- `POST /multiply` - Multiplication
- `POST /divide` - Division (with zero-division handling)
- `GET /` - Health check with service info
- `GET /health` - Simple health check

## Resources

### Official Documentation:
- [Tox Documentation](https://tox.readthedocs.io/)
- [PyProject.toml Guide](https://peps.python.org/pep-0621/)

### Complementary Tools:
- **pytest**: Modern Python testing framework
- **coverage**: Code coverage measurement
- **pre-commit**: Git hooks for code quality
- **nox**: Alternative to Tox with Python configuration

### Tutorials:
- [Tox Tutorial](https://tox.readthedocs.io/en/latest/tutorial.html)
- [Testing with Tox and GitHub Actions](https://hynek.me/articles/python-github-actions/)

## 🚀 Next Steps

### For Beginners:
1. **Start with math_utils** to understand basic Tox concepts
2. **Explore simple configurations** and single-environment testing
3. **Practice writing tests** with pytest basics

### For Intermediate Users:
1. **Study math_utils_api** for advanced Tox patterns
2. **Set up multi-environment testing** for your projects
3. **Integrate code quality tools** (linting, formatting, coverage)
4. **Configure CI/CD pipelines** with Tox

### For Advanced Users:
1. **Experiment with complex dependency matrices**
2. **Add security scanning** and performance testing environments
3. **Create custom Tox plugins** and extensions
4. **Implement advanced CI/CD workflows**

### Recommended Learning Path:
1. **math_utils** → Learn Tox fundamentals
2. **math_utils_api** → Master advanced configurations
3. **Your own projects** → Apply learnings to real-world scenarios

---

*Happy Testing with Tox! 🚀🧪*

Remember: Tox is not just about testing—it's about creating reproducible, reliable development workflows that scale with your team and projects.
