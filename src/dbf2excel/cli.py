from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from dbfread import DBF


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert all DBF files in the current directory to Excel files."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd(),
        help="Directory to scan for DBF files. Defaults to the current directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory for Excel files. Defaults to <source>/excel.",
    )
    parser.add_argument(
        "--encoding",
        default=None,
        help="Optional DBF encoding override, for example cp936 or gbk.",
    )
    return parser


def find_dbf_files(source_dir: Path) -> list[Path]:
    return sorted(path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() == ".dbf")


def convert_file(dbf_path: Path, output_dir: Path, encoding: str | None = None) -> Path:
    table = DBF(
        str(dbf_path),
        load=True,
        encoding=encoding,
        ignore_missing_memofile=True,
        char_decode_errors="ignore",
    )
    rows = [dict(record) for record in table]
    dataframe = pd.DataFrame(rows, columns=table.field_names)
    output_path = output_dir / f"{dbf_path.stem}.xlsx"
    dataframe.to_excel(output_path, index=False)
    return output_path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_dir = args.source.resolve()
    output_dir = args.output.resolve() if args.output else source_dir / "excel"

    if not source_dir.exists():
        print(f"Source directory does not exist: {source_dir}", file=sys.stderr)
        return 1

    if not source_dir.is_dir():
        print(f"Source path is not a directory: {source_dir}", file=sys.stderr)
        return 1

    dbf_files = find_dbf_files(source_dir)
    if not dbf_files:
        print(f"No DBF files found in: {source_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[Path, str]] = []
    for dbf_file in dbf_files:
        try:
            excel_path = convert_file(dbf_file, output_dir, encoding=args.encoding)
            print(f"Converted: {dbf_file.name} -> {excel_path.name}")
        except Exception as exc:  # noqa: BLE001
            failures.append((dbf_file, str(exc)))
            print(f"Failed: {dbf_file.name} ({exc})", file=sys.stderr)

    if failures:
        print(f"{len(failures)} file(s) failed to convert.", file=sys.stderr)
        return 1

    print(f"Done. Excel files saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
