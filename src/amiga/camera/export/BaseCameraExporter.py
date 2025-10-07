from abc import ABC, abstractmethod

import cv2
import numpy as np
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.oak import oak_pb2
from tqdm import tqdm

from amiga.camera.EView import EView
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from amiga.camera.export.ICameraExporter import ICameraExporter


class BaseCameraExporter(ICameraExporter, ABC):
    def export(self, camera_events: list[EventLogPosition], camera_export_settings: CameraExportSettings):
        event_log: EventLogPosition
        for event_log in tqdm(camera_events):
            # parse the message
            sample: oak_pb2.OakFrame = event_log.read_message()

            # decode image
            img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)
            if camera_export_settings.view == EView.DISPARITY:
                disparity_scale: int = max(1, int(camera_export_settings.disparity_scale))
                img = cv2.applyColorMap(img * disparity_scale, cv2.COLORMAP_JET)

            self.handle_frame(event_log, sample, img, camera_export_settings)

        self.close()

    @abstractmethod
    def handle_frame(self, event_log: EventLogPosition, sample: oak_pb2.OakFrame, img: cv2.Mat, camera_export_settings: CameraExportSettings):
        pass

    @abstractmethod
    def close(self):
        pass