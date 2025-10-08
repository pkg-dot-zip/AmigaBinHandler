from __future__ import annotations

from pathlib import Path

from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import build_events_dict

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.CameraExportRetriever import CameraExportRetriever
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from logger.ILogger import ILogger
from util.mpo_merger import MPOMerger


class CameraParser:
    def __init__(self, logger: ILogger, mpo_merger: MPOMerger, camera_export_retriever: CameraExportRetriever):
        self.logger = logger
        self.mpo_merger = mpo_merger
        self.camera_export_retriever = camera_export_retriever

    def parse_all(self, file_name: Path, output_path: Path, disparity_scale: int = 1,
            export_method: ECameraExportMethod = ECameraExportMethod.JPG) -> None:
        """Parses all possible camera information from an 'events.bin' file."""
        for camera in ECamera:
            for view in EView:
                self.parse(file_name, output_path, camera, view, disparity_scale, export_method)

    def parse(
            self, file_name: Path, output_path: Path, camera: ECamera = ECamera.OAK0, view: EView = EView.RGB, disparity_scale: int = 1,
            export_method: ECameraExportMethod = ECameraExportMethod.JPG, attempt_mpo_combining: bool = True
    ) -> bool:
        """
        Parses camera information from an 'events.bin' file.

        :param file_name: Path to the `events.bin` file.
        :param output_path: Path to the folder where converted data will be written.
        :param camera: The name of the camera to visualize. Default: oak0.
        :param view: The name of the camera view to visualize. Default: rbg.
        :param disparity_scale: Scale for amplifying disparity color mapping. Default: 1.
        :param export_method: Type to export.
        :param attempt_mpo_combining: If found, merges left and right image into a single .mpo file. Does not remove original files.
        """
        # Create the file reader.
        reader = EventsFileReader(file_name)
        success: bool = reader.open()
        if not success:
            self.logger.error(f"Failed to open events file: {file_name}")
            return False

        # Get the index of the events file.
        events_index: list[EventLogPosition] = reader.get_index()

        # Structure the index as a dictionary of lists of events.
        events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)

        # customize camera and view
        topic_name = f"/{camera}/{view}"
        if topic_name not in events_dict:
            self.logger.error(f"Camera view not found: {topic_name}")
            return False

        camera_events: list[EventLogPosition] = events_dict[topic_name]

        camera_export_settings = CameraExportSettings(
            camera=camera,
            file_name=file_name,
            output_path=output_path,
            view=view,
            disparity_scale=disparity_scale,
            export_method=export_method,
            attempt_mpo_combining=attempt_mpo_combining,
        )

        # Export.
        exporter = self.camera_export_retriever.get_retriever(camera_export_settings.export_method)
        exporter.export(camera_events, camera_export_settings)

        # Close resources.
        reader.close()

        # MPO.
        if camera_export_settings.attempt_mpo_combining:
            self.__create_mpo_files(camera_export_settings.output_path)

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