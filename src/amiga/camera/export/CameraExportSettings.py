from dataclasses import dataclass
from pathlib import Path

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod


@dataclass
class CameraExportSettings:
    """Contains all settings for exporting camera data."""
    camera: ECamera
    view: EView
    export_method: ECameraExportMethod
    file_name: Path
    output_path: Path
    disparity_scale: int
