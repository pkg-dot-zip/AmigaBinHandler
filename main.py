import argparse
from pathlib import Path

from amiga.camera_parser import CameraParser
from dependencyinjection.di_container import DIContainer


def old_code():
    parser = argparse.ArgumentParser(prog="python main.py", description="Event file converter example.")
    parser.add_argument("--file-name", type=Path, required=True, help="Path to the `events.bin` file.")
    parser.add_argument("--output-path", type=Path, help="Path to the folder where converted data will be written.")
    parser.add_argument(
        "--camera-name", type=str, default="oak0", help="The name of the camera to visualize. Default: oak0."
    )
    parser.add_argument(
        "--view-name",
        type=str,
        default="rgb",
        choices=["rgb", "left", "right", "disparity"],
        help="The name of the camera view to visualize. Default: rbg.",
    )
    parser.add_argument(
        "--disparity-scale", type=int, default=1, help="Scale for amplifying disparity color mapping. Default: 1."
    )
    parser.add_argument(
        '--video-to-jpg',
        action='store_true',
        help="Use this flag to convert video .bin files to a series of jpg images. Default is mp4.",
    )
    args = parser.parse_args()

    # main(args.file_name, args.output_path, args.camera_name, args.view_name, args.disparity_scale, args.video_to_jpg)

if __name__ == "__main__":
    container = DIContainer.get_container()
    container[CameraParser].parse(Path("/home/lincoln/Documents/amiga_test/test_bin.bin"), Path("/home/lincoln/Documents/amiga_test/output/"), "oak0", "rgb", 1, True)