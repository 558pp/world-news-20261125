from hashlib import file_digest
from os import environ
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory


def sha256(path: Path) -> bytes:
    with path.open("rb") as image:
        return file_digest(image, "sha256").digest()


def main() -> None:
    source = Path(__file__).resolve().with_name("entry.png")
    output_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    source_digest = sha256(source)

    with TemporaryDirectory(dir=output_dir) as staging_dir:
        copied_image = Path(staging_dir) / destination.name
        copyfile(source, copied_image)
        if sha256(copied_image) != source_digest:
            raise RuntimeError(f"SHA-256 mismatch while copying {source} to {destination}")
        byte_count = copied_image.stat().st_size
        copied_image.replace(destination)

    print(f"Verified {destination} ({byte_count} bytes)")


if __name__ == "__main__":
    main()
