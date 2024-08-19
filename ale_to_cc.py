#!/usr/bin/python3

#!/usr/bin/env python3

import argparse
import os
import re


def parse_ale(file_path, output_dir, verbose):
    with open(file_path, "r") as file:
        in_data_section = False

        for line in file:
            # Skip headers and column names
            if line.startswith("Data"):
                in_data_section = True
                continue

            if in_data_section:
                # Split the line by tabs
                fields = line.strip().split("\t")

                if len(fields) < 2:
                    continue

                file_name = fields[0].strip()  # First column: File Name
                asc_sop_sat = fields[
                    -3
                ].strip()  # Extract the combined ASC_SOP and ASC_SAT field

                # Extract SOP (Slope, Offset, Power) using regex
                sop_match = re.search(r"\((.*?)\)\((.*?)\)\((.*?)\)", asc_sop_sat)
                if sop_match:
                    slope = sop_match.group(1)
                    offset = sop_match.group(2)
                    power = sop_match.group(3)
                else:
                    if verbose:
                        print(f"Error parsing SOP for {file_name}")
                    continue

                # Extract ASC_SAT (Saturation)
                asc_sat = fields[-2].strip()

                # Create the .cc file content
                cc_content = f"""<ColorCorrection>
    <SOPNode>
        <Slope>{slope.replace(' ', ' ')}</Slope>
        <Offset>{offset.replace(' ', ' ')}</Offset>
        <Power>{power.replace(' ', ' ')}</Power>
    </SOPNode>
    <SatNode>
        <Saturation>{asc_sat}</Saturation>
    </SatNode>
</ColorCorrection>"""

                # Determine output file path
                output_file_name = f"{file_name.split('.')[0]}.cc"
                output_file_path = os.path.join(output_dir, output_file_name)

                # Write to the .cc file
                with open(output_file_path, "w") as output_file:
                    output_file.write(cc_content)

                if verbose:
                    print(f"Written: {output_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert ALE file to Color Correction (.cc) files."
    )
    parser.add_argument("ale_file", help="The ALE file to process.")
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Output directory for .cc files. Default is the current directory.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints details of the files being processed.",
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Parse ALE file and generate .cc files
    parse_ale(args.ale_file, args.output, args.verbose)


if __name__ == "__main__":
    main()
