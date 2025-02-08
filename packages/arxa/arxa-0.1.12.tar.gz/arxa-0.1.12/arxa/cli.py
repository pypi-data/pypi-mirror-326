#!/usr/bin/env python3
# arxa/arxa/cli.py

import os
import sys
import argparse
import tempfile
import logging
import subprocess
import json

# Import rich’s logging handler for better log formatting.
try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None

from . import __version__  # Import version from __init__.py
from .config import load_config
from .arxiv_utils import search_arxiv_by_id_list
from .pdf_utils import download_pdf_from_arxiv, extract_text_from_pdf, sanitize_filename
from .research_review import generate_research_review
from .repo_utils import extract_github_url, clone_repo
from .prompts import PROMPT_PREFIX, PROMPT_SUFFIX  # For printing the template

def configure_logging(quiet: bool) -> None:
    """
    Configure logging to use rich formatting by default unless quiet is True.
    """
    if not quiet and RichHandler is not None:
        handler = RichHandler(markup=True)
    else:
        handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[handler]
    )

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="arxa: Generate research reviews from arXiv papers or PDFs, or start the FastAPI server."
    )
    # Flag to start the server.
    parser.add_argument("--server", action="store_true",
                        help="Start the FastAPI server instead of processing a paper/PDF.")

    # Add mutually exclusive arguments for arXiv id or local PDF.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-aid", help="arXiv ID of the paper (e.g. 1234.5678)")
    group.add_argument("-pdf", help="Path to a local PDF file")

    parser.add_argument("-o", "--output", help="Output markdown file for the review (ignored when --server is used)")
    parser.add_argument(
           "-p",
           "--provider",
           default="arxa.richards.ai:8000",  # default provider uses the remote server
           choices=["arxa.richards.ai:8000", "anthropic", "openai", "ollama", "deepseek", "fireworks"],
           help="LLM provider to use (default: arxa.richards.ai:8000)"
       )
    parser.add_argument(
        "-m",
        "--model",
        help="Model identifier/version (e.g., 'o3-mini'). When using the remote server, this will be ignored.",
        default="o3-mini"
    )
    parser.add_argument("-g", "--github", action="store_true",
                        help="Enable GitHub cloning if a GitHub URL is found in the review")
    parser.add_argument("-c", "--config", help="Path to configuration YAML file")
    parser.add_argument("--quiet", action="store_true", help="Disable rich output formatting")

    args = parser.parse_args()

    configure_logging(args.quiet)

    # Print startup information
    logger.info("Starting arxa version %s", __version__)
    logger.info("Arguments: provider=%s, model=%s", args.provider, args.model)
    if args.config:
        logger.info("Config file provided: %s", args.config)
        try:
            config = load_config(args.config)
            logger.info("Configuration loaded successfully.")
        except Exception as e:
            logger.error("Error loading config: %s", str(e))
            sys.exit(1)
    else:
        logger.info("No configuration file specified; using defaults.")
        config = {}

    # (Optional) Print out the prompt template (first few lines only to avoid spamming the console).
    template_preview = (PROMPT_PREFIX + "\n" + PROMPT_SUFFIX).split("\n")[:10]
    logger.info("Using prompt template (first 10 lines):\n%s", "\n".join(template_preview))

    # If the server flag is present, start the FastAPI server.
    if args.server:
        try:
            import uvicorn
        except ImportError:
            logger.error("uvicorn must be installed to run the server. Install it with pip install uvicorn")
            sys.exit(1)
        logger.info("Starting FastAPI server on port 8000 with provider hard-coded to openai/o3-mini ...")
        uvicorn.run("arxa.server:app", host="0.0.0.0", port=8000, reload=True)
        return

    # For non-server mode, ensure that either -aid or -pdf is provided.
    if not (args.aid or args.pdf):
        parser.error("You must specify either -aid or -pdf when not running in --server mode.")

    papers_dir = config.get("papers_directory", tempfile.gettempdir())
    output_dir = config.get("output_directory", os.getcwd())

    pdf_path = None
    paper_info = {}

    if args.aid:
        aid = args.aid.strip()
        results = search_arxiv_by_id_list([aid])
        if not results:
            logger.error("Paper with arXiv ID %s not found.", aid)
            sys.exit(1)
        paper = results[0]
        paper_info = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "abstract": paper.summary,
            "doi": paper.doi,
            "journal_ref": paper.journal_ref,
            "published": paper.published.isoformat() if paper.published else None,
            "arxiv_link": paper.entry_id,
        }
        pdf_filename = sanitize_filename(f"{aid}.pdf")
        pdf_path = os.path.join(papers_dir, pdf_filename)
        if not os.path.exists(pdf_path):
            logger.info("Downloading PDF for arXiv ID %s ...", aid)
            download_pdf_from_arxiv(paper, pdf_path)
        else:
            logger.info("Using existing PDF file at %s", pdf_path)
    else:
        pdf_path = args.pdf
        paper_info = {
            "title": os.path.basename(pdf_path),
            "authors": [],
            "abstract": "",
            "arxiv_link": "",
        }
        if not os.path.exists(pdf_path):
            logger.error("PDF file %s not found.", pdf_path)
            sys.exit(1)

    try:
        pdf_text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        logger.error("Failed to extract text from PDF: %s", str(e))
        sys.exit(1)

    if args.provider.lower() == "arxa.richards.ai:8000":
        try:
            import requests
        except ImportError:
            logger.error("The requests library is required for remote calls. Install it with pip install requests")
            sys.exit(1)
        endpoint = "http://arxa.richards.ai:8000/generate-review"
        payload = {
            "pdf_text": pdf_text,
            "paper_info": paper_info,
            "provider": args.provider,  # server will override to openai/o3-mini
            "model": args.model
        }
        logger.info("Sending review generation request to remote server at %s", endpoint)
        response = requests.post(endpoint, json=payload)
        try:
            response.raise_for_status()
        except Exception as e:
            logger.error("Remote API call failed: %s", str(e))
            sys.exit(1)
        review = response.json()["review"]
    else:
        provider_normalized = args.provider.lower()
        if provider_normalized == "anthropic":
            try:
                from anthropic import Anthropic
            except ImportError:
                logger.error("Anthropic client library not installed.")
                sys.exit(1)
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_api_key:
                logger.error("ANTHROPIC_API_KEY environment variable not set.")
                sys.exit(1)
            llm_client = Anthropic(api_key=anthropic_api_key)
        elif provider_normalized == "openai":
            import openai
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                logger.error("OPENAI_API_KEY environment variable not set.")
                sys.exit(1)
            openai.api_key = openai_api_key
            llm_client = openai
        elif provider_normalized == "ollama":
            llm_client = None
        elif provider_normalized == "deepseek":
            import openai
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_api_key:
                logger.error("DEEPSEEK_API_KEY environment variable not set.")
                sys.exit(1)
            openai.api_key = deepseek_api_key
            openai.api_base = "https://api.deepseek.com"
            llm_client = openai
        elif provider_normalized == "fireworks":
            # For Fireworks, we do not need a client instance.
            llm_client = None
        else:
            logger.error("Unsupported provider: %s", args.provider)
            sys.exit(1)
        try:
            review = generate_research_review(
                pdf_text,
                paper_info,
                provider=args.provider,
                model=args.model,
                llm_client=llm_client
            )
        except Exception as e:
            logger.error("Error generating research review: %s", str(e))
            sys.exit(1)

    try:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(review)
            logger.info("Review written to %s", args.output)
        else:
            logger.info("Generated review:\n%s", review)
    except Exception as e:
        logger.error("Failed to write review to file: %s", str(e))
        sys.exit(1)

    if not args.quiet:
        try:
            from rich.console import Console
            console = Console()
            console.rule("[bold green]Generated Research Review")
            console.print(review)
            console.rule()
        except ImportError:
            print(review)

    if args.github:
        github_url = None
        try:
            from .repo_utils import extract_github_url
            github_url = extract_github_url(review)
        except Exception as e:
            logger.error("Error extracting GitHub URL: %s", str(e))
        if github_url:
            try:
                clone_repo(github_url, output_dir)
                logger.info("Repository cloned from %s", github_url)
            except Exception as e:
                logger.error("Error during GitHub cloning: %s", str(e))
        else:
            logger.info("No GitHub URL found in the review.")

if __name__ == "__main__":
    main()
