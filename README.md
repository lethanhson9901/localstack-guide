<div align="center">

# 🚀 LocalStack Guide

[![Python](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/downloads/)
[![LocalStack](https://img.shields.io/badge/LocalStack-3.2.0-orange.svg)](https://localstack.cloud/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Hints: Mypy](https://img.shields.io/badge/type%20hints-mypy-blue.svg)](https://mypy-lang.org/)

A modern Python toolkit for AWS local development with LocalStack, emphasizing developer experience and best practices.

[Getting Started](#-getting-started) •
[Features](#-features) •
[Documentation](#-documentation) •
[Contributing](#-contributing)

</div>

---

## 📦 Getting Started

### One-Minute Setup

```bash
# Clone repository
git clone https://github.com/lethanhson9901/localstack-guide.git
cd localstack-guide

# Install UV & create virtual environment
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python=python3.12.3 .venv
source .venv/bin/activate

# Install dependencies & setup
uv pip install -e ".[dev]"
pre-commit install

# Start LocalStack & initialize
docker compose up -d
python scripts/init_local.py init-infrastructure
```

### Quick Verification

```bash
# Run tests
pytest tests/

# Verify LocalStack health
curl http://localhost:4566/_localstack/health
```

---

## ✨ Features

### Core Capabilities

<table>
<tr>
<td>

### 🐍 Modern Python
- UV for lightning-fast package management
- Type safety with mypy
- Ruff for unified Python linting
- Src-layout architecture

</td>
<td>

### ☁️ AWS Development
- LocalStack 3.2.0+
- AWS CDK integration
- Typed boto3 clients
- Automatic cleanup

</td>
</tr>
<tr>
<td>

### 🛠️ Developer Tools
- Pre-commit hooks
- Rich CLI interfaces
- Docker orchestration
- Pytest integration

</td>
<td>

### 📊 AWS Services
- S3 Storage
- DynamoDB
- Lambda Functions
- SQS/SNS Messaging

</td>
</tr>
</table>

---

## 📖 Documentation

### Project Structure

```
localstack-guide/
├── 📁 src/aws_local_dev/        # Main package
│   ├── 📁 configs/              # AWS configurations
│   └── 📁 infrastructure/       # IaC components
├── 📁 tests/                    # Test suite
├── 📁 scripts/                  # Utility scripts
└── 📄 [Config Files]           # Project configurations
```

### Development Guide

#### 1. Environment Setup

Create `.env` file:
```ini
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
LOCALSTACK_HOSTNAME=localhost
SERVICES=s3,dynamodb,lambda,sqs,sns
```

#### 2. Available Resources

##### S3 Storage
```python
# Access S3 bucket
from aws_local_dev.configs import AWSConfig

aws = AWSConfig()
s3 = aws.get_client('s3')
s3.list_objects_v2(Bucket='my-application-storage')
```

##### DynamoDB Tables
```python
# Access DynamoDB
dynamodb = aws.get_client('dynamodb')
dynamodb.query(
    TableName='users',
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': {'S': 'user123'}}
)
```

#### 3. Code Quality

```bash
# Format and lint
ruff check .
ruff format .

# Type checking
mypy .

# Run tests
pytest tests/
```

### Best Practices

#### Code Standards
- Use type hints consistently
- Follow src layout structure
- Document public interfaces
- Write unit tests

#### Git Workflow
1. Create feature branch
2. Make changes
3. Run quality checks
4. Submit PR

---

## 🔧 Configuration

### Available Scripts

| Script | Description |
|--------|-------------|
| `init_local.py` | Initialize AWS infrastructure |
| `pytest tests/` | Run test suite |
| `ruff check .` | Run code quality checks |

### Docker Settings

Key configurations in `compose.yaml`:
```yaml
services:
  localstack:
    image: localstack/localstack:3.2.0
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,dynamodb,lambda,sqs,sns
```

---

## 🚀 Advanced Usage

### Adding New Services

1. Update `SERVICES` in `.env`
2. Add to `infrastructure/base_stack.py`:
```python
def _create_new_service(self) -> None:
    # Service configuration
    pass
```
3. Add tests in `tests/`
4. Update initialization script

### Custom Development Flow

1. Start services:
```bash
docker compose up -d
```

2. Initialize resources:
```bash
python scripts/init_local.py init-infrastructure
```

3. Develop and test:
```bash
pytest tests/ -v
```

---

## 🔍 Troubleshooting

### Common Issues

<details>
<summary>LocalStack Connection Issues</summary>

1. Check Docker status:
```bash
docker compose ps
```

2. Verify health:
```bash
curl http://localhost:4566/_localstack/health
```

3. Check logs:
```bash
docker compose logs localstack
```
</details>

<details>
<summary>Package Installation Issues</summary>

1. Verify Python version:
```bash
python --version  # Should be 3.12.3+
```

2. Check UV installation:
```bash
uv --version
```

3. Reinstall dependencies:
```bash
uv pip install -e ".[dev]"
```
</details>

---

## 👥 Contributing

### Getting Started

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit PR

### Development Process

```bash
# Setup development environment
uv venv --python=python3.12.3 .venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Make changes and test
ruff check .
mypy .
pytest tests/

# Submit PR
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Created with ❤️ by [Son Le](https://github.com/lethanhson9901)

</div>