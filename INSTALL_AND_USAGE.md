# 🚀 Installation and Usage Guide

Get up and running with our semantic search engine in minutes.

# 📋 Prerequisites

## Local Setup
Install these tools on your machine:
| Tool | Purpose | Version | Download Link | Notes |
|------|---------|---------|---------------|--------|
| Python | Programming language runtime | v3.11 | [Download](https://www.python.org/downloads/) | Core runtime environment |
| uv | Python package installer and virtual environment manager | v0.4.30 | [Download](https://github.com/astral-sh/uv) | Modern replacement for pip/venv/poetry |
| GNU Make | Build automation tool | v3.81 | [Download](https://www.gnu.org/software/make/) | Used for running project commands |

## Cloud Services
You'll need access to:

| Service | Purpose | Cost | Required Credentials | Setup Guide |
|---------|---------|------|---------------------|-------------|
| [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) | Vector DB for retrieval | Free tier available | `MONGODB_DATABASE_USER_USERNAME`<br>`MONGODB_DATABASE_USER_PASSWORD` | 1. [Create a Cluster](https://www.mongodb.com/docs/guides/atlas/cluster/) </br> 2. [Add a Database User](https://www.mongodb.com/docs/guides/atlas/db-user/) </br> 3. [Configure a Network Connection](https://www.mongodb.com/docs/guides/atlas/network-connections/) </br> 4. [Creating the API Key](https://docs.superlinked.com/run-in-production/index-1/mongodb#creating-the-api-key) |
| [OpenAI API](https://openai.com/index/openai-api/) | LLM API | Pay-per-use | `OPENAI_API_KEY`<br>`OPENAI_MODEL_ID` | [Quick Start Guide](https://platform.openai.com/docs/quickstart) |

# 💻 Setup in 3 Steps

## 1. Install Dependencies

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

## 2. Configure Environment

Before running any components:
1. Create your environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the required credentials following the inline comments.

> [!IMPORTANT]
> **Quick Test Mode:** Set `USE_MONGO_VECTOR_DB=False` to use an in-memory database instead of MongoDB.

## 3. Load and Process Your Data

The first step is to download and process the dataset sample:
```bash
make download-and-process-sample-dataset
```

We also support the complete dataset, but you need a powerful computer, good internet and patience to run everything on it:
```bash
make download-and-process-full-dataset
```

You should see this structure in your `data` folder:
```text
data/
├── processed_100_sample.jsonl
├── processed_300_sample.jsonl
├── processed_632_sample.jsonl
├── sample.json
└── sample.json.gz
```

# ⚡️ Explore & Run

## 🔍 Interactive Notebooks

| Notebook | Description |
|----------|-------------|
| [Dataset Exploration](1_eda.ipynb) | Dive into the Amazon ESCI dataset |
| [Semantic Search Demo](2_tabular_semantic_search_superlinked.ipynb) | See Superlinked in action |
| [Text-to-SQL Examples](3_tabular_semantic_search_text_to_sql.ipynb) | Try LlamaIndex queries |

## 🚀 Launch the Superlinked Server and MongoDB Vector Database

1. Start it up:
   ```bash
   make start-superlinked-server
   ```
   FastAPI endpoints docs available at `http://localhost:8080/docs`

2. Load your data:
   ```bash
   make load-data   # Give it a few minutes
   ```

3. Try some queries:
   ```bash
   make post-filter-query     # Example: "books under $100"
   make post-semantic-query   # Natural language search
   ```

4. Start the Streamlit UI:
   ```bash
   make start-ui
   ```
   Accessible at `http://localhost:8501/`

> 🔔 Make sure the server is running (step 1) before executing the data loading or search commands.
