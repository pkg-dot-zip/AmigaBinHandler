from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from farm_ng.core.events_file_reader import build_events_dict
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.oak import oak_pb2
from tqdm import tqdm

from logger.ILogger import ILogger


class CameraParser:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def parse(
            self, file_name: Path, output_path: Path, camera_name: str, view_name: str, disparity_scale: int,
            video_to_jpg: bool
    ) -> None:
        """Read an events file and convert it to a video.

        Args:

            file_name (Path): The path to the events file.
            output_path (Path): The path to the folder where the converted data will be written.
            camera_name (str): The name of the camera to visualize.
            view_name (str): The name of the view to visualize.
            disparity_scale (int, optional): The scale to apply to the disparity image. Defaults to 1.
            video_to_jpg (bool, optional): Whether to convert the video to jpgs. Defaults to False.
        """
        # create the file reader
        reader = EventsFileReader(file_name)
        success: bool = reader.open()
        if not success:
            raise RuntimeError(f"Failed to open events file: {file_name}")

        # get the index of the events file
        events_index: list[EventLogPosition] = reader.get_index()

        # structure the index as a dictionary of lists of events
        events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)

        self.logger.info(f"All available topics: {sorted(events_dict.keys())}")

        # customize camera and view
        topic_name = f"/{camera_name}/{view_name}"
        if topic_name not in events_dict:
            raise RuntimeError(f"Camera view not found: {topic_name}")

        camera_events: list[EventLogPosition] = events_dict[topic_name]

        cv2.namedWindow(topic_name, cv2.WINDOW_NORMAL)

        # create a video writer to write the video
        video_writer: cv2.VideoWriter | None = None

        event_log: EventLogPosition
        for event_log in tqdm(camera_events):
            # parse the message
            sample: oak_pb2.OakFrame = event_log.read_message()

            # decode image
            img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)
            if view_name == "disparity":
                disparity_scale: int = max(1, int(disparity_scale))
                img = cv2.applyColorMap(img * disparity_scale, cv2.COLORMAP_JET)

            # show image
            cv2.imshow(topic_name, img)

            if not video_to_jpg:
                # create the video writer if it doesn't exist
                if video_writer is None:
                    height, width, _ = img.shape
                    file_path = file_name.parent if not output_path else output_path.absolute()
                    video_name = file_path / (file_name.stem + f".{view_name}.mp4")
                    video_writer = cv2.VideoWriter(str(video_name), cv2.VideoWriter_fourcc(*'mp4v'), 10,
                                                   (width, height))

                # write the frame to the video
                video_writer.write(img)
            else:
                # write frame to jpg
                file_path = file_name.parent if not output_path else output_path.absolute()
                file_path = file_path / file_name.stem / f"{view_name}"
                frame_name: str = f"frame_{sample.meta.sequence_num:06d}.jpg"
                if not file_path.exists():
                    file_path.mkdir(parents=True, exist_ok=True)

                # write the frame to the path
                cv2.imwrite(str(file_path / frame_name), img)

            cv2.waitKey(1)

        # close the video writer and the file reader
        if video_writer is not None:
            video_writer.release()
        reader.close()
