# Contributing to SuperTrend Strategy Analysis

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 📋 How to Contribute

### 1. Report Bugs
If you find a bug, please create an Issue with:
- **Title:** Clear, descriptive bug title
- **Description:** Detailed explanation of the bug
- **Steps to Reproduce:** Step-by-step instructions
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Environment:** Python version, OS, database version

### 2. Suggest Enhancements
Have ideas for improvements? Open an Issue with:
- **Title:** Feature request title
- **Description:** Detailed description of the enhancement
- **Motivation:** Why this would be useful
- **Example Use Cases:** How it would be used

### 3. Submit Code Changes
Ready to contribute code? Follow these steps:

#### Step 1: Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/stock_market_analysis.git
cd stock_market_analysis

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/stock_market_analysis.git
```

#### Step 2: Create a Feature Branch
```bash
# Update from upstream
git fetch upstream
git checkout upstream/main

# Create your feature branch
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/bug-description
```

#### Step 3: Make Changes
- Follow the code style (see [Code Style](#code-style))
- Add comments and docstrings
- Test your changes thoroughly
- Update documentation if needed

#### Step 4: Commit and Push
```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "Brief description of changes"

# Push to your fork
git push origin feature/your-feature-name
```

#### Step 5: Create Pull Request
- Go to GitHub and create a Pull Request
- Link related issues (e.g., "Closes #123")
- Provide clear description of changes
- Include testing information

## 🎯 Code Style

### Python Guidelines
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 100 characters
- Use type hints where possible

### Example:
```python
def calculate_supertrend(df: pd.DataFrame, length: int = 10, factor: float = 2.0) -> pd.DataFrame:
    """
    Calculate SuperTrend indicator values.
    
    Args:
        df: DataFrame with OHLC data
        length: ATR lookback period (default: 10)
        factor: ATR multiplier (default: 2.0)
    
    Returns:
        DataFrame with SuperTrend values
    """
    # Implementation here
    pass
```

### File Organization
- Scripts: `category/script_name.py` (e.g., `1_collection/fetch_prices.py`)
- Data files: Store in appropriate directory (`nse_history_csv/`, `bse_history_csv/`, etc.)
- Configuration: Use config files or environment variables
- Comments: Use `#` for inline, `"""..."""` for docstrings

## 🧪 Testing

### Before Submitting PR
1. **Test your code locally:**
   ```bash
   python your_script.py
   ```

2. **Check for errors:**
   ```bash
   # Check Python syntax
   python -m py_compile your_script.py
   ```

3. **Verify database integration:**
   - Ensure PostgreSQL connection works
   - Test with sample data
   - Verify data integrity

4. **Update related tests:**
   - Add unit tests if applicable
   - Include test data or fixtures
   - Document test procedures

## 📝 Documentation

### Update Documentation For:
- New features → Add to DOCUMENTATION.md
- New scripts → Add usage instructions
- Parameter changes → Update configuration section
- Database changes → Update schema documentation

### Documentation Format:
```markdown
### Feature Name

**Description:** What it does

**Usage:**
\`\`\`python
# Code example
\`\`\`

**Parameters:**
- param1: description
- param2: description

**Output:**
- result1: description
```

## 🔄 Development Workflow

```
1. Issue Discussion
   ↓
2. Create Feature Branch
   ↓
3. Make Changes & Test
   ↓
4. Submit Pull Request
   ↓
5. Code Review
   ↓
6. Address Feedback
   ↓
7. Merge to Main
```

## ✅ Checklist Before PR

- [ ] Code follows PEP 8 style
- [ ] Docstrings added to new functions
- [ ] Comments explain complex logic
- [ ] Tested locally with sample data
- [ ] No hardcoded paths or credentials
- [ ] Related documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear

## 🚀 Areas for Contribution

### High Priority
- [ ] Improve signal accuracy for low-performing sectors
- [ ] Enhance risk management features
- [ ] Add machine learning parameter optimization
- [ ] Improve dashboard interactivity

### Medium Priority
- [ ] Add more technical indicators
- [ ] Implement portfolio optimization
- [ ] Create trading alerts system
- [ ] Add backtesting framework

### Low Priority
- [ ] Documentation improvements
- [ ] Code refactoring
- [ ] Performance optimization
- [ ] Additional visualizations

## 📞 Questions?

- **GitHub Issues:** For bugs and feature requests
- **Discussions:** For general questions
- **Documentation:** Check [DOCUMENTATION.md](DOCUMENTATION.md) first

## 📚 Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Contributing Guide](https://docs.github.com/en/contributing)
- [SuperTrend Indicator Reference](https://www.investopedia.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [TA-Lib Documentation](https://github.com/mrjbq7/ta-lib)

## 📌 Community Standards

- Be respectful and constructive
- Welcome newcomers and help them learn
- Give credit to contributors
- Accept feedback gracefully
- Follow the Code of Conduct

## 🎓 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards
- Respectful and professional communication
- Focus on ideas and code, not individuals
- Help and support one another
- Report issues through appropriate channels

### Unacceptable Behavior
- Harassment, discrimination, or abuse
- Spam or off-topic content
- Deliberate disruption
- Any unlawful conduct

### Enforcement
Violations may result in temporary or permanent removal from the project.

---

**Thank you for contributing to make this project better!** 🙏

For more information, see [DOCUMENTATION.md](DOCUMENTATION.md) and [README.md](README.md)
