#!/usr/bin/env python3
"""Image Orientation Rotator CLI.

A command-line tool that automatically detects and fixes image orientation
using machine learning models from the check_orientation library.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click
from PIL import Image
from tqdm import tqdm

if TYPE_CHECKING:
    pass

try:
    from check_orientation import check_orientation
except ImportError:
    print(
        "Error: check_orientation library not installed. Run: uv add check_orientation"
    )  # noqa: T201
    sys.exit(1)


class ImageRotator:
    """Handles image rotation detection and correction."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

    def __init__(self, model_name: str = "swsl_resnext50_32x4d") -> None:
        """Initialize the rotator with a specific model."""
        self.model_name = model_name

    def is_image_file(self, file_path: Path) -> bool:
        """Check if file is a supported image format."""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS

    def find_images(self, directory: Path, recursive: bool = True) -> list[Path]:
        """Find all image files in directory."""
        images = []

        if recursive:
            for file_path in directory.rglob("*"):
                if file_path.is_file() and self.is_image_file(file_path):
                    images.append(file_path)
        else:
            for file_path in directory.iterdir():
                if file_path.is_file() and self.is_image_file(file_path):
                    images.append(file_path)

        return sorted(images)

    def detect_rotation(self, image_path: Path) -> int:
        """Detect the rotation angle of an image."""
        try:
            # Use check_orientation to predict rotation
            return check_orientation(str(image_path))
        except Exception as e:  # noqa: BLE001
            click.echo(f"Error detecting rotation for {image_path}: {e}", err=True)
            return 0

    def rotate_image(
        self, image_path: Path, rotation: int, *, backup: bool = True
    ) -> bool:
        """Rotate image by the specified angle."""
        if rotation == 0:
            return True  # No rotation needed

        try:
            # Create backup if requested
            if backup:
                backup_path = image_path.with_suffix(f".backup{image_path.suffix}")
                if not backup_path.exists():
                    image_path.rename(backup_path)
                    source_path = backup_path
                else:
                    source_path = image_path
            else:
                source_path = image_path

            # Open and rotate image
            with Image.open(source_path) as img:
                # Convert rotation to PIL rotation (counterclockwise)
                pil_rotation = (360 - rotation) % 360
                rotated_img = img.rotate(pil_rotation, expand=True)

                # Save the corrected image
                rotated_img.save(image_path, quality=95, optimize=True)

            return True

        except Exception as e:  # noqa: BLE001
            click.echo(f"Error rotating {image_path}: {e}", err=True)
            return False

    def process_image(
        self, image_path: Path, *, backup: bool = True, dry_run: bool = False
    ) -> tuple[bool, int]:
        """Process a single image: detect and correct rotation."""
        rotation = self.detect_rotation(image_path)

        if dry_run:
            return True, rotation

        if rotation != 0:
            success = self.rotate_image(image_path, rotation, backup=backup)
            return success, rotation

        return True, 0


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    default=True,
    help="Process subdirectories recursively",
)
@click.option("--no-backup", is_flag=True, help="Do not create backup files")
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Show what would be done without making changes",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option(
    "--model",
    default="swsl_resnext50_32x4d",
    help="Model to use for orientation detection",
)
def main(
    directory: Path,
    recursive: bool,
    no_backup: bool,
    dry_run: bool,
    verbose: bool,
    model: str,
) -> None:
    """Automatically detect and fix image orientation in a directory.

    DIRECTORY: Path to the directory containing images to process.
    """

    click.echo(f"🔍 Scanning for images in: {directory}")

    rotator = ImageRotator(model)
    images = rotator.find_images(directory, recursive)

    if not images:
        click.echo("❌ No supported image files found")
        return

    click.echo(f"📸 Found {len(images)} image(s)")

    if dry_run:
        click.echo("🔍 DRY RUN - No changes will be made")

    processed = 0
    rotated = 0
    errors = 0

    with tqdm(images, desc="Processing images", unit="img") as pbar:
        for image_path in pbar:
            pbar.set_description(f"Processing {image_path.name}")

            success, rotation = rotator.process_image(
                image_path,
                backup=not no_backup,
                dry_run=dry_run,
            )

            if success:
                processed += 1
                if rotation != 0:
                    rotated += 1
                    if verbose or dry_run:
                        action = "Would rotate" if dry_run else "Rotated"
                        click.echo(f"  {action} {image_path.name} by {rotation}°")
            else:
                errors += 1

    # Summary
    click.echo("\n📊 Summary:")
    click.echo(f"  Processed: {processed}/{len(images)}")
    click.echo(f"  Rotated: {rotated}")
    click.echo(f"  Errors: {errors}")

    if errors > 0:
        click.echo(f"❌ {errors} error(s) occurred during processing")
        sys.exit(1)
    else:
        action = "would be" if dry_run else "were"
        click.echo(f"✅ {rotated} image(s) {action} rotated successfully")


if __name__ == "__main__":
    main()
