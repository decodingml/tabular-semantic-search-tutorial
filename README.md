<div align="center">
  <h1>Hands-on Amazon Tabular Semantic Search</h1>
  <p class="tagline">Open-source series by <a href="https://decodingml.substack.com">Decoding ML</a> in collaboration with Superlinked and MongoDB.</p>
</div>

## 🎯 About These Series

TBD


## 🎓 Prerequisites

| Category | Requirements |
|----------|-------------|
| **Skills** | Basic knowledge of Python and Machine Learning |
| **Hardware** | Any modern laptop/workstation will do the job (no GPU or powerful computing power required). |
| **Level** | Intermediate |

## 💰 Cost Structure

All tools used throughout the course will stick to their free tier, except OpenAI's API, which will cost you <1$ to run all our examples.

## 📚 Articles

TBD

## 🏗️ Project Structure

```text
.
├── data/                                          # Directory where dataset files and processed data will be downloaded.
├── superlinked_app/                               # Main application source code
├── tools/                                         # Utility scripts and helper tools
├── .env                                           # Environment variables for local development
├── .env.example                                   # Template for environment variables
├── 1_eda.ipynb                                    # Notebook for Exploratory Data Analysis for the Amazon dataset
├── 2_tabular_semantic_search_superlinked.ipynb    # Demo notebook for Superlinked tabular semantic search
├── 3_tabular_semantic_search_text_to_sql.ipynb    # Examples of text-to-SQL queries
├── Makefile                                       # Running commands shortcuts
├── pyproject.toml                                 # Python project dependencies and metadata
└── uv.lock                                        # Lock file for uv package manager
```

## 💾 Dataset

We will use the [ESCI-S: extended metadata for Amazon ESCI dataset](https://github.com/shuttie/esci-s?tab=readme-ov-file) dataset released under the Apache-2.0 license.

It is an e-commerce dataset on Amazon products. 

The full dataset references ~1.8M unique products. We will work with a sample of 4400 products to make everything lighter, but the code is compatible with the whole dataset.

📚 Read more on the [ESCI-S dataset](https://github.com/shuttie/esci-s?tab=readme-ov-file)

💻 Explore it in our [Dataset Exploration](1_eda.ipynb) Notebook.


## 🚀 Getting Started

For detailed installation and usage instructions, see our [INSTALL_AND_USAGE](INSTALL_AND_USAGE.md) guide.

**Recommendation:** While you can follow the installation guide directly, we strongly recommend reading the accompanying articles to gain a complete understanding of the series.

## 💡 Questions and Troubleshooting

Have questions or running into issues? We're here to help!

Open a [GitHub issue](https://github.com/decodingml/hands-on-retrieval/issues) for:
- Questions about the course material
- Technical troubleshooting
- Clarification on concepts


## Sponsors

<table>
  <tr>
    <td align="center">
      <a href="" target="_blank">Superlinked</a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="" target="_blank">
        <img src="assets/hopsworks.png" width="200" alt="Hopsworks">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="" target="_blank">MongoDB</a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="" target="_blank">
        <img src="assets/hopsworks.png" width="200" alt="Hopsworks">
      </a>
    </td>
  </tr>
</table>

TBD

## License

This course is an open-source project released under the MIT license. Thus, as long you distribute our LICENSE and acknowledge your project is based on our work, you can safely clone or fork this project and use it as a source of inspiration for your educational projects (e.g., university, college degree, personal projects, etc.).