#!/usr/bin/env python
import os
from subprocess import call
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from argparse import ArgumentParser
from pathlib import Path


def convert_ipynb_to_pdf(ipynb_file_path):
    # Get the PDF file path
    real_ipynb_file_path = Path(ipynb_file_path).resolve()
    # Gets the directory path of the IPYNB file
    pdf_file_path = real_ipynb_file_path.with_suffix("")

    # Check if PDF file already exists
    if not pdf_file_path.exists():
        print(f"Converting {ipynb_file_path} to PDF...")
        # Execute the nbconvert command
        call(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "webpdf",
                "--output",
                pdf_file_path,
                ipynb_file_path,
            ]
        )
    else:
        print(f"PDF for {ipynb_file_path} already exists.")


def find_ipynb_files(root_dir):
    ipynb_files = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".ipynb"):
                ipynb_file_path = os.path.join(subdir, file)
                ipynb_files.append(ipynb_file_path)
    return ipynb_files


def main():
    parser = ArgumentParser(description="Convert IPYNB files to PDF")
    parser.add_argument(
        "directory", type=str, help="Directory to search for IPYNB files"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Maximum number of workers to use for conversion",
    )
    args = parser.parse_args()
    ipynb_files = find_ipynb_files(args.directory)

    with ThreadPoolExecutor(args.max_workers) as executor:
        list(
            tqdm(
                executor.map(convert_ipynb_to_pdf, ipynb_files),
                total=len(ipynb_files),
                desc="Converting IPYNB files to PDF",
            )
        )


if __name__ == "__main__":
    main()
