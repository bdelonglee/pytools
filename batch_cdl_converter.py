#!/usr/bin/env python3

import argparse
import os
import subprocess


def convert_cc_files(input_dir, output_format, destination_dir, verbose):
    # List all .cc files in the specified directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".cc"):
            file_path = os.path.join(input_dir, file_name)

            # Construct the command with the provided output format and destination directory
            command = [
                "cdl_convert",
                file_path,
                "-o",
                output_format,
                "-d",
                destination_dir,
            ]

            # Run the command using subprocess
            result = subprocess.run(command, capture_output=True, text=True)

            if verbose:
                print(f"Processing: {file_path}")
                if result.returncode == 0:
                    print(f"Success: {result.stdout}")
                else:
                    print(f"Error: {result.stderr}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert .cc files using cdl_convert."
    )

    # Optional input directory (defaults to current directory)
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=".",
        help="Directory containing .cc files to process. Default is the current directory.",
    )

    # Output format and destination directory with default values
    parser.add_argument(
        "-o",
        "--output",
        default="ccc,cdl",
        help="Output format for cdl_convert. Default is 'ccc,cdl'.",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default=".",
        help="Destination directory for output files. Default is the current directory.",
    )

    # Verbose flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints details of the conversion process.",
    )

    args = parser.parse_args()

    # Convert all .cc files in the directory with the specified options
    convert_cc_files(args.input_dir, args.output, args.destination, args.verbose)


if __name__ == "__main__":
    main()
