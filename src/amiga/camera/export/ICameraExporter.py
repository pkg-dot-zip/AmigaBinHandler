from abc import ABC, abstractmethod

from farm_ng.core.events_file_reader import EventLogPosition

from amiga.camera.export.CameraExportSettings import CameraExportSettings


class ICameraExporter(ABC):
    @abstractmethod
    def export(self, camera_events: list[EventLogPosition], camera_export_settings: CameraExportSettings):
        """
        Starts exporting camera data.
        :param camera_events: List of events to export data for.
        :param camera_export_settings: The settings to export with.
        """
        pass