import cv2
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.oak import oak_pb2

from amiga.camera.export.BaseCameraExporter import BaseCameraExporter
from amiga.camera.export.CameraExportSettings import CameraExportSettings


class CameraJpgExporter(BaseCameraExporter):
    def close(self):
        pass

    def handle_frame(self, event_log: EventLogPosition, sample: oak_pb2.OakFrame, img: cv2.Mat, camera_export_settings: CameraExportSettings):
        # write frame to jpg
        file_path = camera_export_settings.file_name.parent if not camera_export_settings.output_path else camera_export_settings.output_path.absolute()
        file_path = file_path / camera_export_settings.file_name.stem / f"{camera_export_settings.camera}" / f"{camera_export_settings.view}"
        if not file_path.exists():
            file_path.mkdir(parents=True, exist_ok=True)

        # write the frame to the path
        frame_name: str = f"frame_{sample.meta.sequence_num:06d}.jpg"
        cv2.imwrite(str(file_path / frame_name), img)