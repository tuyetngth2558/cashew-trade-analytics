# Contributing to Cashew Trade Analytics

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the feature and its benefits
- Provide examples of how it would be used

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Include type hints where appropriate
   - Write tests for new functionality

4. **Test your changes**:
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```
   Use clear, descriptive commit messages

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**:
   - Describe what changes you made and why
   - Reference any related issues
   - Ensure all tests pass

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/cashew-trade-analytics.git
cd cashew-trade-analytics
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
pytest tests/ -v
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Keep functions focused and small
- Maximum line length: 100 characters

### Documentation
- Add docstrings to all public functions/classes
- Update README.md if adding features
- Include inline comments for complex logic

### Testing
- Write unit tests for new functions
- Maintain test coverage above 80%
- Test edge cases and error conditions

## Project Structure

```
src/              # Core modules
tests/            # Test files
dashboard/        # Streamlit app
scripts/          # Utility scripts
docs/             # Documentation
```

## Questions?

Feel free to open an issue for any questions about contributing!
