from __future__ import annotations

from pathlib import Path

from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import build_events_dict

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.CameraExportRetriever import CameraExportRetriever
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from logger.ILogger import ILogger
from util.mpo_merger import MPOMerger


class CameraParser:
    def __init__(self, logger: ILogger, mpo_merger: MPOMerger, camera_export_retriever: CameraExportRetriever):
        self.logger = logger
        self.mpo_merger = mpo_merger
        self.camera_export_retriever = camera_export_retriever

    def parse_all(self, export_settings: CameraExportSettings) -> None:
        """Parses all possible camera information from an 'events.bin' file."""
        for camera in ECamera:
            for view in EView:
                export_settings.camera = camera
                export_settings.view = view
                self.parse(export_settings)

    def parse(
            self, export_settings: CameraExportSettings
    ) -> bool:
        """
        Parses camera information from an 'events.bin' file.
        """
        # Create the file reader.
        reader = EventsFileReader(export_settings.file_name)
        success: bool = reader.open()
        if not success:
            self.logger.error(f"Failed to open events file: {export_settings.file_name}")
            return False

        # Get the index of the events file.
        events_index: list[EventLogPosition] = reader.get_index()

        # Structure the index as a dictionary of lists of events.
        events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)

        # Customize camera and view.
        topic_name = f"/{export_settings.camera}/{export_settings.view}"
        if topic_name not in events_dict:
            self.logger.error(f"Camera view not found: {topic_name}")
            return False

        camera_events: list[EventLogPosition] = events_dict[topic_name]

        # Export.
        exporter = self.camera_export_retriever.get_retriever(export_settings.export_method)
        exporter.export(camera_events, export_settings)

        # Close resources.
        reader.close()

        # MPO.
        if export_settings.attempt_mpo_combining:
            self.__create_mpo_files(export_settings.output_path)

        return True


    def __create_mpo_files(self, root_path: Path) -> None:
        """Create mpo files from left & right images."""
        for child_dir in root_path.iterdir():
            if child_dir.is_dir():
                for camera in ECamera:
                    cam_dir_path = child_dir / f"{camera}"
                    left_dir_path = cam_dir_path / EView.LEFT
                    right_dir_path = cam_dir_path / EView.RIGHT
                    mpo_output_dir_path = (cam_dir_path / "mpo")
                    mpo_output_dir_path.mkdir(parents=True, exist_ok=True)

                    if left_dir_path.exists() and right_dir_path.exists():
                        self.mpo_merger.merge_folders(mpo_output_dir_path, left_dir_path, right_dir_path)