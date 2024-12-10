# 🚀 Installation and Usage Guide

This guide will help you ...

# 📋 Prerequisites

## Local Tools
You'll need the following tools installed locally:
- [Python v3.11](https://www.python.org/downloads/)
- [uv v0.4.30](https://github.com/astral-sh/uv) - Python package installer and virtual environment manager
- [GNU Make 3.81](https://www.gnu.org/software/make/) - Build automation tool

## Cloud Services
The project requires access to these cloud services:

| Service | Purpose | Cost | Required Credentials | Setup Guide |
|---------|---------|------|---------------------|-------------|
| [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) | Vector DB for retrieval | Free tier available | `MONGODB_DATABASE_USER_USERNAME`<br>`MONGODB_DATABASE_USER_PASSWORD` | 1. [Create a Cluster](https://www.mongodb.com/docs/guides/atlas/cluster/) </br> 2. [Add a Database User](https://www.mongodb.com/docs/guides/atlas/db-user/) </br> 3. [Configure a Network Connection](https://www.mongodb.com/docs/guides/atlas/network-connections/) </br> 4. [Creating the API Key](https://docs.superlinked.com/run-in-production/index-1/mongodb#creating-the-api-key) |
| [OpenAI API](https://openai.com/index/openai-api/) | LLM API | Pay-per-use | `OPENAI_API_KEY`<br>`OPENAI_MODEL_ID` | [Quick Start Guide](https://platform.openai.com/docs/quickstart) |

## 1. Installation

Set up the project environment by running the following:
```bash
make install
```
Test that you have Python 3.11.8 installed in your new `uv` environment:
```bash
uv run python --version
# Output: Python 3.11.8
```

This command will:
- Create a virtual environment using `uv`
- Activate the virtual environment
- Install all dependencies from `pyproject.toml`

> [!NOTE]
> Normally, `uv` will pick the right Python version mentioned in `.python-version` and install it automatically if it is not on your system. If you are having any issues, explicitly install the right Python version by running `make install-python`

## 2. Environment Configuration

Before running any components:
1. Create your environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the required credentials following the inline comments.

# ⚡️ Running the Code

1. Start the server:
   ```bash
   make start-server
   ```
   This will launch the application server using Python.

2. Load sample data:
   ```bash
   make load-data
   ```
   This sends a POST request to populate the database with initial product schema data.

3. Test the search functionality:
   ```bash
   make post-filter-query
   ```
   This executes a sample natural language query ("books with a price lower than 100") against the API.

> [!TIP]
> Make sure the server is running (step 1) before executing the data loading or search commands.