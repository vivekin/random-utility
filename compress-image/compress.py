#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
import sys


# =========================
# Configuration
# =========================

INPUT_DIR = Path("testedit")
OUTPUT_DIR = Path("output")

JPEG_QUALITY = 40

# Set to True to process subdirectories recursively
RECURSIVE = False


# =========================
# Processing
# =========================

def process_image(input_path: Path, output_path: Path):
    try:
        with Image.open(input_path) as img:

            # Only process JPEG images
            if img.format != "JPEG":
                print(f"SKIP  {input_path} (not JPEG)")
                return

            original_size = img.size

            # Preserve EXIF exactly as stored in the source JPEG.
            exif_data = img.info.get("exif")

            # Preserve ICC color profile.
            icc_profile = img.info.get("icc_profile")

            # Convert to RGB if necessary.
            # Normal mobile JPEGs should already be RGB.
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Make sure output directory exists.
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Re-encode JPEG.
            #
            # We explicitly provide:
            #   exif        -> preserves EXIF
            #   icc_profile -> preserves ICC profile
            #
            # We do NOT copy arbitrary APP5-APP8 data.
            save_options = {
                "format": "JPEG",
                "quality": JPEG_QUALITY,
                "optimize": True,
            }

            if exif_data is not None:
                save_options["exif"] = exif_data

            if icc_profile is not None:
                save_options["icc_profile"] = icc_profile

            img.save(output_path, **save_options)

            # Verify output.
            with Image.open(output_path) as result:
                new_size = result.size

                if new_size != original_size:
                    raise RuntimeError(
                        f"Dimension changed: "
                        f"{original_size} -> {new_size}"
                    )

            original_bytes = input_path.stat().st_size
            output_bytes = output_path.stat().st_size

            reduction = (
                (1 - output_bytes / original_bytes) * 100
                if original_bytes
                else 0
            )

            print(
                f"OK    {input_path} -> {output_path}\n"
                f"      Dimensions : {original_size[0]}x{original_size[1]}\n"
                f"      Quality    : {JPEG_QUALITY}\n"
                f"      Size       : "
                f"{original_bytes / 1024 / 1024:.2f} MB -> "
                f"{output_bytes / 1024 / 1024:.2f} MB "
                f"({reduction:.1f}% smaller)"
            )

    except Exception as e:
        print(f"ERROR {input_path}: {e}")


def main():
    if not INPUT_DIR.exists():
        print(f"Input directory does not exist: {INPUT_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if RECURSIVE:
        files = INPUT_DIR.rglob("*")
    else:
        files = INPUT_DIR.glob("*")

    jpeg_files = [
        p for p in files
        if p.is_file()
        and p.suffix.lower() in (".jpg", ".jpeg")
    ]

    if not jpeg_files:
        print("No JPEG files found.")
        return

    print(f"Found {len(jpeg_files)} JPEG file(s)")
    print(f"JPEG quality: {JPEG_QUALITY}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    for input_path in jpeg_files:

        # Preserve directory structure when RECURSIVE=True
        relative_path = input_path.relative_to(INPUT_DIR)
        output_path = OUTPUT_DIR / relative_path

        process_image(input_path, output_path)

    print("\nDone.")


if __name__ == "__main__":
    main()