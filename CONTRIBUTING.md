# Contributing to Smart Quiz App 🤝

Thank you for your interest in contributing to Smart Quiz App! We welcome contributions from everyone.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your feature
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Setting Up Your Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/smart-quiz-app.git
cd smart-quiz-app

# Create a new branch
git checkout -b feature/your-feature-name

# Test the application
python3 test_features.py
python3 main.py
```

## 📝 Types of Contributions

### 🐛 Bug Reports

- Use the GitHub issue tracker
- Include steps to reproduce
- Provide system information
- Include error messages and logs

### ✨ Feature Requests

- Check existing issues first
- Clearly describe the feature
- Explain why it would be useful
- Consider backward compatibility

### 🔧 Code Contributions

- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

### 📚 Documentation

- Fix typos and grammar
- Improve clarity
- Add examples
- Update outdated information

## 🧪 Testing

Before submitting a pull request:

```bash
# Run the test suite
python3 test_features.py

# Test basic functionality
python3 main.py

# Check for syntax errors
python3 -m py_compile *.py
```

## 📋 Code Style Guidelines

### Python Code

- Follow PEP 8
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example

```python
def calculate_difficulty_score(success_rate: float, ease_factor: float) -> float:
    """
    Calculate difficulty score for a question.
    
    Args:
        success_rate: Percentage of correct answers (0.0-1.0)
        ease_factor: Current ease factor (1.3-4.0)
    
    Returns:
        Difficulty score (higher = more difficult)
    """
    return (1 - success_rate) * 100 + (3.0 - ease_factor) * 20
```

## 🎯 Areas We Need Help With

### High Priority

- 🌐 **Web Interface**: Create a web-based version
- 📱 **Mobile App**: Develop mobile applications
- 🌍 **Internationalization**: Add support for multiple languages
- 📊 **Advanced Analytics**: Enhanced visualizations and insights

### Medium Priority

- 🎨 **UI/UX Improvements**: Better terminal interface
- 🔊 **Audio Support**: Text-to-speech for questions
- 🎲 **Question Generation**: AI-powered question creation
- 🏆 **Gamification**: Achievements, badges, and challenges

### Low Priority

- 📝 **More Question Sets**: Additional subject areas
- 🔌 **Plugin System**: Extensible architecture
- ☁️ **Cloud Sync**: Cross-device synchronization
- 📈 **Export Features**: Data export capabilities

## 📁 Project Structure

```text
smart-quiz-app/
├── main.py                 # Main application entry point
├── SpacedRepetition.py     # Spaced repetition algorithm
├── ErrorAnalyzer.py       # Error analysis system
├── QuizLoader.py          # Quiz generation logic
├── Question.py            # Question model
├── Quiz.py                # Quiz engine
├── ScoreTracker.py        # Performance tracking
├── test_features.py       # Test suite
├── db/                    # Question databases
└── .github/               # GitHub workflows
```

## 🔄 Pull Request Process

1. **Create a Feature Branch**

   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes**

   ```bash
   python3 test_features.py
   ```

4. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create a Pull Request**
   - Use a clear, descriptive title
   - Explain what your changes do
   - Reference any related issues
   - Include screenshots if applicable

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## 🎨 Adding New Question Sets

To add new topics:

1. **Create a JSON file** in the `db/` directory
2. **Follow the format**:

   ```json
   {
     "title": "Your Topic Name",
     "description": "Brief description",
     "duration": 300,
     "questions": [
       {
         "question": "Your question here?",
         "answers": [
           "1. Option A",
           "2. Option B",
           "3. Option C",
           "4. Option D"
         ],
         "answer": 1,
         "hints": {
           "correct": "Great! Explanation of correct answer.",
           "fail": "Not quite. Explanation of why it's wrong."
         }
       }
     ]
   }
   ```

3. **Test your questions**:

   ```bash
   python3 main.py
   ```

## 🐛 Reporting Bugs

### Before Submitting

- Check if the bug has already been reported
- Try to reproduce the issue
- Gather relevant information

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python Version: [e.g. 3.9.5]
- Terminal: [e.g. bash, zsh]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context or screenshots.
```

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- CONTRIBUTORS.md file
- GitHub contributor graphs
- Release notes for significant contributions

## 📞 Getting Help

- 💬 **GitHub Discussions**: For questions and ideas
- 🐛 **Issues**: For bugs and feature requests
- 📧 **Email**: For private matters

## 📜 Code of Conduct

### Our Pledge

We are committed to making participation in our project a harassment-free experience for everyone.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team.

---

Thank you for contributing to Smart Quiz App! 🎉
