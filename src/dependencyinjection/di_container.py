from typing import List, Optional

from lagom import Container, Singleton

from amiga.camera.camera_parser import CameraParser
from amiga.camera.export.CameraExportRetriever import CameraExportRetriever
from logger.ILogger import ILogger
from logger.Logger import Logger
from parser.CameraArgParser import CameraArgParser
from parser.IArgParser import IArgParser
from util.mpo_merger import MPOMerger

class DIContainer:
    container: Optional[Container] = None

    @staticmethod
    def get_container() -> Container:
        if DIContainer.container is None:
            DIContainer.container = Container()
            DIContainer.container[ILogger] = Singleton(Logger)
            DIContainer.container[CameraParser] = Singleton(CameraParser)
            DIContainer.container[MPOMerger] = Singleton(MPOMerger)
            DIContainer.container[CameraExportRetriever] = Singleton(CameraExportRetriever)

            # All ArgParsers.
            DIContainer.container[CameraArgParser] = Singleton(CameraArgParser)
            DIContainer.container[List[IArgParser]] = [
                DIContainer.container[CameraArgParser],
            ]

        return DIContainer.container