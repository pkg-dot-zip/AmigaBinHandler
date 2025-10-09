from pathlib import Path

from lagom import Container

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from amiga.camera.camera_parser import CameraParser
from amiga.camera.export.CameraExportSettings import CameraExportSettings
from amiga.camera.export.ECameraExportMethod import ECameraExportMethod
from parser.IArgParser import IArgParser


class CameraArgParser(IArgParser):
    def get_component_name(self) -> str:
        return "camera"

    def add_parser(self, subparser_root):
        camera_parser_cmd = subparser_root.add_parser(self.get_component_name(), help="Parse camera data")
        camera_parser_cmd.add_argument("-o", "--output_dir", dest="output_dir", type=Path, required=True,
                                       help="Output directory")
        camera_parser_cmd.add_argument("-f", "--file", dest="file_name", type=Path, required=True,
                                       help="Path to the .bin data file")
        camera_parser_cmd.add_argument("-c", "--camera", dest="camera_name", type=ECamera, choices=[e for e in ECamera],
                                       help="Camera name")
        camera_parser_cmd.add_argument("-v", "--view", dest="view_name", type=EView, choices=[e for e in EView],
                                       help="View name")
        camera_parser_cmd.add_argument("-m", "--method", dest="export_method", type=ECameraExportMethod,
                                       default=ECameraExportMethod.JPG, choices=[e for e in ECameraExportMethod],
                                       help="Export method")
        camera_parser_cmd.add_argument("-d", "--disparity_scale", dest="disparity_scale", type=int, default=1,
                                       help="Disparity scale")
        camera_parser_cmd.add_argument("-a", "--mpo", dest="attempt_mpo_combining", action="store_true",
                                       help="Combine left and right images into a single .mpo file")

    def handle_parse(self, args, container: Container):
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
            camera_handler.parse(camera_settings)
        elif args.camera_name is not None:
            for v in EView:
                camera_settings.view = v
                camera_handler.parse(camera_settings)
        elif args.view_name is not None:
            for c in ECamera:
                camera_settings.camera = c
                camera_handler.parse(camera_settings)
        else:
            camera_handler.parse_all(camera_settings)