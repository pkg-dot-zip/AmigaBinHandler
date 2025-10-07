from __future__ import annotations

from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from farm_ng.core.events_file_reader import build_events_dict
from farm_ng.core.events_file_reader import EventLogPosition
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.oak import oak_pb2
from tqdm import tqdm

from amiga.camera.ECamera import ECamera
from amiga.camera.EView import EView
from logger.ILogger import ILogger


class CameraParser:
    def __init__(self, logger: ILogger):
        self.logger = logger
        self.video_writer: Optional[cv2.VideoWriter] = None

    def __close_video_writer(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

    def parse(
            self, file_name: Path, output_path: Path, camera: ECamera = ECamera.OAK0, view: EView = EView.RGB, disparity_scale: int = 1,
            video_to_jpg: bool = True
    ) -> None:
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
        topic_name = f"/{camera}/{view}"
        if topic_name not in events_dict:
            raise RuntimeError(f"Camera view not found: {topic_name}")

        camera_events: list[EventLogPosition] = events_dict[topic_name]

        event_log: EventLogPosition
        for event_log in tqdm(camera_events):
            self.__write_frame(
                file_name=file_name,
                output_path=output_path,
                event_log=event_log,
                view=view,
                disparity_scale=disparity_scale,
                video_to_jpg=video_to_jpg,
            )

        # close the video writer and the file reader__write
        self.__close_video_writer()
        reader.close()

    def __write_frame(self, file_name: Path, output_path: Path, event_log: EventLogPosition, view: EView, disparity_scale: int, video_to_jpg: bool) -> None:
        # parse the message
        sample: oak_pb2.OakFrame = event_log.read_message()

        # decode image
        img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)
        if view == EView.DISPARITY:
            disparity_scale: int = max(1, int(disparity_scale))
            img = cv2.applyColorMap(img * disparity_scale, cv2.COLORMAP_JET)

        # Write to jpg or video dependent on bool value.
        if not video_to_jpg:
            self.__write_frame_to_video(
                file_name=file_name,
                output_path=output_path,
                view=view,
                img=img,
            )
        else:
            self.__write_frame_to_jpg(
                sample=sample,
                img=img,
                file_name=file_name,
                output_path=output_path,
                view=view,
            )


    def __write_frame_to_video(self, file_name: Path, output_path: Path, view: EView, img):
        # create the video writer if it doesn't exist
        if self.video_writer is None:
            height, width, _ = img.shape
            file_path = file_name.parent if not output_path else output_path.absolute()
            video_name = file_path / (file_name.stem + f".{view}.mp4")
            self.video_writer = cv2.VideoWriter(str(video_name), cv2.VideoWriter_fourcc(*'mp4v'), 10,
                                           (width, height))

        # write the frame to the video
        self.video_writer.write(img)

    def __write_frame_to_jpg(self, sample: oak_pb2.OakFrame, img, file_name: Path, output_path: Path, view: EView):
        # write frame to jpg
        file_path = file_name.parent if not output_path else output_path.absolute()
        file_path = file_path / file_name.stem / f"{view}"
        if not file_path.exists():
            file_path.mkdir(parents=True, exist_ok=True)

        # write the frame to the path
        frame_name: str = f"frame_{sample.meta.sequence_num:06d}.jpg"
        cv2.imwrite(str(file_path / frame_name), img)
