from lagom import Container, Singleton

from amiga.camera.camera_parser import CameraParser
from logger.ILogger import ILogger
from logger.Logger import Logger
from util.mpo_merger import MPOMerger


class DIContainer:
    @staticmethod
    def get_container() -> Container:
        container = Container()

        container[ILogger] = Singleton(Logger)
        container[CameraParser] = Singleton(CameraParser)
        container[MPOMerger] = Singleton(MPOMerger)

        return container