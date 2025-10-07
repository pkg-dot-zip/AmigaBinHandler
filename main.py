from pathlib import Path

from amiga.camera.camera_parser import CameraParser
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from dependencyinjection.di_container import DIContainer

if __name__ == "__main__":
    container = DIContainer.get_container()
    container[CameraParser].parse_all(Path("/home/lincoln/Documents/amiga_test/test_bin.bin"), Path("/home/lincoln/Documents/amiga_test/output/"), export_method=ECameraExportMethod.MP4)