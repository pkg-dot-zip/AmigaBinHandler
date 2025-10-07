from __future__ import annotations

from pathlib import Path

from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import build_events_dict

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from amiga.camera.export.CameraJpgExporter import CameraJpgExporter
from amiga.camera.export.CameraMp4Exporter import CameraMp4Exporter
from logger.ILogger import ILogger


class CameraParser:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def parse(
            self, file_name: Path, output_path: Path, camera: ECamera = ECamera.OAK0, view: EView = EView.RGB, disparity_scale: int = 1,
            video_to_jpg: bool = True
    ) -> None:
        # create the file reader
        reader = EventsFileReader(file_name)
        success: bool = reader.open()
        if not success:
            raise RuntimeError(f"Failed to open events file: {file_name}")

        # get the index of the events file
        events_index: list[EventLogPosition] = reader.get_index()

        # structure the index as a dictionary of lists of events
        events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)

        self.logger.info(f"All available topics: {sorted(events_dict.keys())}")

        # customize camera and view
        topic_name = f"/{camera}/{view}"
        if topic_name not in events_dict:
            raise RuntimeError(f"Camera view not found: {topic_name}")

        camera_events: list[EventLogPosition] = events_dict[topic_name]

        camera_export_settings = CameraExportSettings(
            camera=camera,
            file_name=file_name,
            output_path=output_path,
            view=view,
            disparity_scale=disparity_scale,
            video_to_jpg=video_to_jpg
        )

        if camera_export_settings.video_to_jpg:
            CameraJpgExporter().export(camera_events, camera_export_settings)
        else:
            CameraMp4Exporter().export(camera_events, camera_export_settings)

        reader.close()
