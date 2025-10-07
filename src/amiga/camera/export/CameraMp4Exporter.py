from typing import Optional

import cv2
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.oak import oak_pb2

from amiga.camera.export.BaseCameraExporter import BaseCameraExporter
from amiga.camera.export.CameraExportSettings import CameraExportSettings


class CameraMp4Exporter(BaseCameraExporter):
    def __init__(self):
        self.video_writer: Optional[cv2.VideoWriter] = None

    def handle_frame(self, event_log: EventLogPosition, sample: oak_pb2.OakFrame, img: cv2.Mat,
                     camera_export_settings: CameraExportSettings):
        # create the video writer if it doesn't exist
        if self.video_writer is None:
            height, width, _ = img.shape
            file_path = camera_export_settings.file_name.parent if not camera_export_settings.output_path else camera_export_settings.output_path.absolute()
            video_name = file_path / (camera_export_settings.file_name.stem + f".{camera_export_settings.view}.mp4")
            self.video_writer = cv2.VideoWriter(str(video_name), cv2.VideoWriter_fourcc(*'mp4v'), 10,
                                                (width, height))

        # write the frame to the video
        self.video_writer.write(img)

    def close(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None