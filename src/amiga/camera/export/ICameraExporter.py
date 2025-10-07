from abc import ABC, abstractmethod

from farm_ng.core.events_file_reader import EventLogPosition

from amiga.camera.export.CameraExportSettings import CameraExportSettings


class ICameraExporter(ABC):
    @abstractmethod
    def export(self, camera_events: list[EventLogPosition], camera_export_settings: CameraExportSettings):
        pass