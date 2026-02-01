# Spark Claude Workflow

A PySpark project with automated testing and AI-powered code reviews—no local Python, Java, or Spark installation required.

## Overview

This repository demonstrates a cloud-first development workflow where:

- **PySpark tests** run entirely in GitHub Actions
- **Claude AI** automatically reviews pull requests for bugs, security issues, and code quality
- **Local development** only requires Git and a code editor

## Project Structure

```
spark-claude-workflow/
├── .github/
│   └── workflows/
│       ├── claude-review.yml    # AI code review workflow
│       └── pytest-spark.yml     # PySpark test workflow
├── jobs/
│   ├── __init__.py
│   └── word_count.py            # Sample PySpark job
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures (Spark session)
│   └── test_word_count.py       # Unit tests
└── requirements.txt             # Python dependencies
```

## Workflows

### PySpark Tests (`pytest-spark.yml`)

Runs automatically on:
- Every push to `main`
- Every pull request

**What it does:**
1. Sets up Python 3.11 and Java 17
2. Installs PySpark and pytest
3. Runs all tests with coverage reporting

### Claude PR Review (`claude-review.yml`)

Runs automatically on:
- Pull request opened, updated, or reopened
- Comments mentioning `@claude`

**What it does:**
1. Analyzes code changes in the PR
2. Posts review comments identifying:
   - Potential bugs
   - Security vulnerabilities
   - Code quality improvements
   - Style issues

## Getting Started

### Prerequisites

- Git
- GitHub account
- [Anthropic API key](https://console.anthropic.com) (for Claude reviews)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/spark-claude-workflow.git
   cd spark-claude-workflow
   ```

2. **Add your Anthropic API key to GitHub:**
   - Go to repository Settings → Secrets and variables → Actions
   - Create a new secret: `ANTHROPIC_API_KEY`

3. **Start developing:**
   ```bash
   git checkout -b my-feature
   # Make changes
   git add .
   git commit -m "Add feature"
   git push -u origin my-feature
   ```

4. **Open a pull request** and watch the workflows run.

## Writing Spark Jobs

Add new jobs in the `jobs/` directory:

```python
# jobs/my_job.py
from pyspark.sql import SparkSession

def my_transformation(spark: SparkSession, data):
    df = spark.createDataFrame(data)
    # Your logic here
    return df
```

## Writing Tests

Add tests in the `tests/` directory. Use the `spark` fixture for a pre-configured SparkSession:

```python
# tests/test_my_job.py
from jobs.my_job import my_transformation

def test_my_transformation(spark):
    data = [("a", 1), ("b", 2)]
    result = my_transformation(spark, data)
    assert result.count() == 2
```

## Interacting with Claude

In any pull request, you can:

- **Ask questions:** Comment `@claude what does this function do?`
- **Request reviews:** Comment `@claude review this for security issues`
- **Get explanations:** Comment `@claude explain the test failures`

## Local Development (Optional)

If you want to run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
PYTHONPATH=. pytest tests/ -v
```

Requires Python 3.11+ and Java 17+.

## Configuration

### Customize Claude Reviews

Edit `.github/workflows/claude-review.yml` to add custom prompts:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}
    prompt: "Focus on PySpark best practices and performance optimizations"
```

### Customize Test Settings

Edit `tests/conftest.py` to adjust Spark configuration:

```python
spark = (
    SparkSession.builder
    .config("spark.sql.shuffle.partitions", "2")
    .config("spark.driver.memory", "2g")  # Increase memory
    .getOrCreate()
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail with "Java not found" | Java is auto-installed in CI; for local dev, install Java 17 |
| Claude review not posting | Check that `ANTHROPIC_API_KEY` secret is set |
| Empty DataFrame errors | Handle empty inputs before creating DataFrames |

## License

MIT
