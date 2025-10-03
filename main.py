#!/usr/bin/env python3
"""
RAG vs Graph RAG vs Knowledge Graph System

Main entry point for the system.
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Main entry point"""
    from rag_system.cli import cli

    # Run CLI
    cli()


if __name__ == "__main__":
    main()
