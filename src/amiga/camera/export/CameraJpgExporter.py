import cv2
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.oak import oak_pb2

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.export.BaseCameraExporter import BaseCameraExporter
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from logger.Logger import Logger
from util.mpo_merger import MPOMerger


class CameraJpgExporter(BaseCameraExporter):
    def __init__(self):
        # TODO: Grab from DI.
        self.mpo_merger = MPOMerger(Logger())

    def handle_frame(self, event_log: EventLogPosition, sample: oak_pb2.OakFrame, img: cv2.Mat, camera_export_settings: CameraExportSettings):
        # write frame to jpg
        file_path = camera_export_settings.file_name.parent if not camera_export_settings.output_path else camera_export_settings.output_path.absolute()
        file_path = file_path / camera_export_settings.file_name.stem / f"{camera_export_settings.camera}" / f"{camera_export_settings.view}"
        if not file_path.exists():
            file_path.mkdir(parents=True, exist_ok=True)

        # write the frame to the path
        frame_name: str = f"frame_{sample.meta.sequence_num:06d}.jpg"
        cv2.imwrite(str(file_path / frame_name), img)


    def close(self, camera_export_settings: CameraExportSettings):

        # Create mpo files from left & right images.
        if camera_export_settings.attempt_mpo_combining:
            root_path = camera_export_settings.output_path

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
