from pathlib import Path

from amiga.camera.camera_parser import CameraParser
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from dependencyinjection.di_container import DIContainer

def main():
    # First handle arguments.
    # TODO: Add argument handler.

    # The start executing our code.
    container = DIContainer.get_container()
    container[CameraParser].parse_all(Path("/home/lincoln/Documents/amiga_test/test_bin.bin"),
                                      Path("/home/lincoln/Documents/amiga_test/output/"),
                                      export_method=ECameraExportMethod.JPG)

if __name__ == "__main__":
    main()