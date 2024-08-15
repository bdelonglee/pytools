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
<<<<<<< HEAD
    """
    Parcours le répertoire donné et détecte les séquences d'images.
    Retourne une liste de séquences trouvées avec leurs informations associées.

    :param directory: Le répertoire de départ à analyser
    :param recursive: Si vrai, analyse les sous-répertoires
    :param depth: Profondeur maximale de l'analyse (seulement si recursive est vrai)
    :param include_resolution: Si vrai, inclut la résolution des images dans les résultats
    :param include_size: Si vrai, inclut la taille et la taille moyenne des images dans les résultats
    :return: Une liste de tuples représentant les séquences d'images détectées
    """
    sequences = defaultdict(list)

    # Expression régulière pour identifier les fichiers de séquence
    regex = re.compile(r"^(.*?)(\.\w+)?\.(\d+)\.(\w+)$")

    def explore_directory(current_directory, current_depth, base_path):
        """
        Explore un répertoire donné pour détecter des séquences d'images.

        :param current_directory: Répertoire courant à analyser
        :param current_depth: Profondeur actuelle dans l'arborescence de répertoires
        :param base_path: Chemin de base utilisé pour calculer le chemin relatif
        """
=======
    sequences = defaultdict(list)

    regex = re.compile(r"^(.*?)(\.\w+)?\.(\d+)\.(\w+)$")

    def explore_directory(current_directory, current_depth, base_path):
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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

<<<<<<< HEAD
                    # Obtenir la résolution de l'image si demandé
=======
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
                    if include_resolution:
                        with Image.open(file_path) as img:
                            resolution = f"{img.width}x{img.height}"
                    else:
                        resolution = None

<<<<<<< HEAD
                    # Obtenir la taille du fichier si demandé
=======
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
                    file_size = os.path.getsize(file_path) if include_size else None

                    sequences[key].append((frame_number, resolution, file_size))

<<<<<<< HEAD
            # Si la récursion est activée et qu'on n'a pas encore atteint la profondeur maximale
=======
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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
<<<<<<< HEAD
        frame_count = len(frames)  # Nombre d'images dans la séquence

        # Détection des frames manquantes
=======
        frame_count = len(frames)  # Count of images in the sequence

>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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
<<<<<<< HEAD
    """
    Formate une taille en octets pour être plus lisible (par ex. en KB, MB, etc.).

    :param size: Taille en octets
    :return: Taille formatée en chaîne de caractères
    """
=======
    """Format bytes as a human-readable size"""
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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
<<<<<<< HEAD
    """
    Affiche les résultats des séquences d'images détectées de manière formatée ou sous forme de commandes `rv`.

    :param results: Liste des séquences à afficher
    :param include_resolution: Si vrai, inclut la résolution des images dans l'affichage
    :param include_size: Si vrai, inclut la taille totale et la taille moyenne des images dans l'affichage
    :param include_count: Si vrai, inclut le nombre d'images dans chaque séquence
    :param rv_mode: Si vrai, génère des commandes `rv` pour chaque séquence
    """
    # Trier les résultats par chemin, nom, etc.
=======
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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
<<<<<<< HEAD
                print("")  # Ajouter une ligne vide entre les sous-dossiers
=======
                print("")  # Add an empty line between different subdirectories
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
            if relative_path != ".":
                print(f"rv {os.path.join(relative_path, full_name)}")
            else:
                print(f"rv {full_name}")
            last_relative_path = relative_path

    else:
<<<<<<< HEAD
        # Calculer les largeurs de colonnes optimales
        max_path_len = max(len(res[0]) for res in results) + 2
        max_path_len = min(max_path_len, 30)  # Limiter à 30 caractères
=======
        # Calculate the optimal column widths
        max_path_len = max(len(res[0]) for res in results) + 2
        max_path_len = min(max_path_len, 30)  # Limit to 30 characters
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69

        header = (
            f"{'path':<{max_path_len}} {'name':<20} {'range':<15} {'pad':<4} {'ext':<4}"
        )
        if include_count:
            header += f" {'count':<6}"
        if include_resolution:
            header += f" {'resolution':<12}"
        if include_size:
<<<<<<< HEAD
            header += f"    {'size':<10} {'avg size':<10}"  # Ajouter des espaces supplémentaires avant size
        header += f" {'missing':<20}"

        # Imprimer l'en-tête et la ligne de séparation
=======
            header += (
                f"    {'size':<10} {'avg size':<10}"  # Added extra spaces before size
            )
        header += f" {'missing':<20}"

        # Print header and separator line
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
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
<<<<<<< HEAD
                line += f"    {size_str:<10} {avg_size_str:<10}"  # Ajouter des espaces supplémentaires avant size
=======
                line += f"    {size_str:<10} {avg_size_str:<10}"  # Added extra spaces before size
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
            line += f" {missing:<20}"
            print(line)


def main():
<<<<<<< HEAD
    # Configuration de l'analyseur d'arguments pour le script
    parser = argparse.ArgumentParser(
        description="Outil pour détecter et lister les séquences d'images dans un répertoire.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
=======
    parser = argparse.ArgumentParser(
        description="Tool for detecting and listing image sequences in a directory."
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
<<<<<<< HEAD
        help="Répertoire à analyser (par défaut : répertoire courant)",
=======
        help="Directory to analyze (default: current working directory)",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
<<<<<<< HEAD
        help="Lister récursivement les séquences dans les sous-répertoires",
=======
        help="Recursively list sequences in subdirectories",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=1,
<<<<<<< HEAD
        help="Profondeur de la récursion (utilisé seulement si --recursive est activé)",
=======
        help="Depth of recursion (only used if --recursive is set)",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "--resolution",
        action="store_true",
<<<<<<< HEAD
        help="Inclure la résolution des images dans la sortie",
=======
        help="Include resolution of images in the output",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "--size",
        action="store_true",
<<<<<<< HEAD
        help="Inclure la taille totale et la taille moyenne des images dans la sortie",
=======
        help="Include size and average size of images in the output",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "--count",
        action="store_true",
<<<<<<< HEAD
        help="Inclure le nombre d'images dans chaque séquence",
=======
        help="Include the count of images in each sequence",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )
    parser.add_argument(
        "--rv",
        action="store_true",
<<<<<<< HEAD
        help="Générer des commandes prêtes à exécuter pour lancer un player sur les séquences d'images",
=======
        help="Generate ready-to-run commands for launching a player on the image sequences",
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    )

    args = parser.parse_args()

    if args.rv:
<<<<<<< HEAD
        args.resolution = False  # Désactiver la résolution si le mode RV est activé

    if not args.recursive:
        args.depth = 1  # Limiter la profondeur à 1 si la récursion n'est pas activée

    # Détecter les séquences d'images
=======
        args.resolution = False  # Disable resolution if RV mode is enabled

    if not args.recursive:
        args.depth = 1  # Set depth to 1 if recursion is not enabled

>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    sequences = detect_sequences(
        args.directory,
        recursive=args.recursive,
        depth=args.depth,
        include_resolution=args.resolution,
        include_size=args.size,
    )
<<<<<<< HEAD

    # Afficher les résultats
=======
>>>>>>> 816dfba4c13302be6fda2bd845e25e7aae74ab69
    display_results(
        sequences,
        include_resolution=args.resolution,
        include_size=args.size,
        include_count=args.count,
        rv_mode=args.rv,
    )


if __name__ == "__main__":
    main()
