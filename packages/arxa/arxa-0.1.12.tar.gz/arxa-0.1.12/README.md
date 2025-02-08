# arxa

arxa is a Python package that helps you generate comprehensive research reviews from arXiv papers or local PDFs. It features a command‐line interface for searching arXiv and generating summaries, along with a FastAPI server for remote generation. arxa integrates with various LLM providers (OpenAI, Anthropic, Ollama) and includes tools for PDF processing, configuration management, and repository handling.

## Installation

### Easy Installation (from PyPI)
To install the package easily via pip:

    pip install arxa

### Installing from Source
If you prefer to install from the source repository:
1. Clone the repository:

       git clone https://github.com/binaryninja/arxa.git

2. Change into the repository directory:

       cd arxa

3. Install it in editable mode:

       pip install -e .

This way you can make changes to the source code and test them immediately.

## Repository Structure and File Overview

```
arxa/
├── arxa/
│   ├── __init__.py             # Package version information.
│   ├── arxiv_utils.py          # Functions to search and retrieve arXiv papers.
│   ├── cli.py                # Command-line interface for generating reviews or starting the server.
│   ├── config.py             # Utilities for loading configuration from a YAML file.
│   ├── llm_backends.py       # Backend functions to interface with OpenAI, Anthropic, and Ollama APIs.
│   ├── pdf_utils.py          # PDF processing utilities: sanitizing filenames, downloading PDFs, extracting text.
│   ├── prompts.py            # Prompt templates used to instruct the language model.
│   ├── repo_utils.py         # Functions to extract and clone GitHub repository URLs from generated reviews.
│   ├── research_review.py    # Core functionality to generate a research review summary using an LLM.
│   └── server.py             # Use this to configure your own private arxa server.
└── __pycache__/               # Contains Python bytecode cache files.
```

### Detailed File & Function Descriptions

#### arxa/arxiv_utils.py
- Provides functions to interact with the arXiv API:
  - `search_arxiv_by_author(author: str, max_results: int = 10)`: Searches for papers by author name.
  - `search_arxiv_by_keyword(keyword: str, max_results: int = 10)`: Searches for papers by keyword in the title.
  - `search_arxiv_by_id_list(id_list: list)`: Searches for papers given a list of arXiv IDs (handles batching if necessary).

#### arxa/cli.py
- The entry point for the command-line interface.
- Parses arguments and provides two main modes:
  - **Server Mode**: Starts the FastAPI server by using the `--server` flag.  remember to set your own API key(s) in the `config.yaml` file.
  - **Review Generation Mode**: Accepts an arXiv ID (`-aid`) or local PDF file (`-pdf`) to generate a research review.
- Other options include:
  - `-o` or `--output`: Specify output file for the generated review.
  - `-p` or `--provider`: Choose the LLM provider (default: "arxa.richards.ai:8000" for community server, or use "anthropic", "openai"").
  - `-m` or `--model`: Specify model identifier/version, such as "o3-mini".
  - `-g` or `--github`: Enable GitHub cloning if a GitHub URL is detected in the generated review.
  - `-c` or `--config`: Path to a YAML configuration file.
  - `--quiet`: Disable rich output formatting.

Usage examples:

- Generate a review from an arXiv ID:

      arxa -aid 2301.00123v1 -o review.md

- Generate a review from a local PDF:

      arxa -pdf /path/to/paper.pdf

- Generate a review using a specific provider and model:

      arxa -aid 2301.00123v1 -o review.md -p openai -m o3-mini

- Start a private arxa server:

      arxa --server

#### arxa/config.py
- Contains a helper function:
  - `load_config(config_path: str = "config.yaml")`: Loads configuration data from a YAML file. This file can specify defaults such as directories for papers and output.

#### arxa/llm_backends.py
- Provides functions to interface with various LLM backends:
  - `openai_generate(...)`: Uses OpenAI’s API (with rate limit handling via the tenacity library) to generate output.
  - `anthropic_generate(...)`: Uses Anthropic’s API to generate completions with built-in retry logic.
  - `ollama_generate(...)`: Interfaces with a local Ollama inference server.
  - `truncate_text_to_token_limit(...)`: Truncates input text so that its token count does not exceed the specified maximum.
- Custom exceptions (`OpenAIAPIError`, `AnthropicAPIError`, `OllamaAPIError`) handle backend-specific issues.

#### arxa/pdf_utils.py
- PDF-related utility functions:
  - `sanitize_filename(filename: str)`: Removes invalid characters from filenames.
  - `download_pdf_from_arxiv(paper: arxiv.Result, output_path: str)`: Downloads a paper’s PDF to the specified path.
  - `extract_text_from_pdf(pdf_path: str)`: Extracts text from a PDF using PyPDF2.

#### arxa/prompts.py
- Contains prompt templates that guide the language model in generating the research review.
- `PROMPT_PREFIX`: Instructions and initial context.
- `PROMPT_SUFFIX`: A markdown template into which paper information is inserted.

The templates instruct the model to generate content sections such as Paper Information, Summary, Methodology, Strengths, Weaknesses, and additional notes.

#### arxa/repo_utils.py
- Offers functions for handling GitHub repositories mentioned in a review:
  - `extract_github_url(content: str)`: Uses regex to find a GitHub URL in the generated review.
  - `clone_repo(github_url: str, output_dir: str)`: Uses the GitHub CLI (`gh`) to fork/clone the repository to a local directory.

#### arxa/research_review.py
- Implements the generation of a research review summary using text extracted from a PDF and paper metadata.
- Key functions:
  - `truncate_text_to_token_limit(...)`: Ensures the prompt does not exceed a maximum token limit (using tiktoken).
  - `generate_research_review(...)`: Constructs the full prompt (inserting the truncated PDF text and paper_info into the prompt template) and calls the appropriate LLM backend (OpenAI, Anthropic, or Ollama) to generate the review.
- It then extracts the relevant response section demarcated by `<research_notes>` tags.

#### arxa/server.py
- Implements a FastAPI server to offer a RESTful interface. Key features:
  - An endpoint `/generate-review` that accepts a JSON payload (with PDF text, paper information, provider, model) and returns the generated review.
  - A `/health` endpoint for a simple health check.
  - Custom middleware for logging and rate limiting (tracks request frequency per IP, blacklists abusive clients).
  - Overrides provider/model parameters so that all requests are processed using (for example) the OpenAI API with a specific model ("o3-mini").

## Command-Line Options

When running the package via the command line (using the `arxa` CLI), you have various options:

- --server
  Start the FastAPI server instead of processing a PDF or arXiv paper.

- -aid
  Specify an arXiv ID (e.g., `1234.5678`) to fetch and generate a review.

- -pdf
  Provide the path to a local PDF to generate a research review from.

- -o, --output
  Set the output file for saving the generated markdown review.

- -p, --provider
  Choose the LLM provider. Options are:
  • arxa.richards.ai:8000 (default remote server)
  • anthropic
  • openai
  • ollama

- -m, --model
  Define the model identifier/version (default "o3-mini" when using remote server mode).

- -g, --github
  Enable GitHub cloning if a GitHub URL is present in the generated review.

- -c, --config
  Path to an alternative YAML configuration file.

- --quiet
  Disable enhanced output formatting (useful when rich output is not desired).

Example CLI command:

    arxa -aid 2301.00123v1 -o my_review.md -p openai -m o3-mini --github

This command will search for the paper using the provided arXiv ID, download and process the PDF if necessary, generate a research review using OpenAI’s API, write the review to "my_review.md", and clone any detected GitHub repository.
