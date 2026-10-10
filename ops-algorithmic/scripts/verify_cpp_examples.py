#!/usr/bin/env python3
"""Extract standalone C++ examples from references/cpp-examples.md and verify them."""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

FENCE = re.compile(r"```cpp compile-example\n(.*?)\n```", re.DOTALL)


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    source = root / "references" / "cpp-examples.md"
    compiler = shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        print("No C++ compiler found; cannot verify examples.", file=sys.stderr)
        return 2

    text = source.read_text(encoding="utf-8")
    blocks = FENCE.findall(text)
    if not blocks:
        print("No compile-example blocks found.", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="skill-cpp-examples-") as temp_dir:
        temp = pathlib.Path(temp_dir)
        for index, block in enumerate(blocks, start=1):
            cpp = temp / f"example_{index}.cpp"
            exe = temp / f"example_{index}"
            cpp.write_text(block + "\n", encoding="utf-8")
            compile_result = subprocess.run(
                [compiler, "-std=c++20", "-O2", "-Wall", "-Wextra", "-pedantic", str(cpp), "-o", str(exe)],
                text=True,
                capture_output=True,
                check=False,
            )
            if compile_result.returncode != 0:
                print(f"Example {index} failed to compile:\n{compile_result.stderr}", file=sys.stderr)
                return 1
            run_result = subprocess.run([str(exe)], check=False)
            if run_result.returncode != 0:
                print(f"Example {index} returned {run_result.returncode}.", file=sys.stderr)
                return 1

    print(f"Verified {len(blocks)} C++20 examples with {pathlib.Path(compiler).name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
