"""Wrapper kecil untuk menjalankan fungsi `run_ga()` dari modul GA.

Awalnya file ini menunjuk ke berkas bernama "import_path (1).py" yang
mengandung spasi sehingga tidak bisa diimport secara normal. Untuk membuat
nya lebih fleksibel, sekarang behaviour berikut diterapkan:

- Jika opsi `--file` / `-f` diberikan, coba load dari path itu.
- Jika tidak diberikan, cari di direktori yang sama untuk file .py
    (kecuali file ini sendiri) yang mendefinisikan fungsi `run_ga()` dan
    pilih yang pertama ditemukan.

Cara pakai:
        python import_path.py
        python import_path.py --file path/to/ga_file.py

Return: meneruskan nilai yang dikembalikan oleh run_ga(), atau None jika
tidak ditemukan atau terjadi error.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from typing import Any, Tuple


def load_module_from_path(path: str, name: str = "loaded_module"):
    """Load a Python module from a filesystem path and return the module.

    This uses importlib to avoid issues with filenames that are not valid
    identifiers (spaces, parentheses, etc.).
    """
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_run_ga_in_directory(directory: str) -> list[str]:
    """Return list of python file paths in `directory` (excluding this file)
    that define `run_ga()` when loaded. The list is ordered by filename.
    This function does not import all modules permanently into sys.modules
    under their real names; it uses unique temporary names.
    """
    results: list[str] = []
    this_file = os.path.abspath(__file__)
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".py"):
            continue
        candidate = os.path.abspath(os.path.join(directory, name))
        if candidate == this_file:
            continue
        try:
            mod = load_module_from_path(candidate, name=f"_probe_{os.path.splitext(name)[0]}")
        except Exception:
            # ignore files that fail to import during probing
            continue
        if hasattr(mod, "run_ga"):
            results.append(candidate)
    return results


def main(argv: list[str] | None = None) -> Tuple[Any, ...] | None:
    """Entry point: temukan file GA dan jalankan run_ga().

    Jika file target berada di lokasi yang sama dengan file ini dan bernama
    "import_path (1).py", ia akan diload dan fungsi run_ga dipanggil.
    """
    parser = argparse.ArgumentParser(description="Run GA from sibling file")
    parser.add_argument("--file", "-f", help="Path to GA file",
                        default=None)
    args = parser.parse_args(argv)

    ga_path: str | None
    if args.file:
        ga_path = os.path.abspath(args.file)
        if not os.path.exists(ga_path):
            print(f"File not found: {ga_path}")
            return None
    else:
        # search current directory for a candidate implementing run_ga
        dirpath = os.path.dirname(os.path.abspath(__file__))
        candidates = find_run_ga_in_directory(dirpath)
        if not candidates:
            print("Tidak ditemukan berkas GA (tidak ada file .py sibling yang menyediakan run_ga())")
            return None
        if len(candidates) > 1:
            print("Beberapa kandidat GA ditemukan, menggunakan yang pertama:")
            for c in candidates:
                print(" -", c)
        ga_path = candidates[0]

    # load module and call run_ga if present
    try:
        mod = load_module_from_path(ga_path, name="ga_module")
    except Exception as e:
        print("Gagal memuat modul:", e)
        return None

    if not hasattr(mod, "run_ga"):
        print(f"Module {ga_path} tidak memiliki fungsi run_ga()")
        return None

    result = mod.run_ga()
    return result


if __name__ == "__main__":
    main()
