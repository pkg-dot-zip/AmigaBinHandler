from dataclasses import dataclass
from pathlib import Path

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView


@dataclass
class CameraExportSettings:
    camera: ECamera
    view: EView
    file_name: Path
    output_path: Path
    disparity_scale: int
    video_to_jpg: bool