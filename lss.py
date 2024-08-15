#!/opt/homebrew/opt/python@3.12/libexec/bin/python
#!/usr/bin/python3

import argparse
import os
import re
from collections import defaultdict

from PIL import Image


def detect_sequences(
    directory, recursive=False, depth=1, include_resolution=False, include_size=False
):
    sequences = defaultdict(list)

    regex = re.compile(r"^(.*?)(\.\w+)?\.(\d+)\.(\w+)$")

    def explore_directory(current_directory, current_depth, base_path):
        if current_depth > depth:
            return

        for root, dirs, files in os.walk(current_directory):
            if not recursive and root != base_path:
                continue

            relative_depth = os.path.relpath(root, base_path).count(os.sep) + 1

            if relative_depth > depth:
                continue

            for filename in files:
                match = regex.match(filename)
                if match:
                    base_name = match.group(1)
                    sub_category = match.group(2) or ""
                    frame_number = int(match.group(3))
                    padding = len(match.group(3))
                    extension = match.group(4)

                    relative_path = os.path.relpath(root, base_path)
                    key = (base_name, sub_category, padding, extension, relative_path)

                    file_path = os.path.join(root, filename)

                    if include_resolution:
                        with Image.open(file_path) as img:
                            resolution = f"{img.width}x{img.height}"
                    else:
                        resolution = None

                    file_size = os.path.getsize(file_path) if include_size else None

                    sequences[key].append((frame_number, resolution, file_size))

            if recursive and current_depth < depth:
                for subdir in dirs:
                    explore_directory(
                        os.path.join(root, subdir), current_depth + 1, base_path
                    )

            if not recursive:
                break

    explore_directory(directory, 1, directory)

    results = []

    for (
        base_name,
        sub_category,
        padding,
        extension,
        relative_path,
    ), frames in sequences.items():
        frames.sort(key=lambda x: x[0])
        missing_ranges = []
        resolutions = set(res[1] for res in frames if res[1] is not None)
        total_size = sum(f[2] for f in frames if f[2] is not None)
        average_size = total_size // len(frames) if total_size and frames else None
        frame_count = len(frames)  # Count of images in the sequence

        missing_start = None
        for i in range(frames[0][0], frames[-1][0]):
            if i not in [f[0] for f in frames]:
                if missing_start is None:
                    missing_start = i
            else:
                if missing_start is not None:
                    if i - 1 == missing_start:
                        missing_ranges.append(f"{missing_start}")
                    else:
                        missing_ranges.append(f"{missing_start}-{i-1}")
                    missing_start = None

        if missing_start is not None:
            if frames[-1][0] - 1 == missing_start:
                missing_ranges.append(f"{missing_start}")
            else:
                missing_ranges.append(f"{missing_start}-{frames[-1][0]-1}")

        frame_range = f"[{frames[0][0]}-{frames[-1][0]}]"
        missing_str = f"[{', '.join(missing_ranges)}]" if missing_ranges else ""
        resolution_str = ", ".join(resolutions) if resolutions else None

        results.append(
            (
                relative_path,
                f"{base_name}",
                f"{sub_category}",
                frame_range,
                str(padding),
                extension,
                frame_count,
                resolution_str,
                missing_str,
                total_size,
                average_size,
            )
        )

    return results


def format_size(size):
    """Format bytes as a human-readable size"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024


def display_results(
    results,
    include_resolution=False,
    include_size=False,
    include_count=False,
    rv_mode=False,
):
    results.sort(key=lambda x: (x[0], x[1], x[3], x[2] != "", x[2]))

    if rv_mode:
        last_relative_path = None

        for (
            relative_path,
            name,
            sub_category,
            frame_range,
            padding,
            extension,
            count,
            resolution,
            missing,
            total_size,
            average_size,
        ) in results:
            full_name = f"{name}{sub_category}.*.{extension}"
            if relative_path != last_relative_path and last_relative_path is not None:
                print("")  # Add an empty line between different subdirectories
            if relative_path != ".":
                print(f"rv {os.path.join(relative_path, full_name)}")
            else:
                print(f"rv {full_name}")
            last_relative_path = relative_path

    else:
        # Calculate the optimal column widths
        max_path_len = max(len(res[0]) for res in results) + 2
        max_path_len = min(max_path_len, 30)  # Limit to 30 characters

        header = (
            f"{'path':<{max_path_len}} {'name':<20} {'range':<15} {'pad':<4} {'ext':<4}"
        )
        if include_count:
            header += f" {'count':<6}"
        if include_resolution:
            header += f" {'resolution':<12}"
        if include_size:
            header += (
                f"    {'size':<10} {'avg size':<10}"  # Added extra spaces before size
            )
        header += f" {'missing':<20}"

        # Print header and separator line
        print(header)
        print("=" * len(header))

        last_relative_path = None

        for (
            relative_path,
            name,
            sub_category,
            frame_range,
            padding,
            extension,
            count,
            resolution,
            missing,
            total_size,
            average_size,
        ) in results:
            if relative_path != last_relative_path and last_relative_path is not None:
                print("-" * len(header))

            path_display = relative_path if relative_path != last_relative_path else ""
            last_relative_path = relative_path

            full_name = f"{name}{sub_category}"
            line = f"{path_display:<{max_path_len}} {full_name:<20} {frame_range:<15} {padding:<4} {extension:<4}"
            if include_count:
                line += f" {count:<6}"
            if include_resolution:
                line += f" {resolution:<12}"
            if include_size:
                size_str = format_size(total_size) if total_size else ""
                avg_size_str = format_size(average_size) if average_size else ""
                line += f"    {size_str:<10} {avg_size_str:<10}"  # Added extra spaces before size
            line += f" {missing:<20}"
            print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Tool for detecting and listing image sequences in a directory."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Directory to analyze (default: current working directory)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively list sequences in subdirectories",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=1,
        help="Depth of recursion (only used if --recursive is set)",
    )
    parser.add_argument(
        "--resolution",
        action="store_true",
        help="Include resolution of images in the output",
    )
    parser.add_argument(
        "--size",
        action="store_true",
        help="Include size and average size of images in the output",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Include the count of images in each sequence",
    )
    parser.add_argument(
        "--rv",
        action="store_true",
        help="Generate ready-to-run commands for launching a player on the image sequences",
    )

    args = parser.parse_args()

    if args.rv:
        args.resolution = False  # Disable resolution if RV mode is enabled

    if not args.recursive:
        args.depth = 1  # Set depth to 1 if recursion is not enabled

    sequences = detect_sequences(
        args.directory,
        recursive=args.recursive,
        depth=args.depth,
        include_resolution=args.resolution,
        include_size=args.size,
    )
    display_results(
        sequences,
        include_resolution=args.resolution,
        include_size=args.size,
        include_count=args.count,
        rv_mode=args.rv,
    )


if __name__ == "__main__":
    main()
