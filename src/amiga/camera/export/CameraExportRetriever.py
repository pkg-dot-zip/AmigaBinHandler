from amiga.camera.export.CameraJpgExporter import CameraJpgExporter
from amiga.camera.export.CameraMp4Exporter import CameraMp4Exporter
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from amiga.camera.export.ICameraExporter import ICameraExporter


class CameraExportRetriever:
    def __init__(self):
        self.jpg_exporter = CameraJpgExporter()
        self.mp4_exporter = CameraMp4Exporter()

    def get_retriever(self, method: ECameraExportMethod) -> ICameraExporter:
        if method == ECameraExportMethod.JPG:
            return self.jpg_exporter
        elif method == ECameraExportMethod.MP4:
            return self.mp4_exporter
        else:
            raise NotImplementedError()