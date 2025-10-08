import argparse
from pathlib import Path

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.camera_parser import CameraParser
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from dependencyinjection.di_container import DIContainer

def main():
    parser = argparse.ArgumentParser(description="Parse data from .bin files.")
    subparsers = parser.add_subparsers(dest="parser", help="Specify the parsing type.")

    # Camera parsing subparser
    camera_parser_cmd = subparsers.add_parser("camera", help="Parse camera data")
    camera_parser_cmd.add_argument("-o", "--output_dir", dest="output_dir", type=Path, required=True, help="Output directory")
    camera_parser_cmd.add_argument("-f", "--file", dest="file_name", type=Path, required=True, help="Path to the .bin data file")
    camera_parser_cmd.add_argument("-c", "--camera", dest="camera_name", type=ECamera, choices=[e for e in ECamera], help="Camera name")
    camera_parser_cmd.add_argument("-v", "--view", dest="view_name", type=EView, choices=[e for e in EView], help="View name")
    camera_parser_cmd.add_argument("-m", "--method", dest="export_method", type=ECameraExportMethod, default=ECameraExportMethod.JPG, choices=[e for e in ECameraExportMethod], help="Export method")
    camera_parser_cmd.add_argument("-d", "--disparity_scale", dest="disparity_scale", type=int, default=1, help="Disparity scale")
    camera_parser_cmd.add_argument("-a", "--mpo", dest="attempt_mpo_combining", action="store_true", help="Combine left and right images into a single .mpo file")

    # Handle main parser.
    container = DIContainer.get_container()
    args = parser.parse_args()

    # If camera target specified.
    if args.parser == "camera":
        camera_settings = CameraExportSettings(
            file_name=args.file_name,
            output_path=args.output_dir,
            camera=args.camera_name,
            view=args.view_name,
            export_method=args.export_method,
            disparity_scale=args.disparity_scale,
            attempt_mpo_combining=args.attempt_mpo_combining,
        )

        camera_handler = container[CameraParser]
        if args.camera_name is not None and args.view_name is not None:
            pass
        elif args.camera_name is not None:
            pass
        elif args.view_name is not None:
            pass
        else:
            camera_handler.parse_all(camera_settings)

    # No valid target.
    else:
        parser.print_help()

if __name__ == "__main__":
    main()