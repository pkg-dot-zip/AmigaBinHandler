from dataclasses import dataclass
from pathlib import Path

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod


@dataclass
class CameraExportSettings:
    """Contains all settings for exporting camera data."""

    file_name: Path
    """Path to the `events.bin` file."""

    output_path: Path
    """Path to the folder where converted data will be written."""

    camera: ECamera = ECamera.OAK0
    """The name of the camera to visualize. Default: oak0."""

    view: EView = EView.RGB
    """The name of the camera view to visualize. Default: rbg."""

    export_method: ECameraExportMethod = ECameraExportMethod.JPG
    """Type to export. Default: jpg"""

    disparity_scale: int = 1
    """Scale for amplifying disparity color mapping. Default: 1."""

    attempt_mpo_combining: bool = True
    """If found, merges left and right image into a single .mpo file. Does not remove original files."""
