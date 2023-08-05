from typing import Optional

from abc import ABCMeta, abstractmethod
from twisted.internet.defer import Deferred


class DeviceApiABC(metaclass=ABCMeta):
    """ Device API

    This is the public API for the part of the plugin that runs on the server service.

    """

    @abstractmethod
    def deviceDescription(self, deviceToken: str) -> Deferred:
        """ Device Description

        Retrieve the devices description

        :param deviceToken: The token for the device to retrieve the description for
        :return: A Deferred that will fire with :code:`Optional[str]`

        """


    @abstractmethod
    def deviceDescriptionBlocking(self, deviceToken: str) -> Optional[str]:
        """ Device Description

        Retrieve the devices description, this must be called from a thread.

        :param deviceToken: The token for the device to retrieve the description for
        :return: The device description or None

        """