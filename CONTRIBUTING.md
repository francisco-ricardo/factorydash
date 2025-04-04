# Contributing to FactoryDash

Thank you for your interest in contributing to FactoryDash! This document 
outlines the guidelines and best practices for contributing to the project. 
By following these guidelines, you help ensure that the codebase remains 
clean, maintainable, and aligned with best practices for Django and 
Python development.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Code of Conduct](#code-of-conduct)
3. [Development Guidelines](#development-guidelines)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Style Guide](#style-guide)
7. [Commit Messages](#commit-messages)

---

## Getting Started

1. **Fork the Repository**:  
   Start by forking the repository to your GitHub account.

2. **Clone the Repository**:  
   Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/factorydash.git
   cd factorydash
   ```

3. **Set Up the Environment**:  
   Follow the instructions in the `README.md` file to set up the local 
   development environment using Docker or your preferred method.

4. **Create a Branch**:  
   Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## Code of Conduct

By contributing, you agree to uphold the project's 
[Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, collaborative, 
and professional in all interactions.

---

## Development Guidelines

1. **Follow Clean Code Principles**:
   - Write readable, maintainable, and well-documented code.
   - Use meaningful variable and function names.
   - Avoid hardcoding values; use environment variables or configuration files.

2. **Adhere to Django Best Practices**:
   - Use Django's built-in features whenever possible (e.g., `QuerySet` methods, middleware).
   - Keep views thin and business logic in models or services.
   - Use class-based views (CBVs) for better reusability and readability.
   - Avoid writing raw SQL unless absolutely necessary.

3. **Modular Design**:
   - Break down large functions or classes into smaller, reusable components.
   - Keep the code DRY (Don't Repeat Yourself).

4. **Environment Variables**:
   - Use `.env` files for sensitive configurations (e.g., `SECRET_KEY`, `DATABASE_URL`).
   - Validate environment variables in the settings file.

5. **Error Handling**:
   - Add proper error handling for edge cases.
   - Log errors using Django's logging framework.

6. **Database Migrations**:
   - Run `makemigrations` and `migrate` for any model changes.
   - Test migrations locally before submitting.

---

## Testing

1. **Write Tests**:
   - Add unit tests for all new features and bug fixes.
   - Use `pytest` and `pytest-django` for testing.

2. **Test Coverage**:
   - Ensure that your code has sufficient test coverage.
   - Run tests locally before submitting:
     ```bash
     pytest --cov=app/factorydash
     ```

3. **Mock External Dependencies**:
   - Mock external services (e.g., NIST API) in tests to avoid network dependencies.

4. **Run the Test Suite**:
   - Ensure all tests pass before submitting:
     ```bash
     pytest
     ```

---

## Submitting Changes

1. **Pull the Latest Changes**:
   - Sync your branch with the latest changes from the `main` branch:
     ```bash
     git fetch origin
     git checkout main
     git pull origin main
     git checkout feature/your-feature-name
     git merge main
     ```

2. **Push Your Changes**:
   - Push your branch to your forked repository:
     ```bash
     git push origin feature/your-feature-name
     ```

3. **Open a Pull Request**:
   - Open a pull request (PR) to the `main` branch of the original repository.
   - Provide a clear and concise description of your changes, including:
     - The problem your changes address.
     - The solution you implemented.
     - Any additional context or screenshots.

4. **Address Feedback**:
   - Be responsive to feedback from maintainers and make necessary changes.

---

## Style Guide

1. **PEP 8 Compliance**:
   - Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.
   - Use tools like `flake8` or `black` to ensure compliance:
     ```bash
     black app/factorydash
     flake8 app/factorydash
     ```

2. **Docstrings**:
   - Write PEP 257-compliant docstrings for all modules, classes, and functions.
   - Use Google-style or reStructuredText (reST) docstrings.

3. **Type Hints**:
   - Use type hints for function arguments and return values (PEP 484):
     ```python
     def fetch_data(url: str) -> dict:
         ...
     ```

4. **Imports**:
   - Follow PEP 8 import guidelines:
     - Standard library imports.
     - Third-party imports.
     - Local application imports.
   - Use absolute imports instead of relative imports.

---

## Commit Messages

1. **Format**:
   - Use the following format for commit messages:
     ```
     <type>: <short summary>

     <detailed description>
     ```

2. **Types**:
   - `feat`: A new feature.
   - `fix`: A bug fix.
   - `docs`: Documentation changes.
   - `style`: Code style changes (e.g., formatting).
   - `refactor`: Code refactoring.
   - `test`: Adding or updating tests.
   - `chore`: Maintenance tasks (e.g., updating dependencies).

3. **Examples**:
   - `feat: Add WebSocket support for real-time updates`
   - `fix: Resolve pagination bug in DashboardConsumer`
   - `docs: Update README with deployment instructions`

---

Thank you for contributing to FactoryDash!
