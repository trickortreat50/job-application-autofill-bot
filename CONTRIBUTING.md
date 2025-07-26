# Contributing to Job Application Auto-Fill Bot

Thank you for your interest in contributing to the Job Application Auto-Fill Bot! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/yourusername/job-application-autofill-bot/issues) section
2. If not, create a new issue with:
   - A clear and descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your operating system and Python version
   - Any error messages or logs

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - A clear description of the feature
   - Why this feature would be useful
   - Any implementation ideas you have

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Submit a pull request with a clear description

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/job-application-autofill-bot.git
   cd job-application-autofill-bot
   ```

2. Set up the development environment:
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using conda
   conda env create -f environment.yml
   conda activate job-autofill-bot
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Add comments for complex logic

## Testing

Before submitting a pull request:

1. Run the existing tests:
   ```bash
   python -m pytest tests/
   ```

2. Test the application manually:
   ```bash
   python main.py
   ```

3. Test the command-line interface:
   ```bash
   python main.py --cli
   ```

## Pull Request Guidelines

1. Keep pull requests focused on a single feature or bug fix
2. Include a clear description of what the PR does
3. Reference any related issues
4. Ensure all tests pass
5. Update documentation if needed

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainers directly

Thank you for contributing to make this tool better for everyone! 