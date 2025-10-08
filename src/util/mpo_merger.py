from pathlib import Path

from logger.ILogger import ILogger


class MPOMerger:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def merge_folders(self, export_dir: Path, left_dir: Path, right_dir: Path):
        """Assumes left and right dir children file names are equal. Will skip entries that are not in both."""

        if not left_dir.exists() or not right_dir.exists():
            return

        # TODO: Check if image is actually image.
        for image in left_dir.iterdir():
            left_image = image
            right_image = right_dir / image.name

            if right_image.exists():
                self.merge(export_dir / (image.stem + ".mpo"), left_image, right_image)

    def merge(self, export_path: Path, img_path_1: Path, img_path_2: Path):
        """Merges two images into a single .mpo image."""
        # TODO: Check if image is actually image.

        if not img_path_1.exists() or not img_path_2.exists():
            return

        from PIL import Image
        im1 = Image.open(img_path_1)
        im2 = Image.open(img_path_2)
        im1.save(export_path, save_all=True, append_images=[im2], format='MPO')
        self.logger.info(f"Saved new mpo file to {export_path}")