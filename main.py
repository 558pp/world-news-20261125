import hashlib
import os
import shutil
import tempfile
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().with_name("entry.png")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"

    with tempfile.TemporaryDirectory(dir=output_dir, prefix=".entry-") as staging_dir:
        staged = Path(staging_dir) / "entry.png"
        shutil.copyfile(source, staged)
        with source.open("rb") as original, staged.open("rb") as copied:
            expected = hashlib.file_digest(original, "sha256").digest()
            actual = hashlib.file_digest(copied, "sha256").digest()
        if actual != expected:
            raise RuntimeError("SHA-256 mismatch while copying entry.png")

        byte_count = staged.stat().st_size
        staged.replace(destination)

    print(f"Copied and verified {byte_count} bytes to {destination}")


if __name__ == "__main__":
    main()
