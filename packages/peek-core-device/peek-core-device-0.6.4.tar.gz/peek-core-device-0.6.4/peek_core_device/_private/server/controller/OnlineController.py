import logging
from typing import List

from sqlalchemy.orm.exc import NoResultFound
from twisted.internet.defer import Deferred

from peek_core_device._private.server.controller.ObservableNotifier import \
    ObservableNotifier
from peek_core_device._private.storage.DeviceInfoTuple import DeviceInfoTuple
from peek_core_device._private.tuples.UpdateDeviceOnlineAction import \
    UpdateDeviceOnlineAction
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Tuple import Tuple
from vortex.TupleAction import TupleActionABC
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

logger = logging.getLogger(__name__)


class OnlineController:
    def __init__(self, dbSessionCreator, tupleObservable: TupleDataObservableHandler):
        self._dbSessionCreator = dbSessionCreator
        self._tupleObservable = tupleObservable

        self._setAllDevicesOfflineBlocking()

    def shutdown(self):
        pass

    def processTupleAction(self, tupleAction: TupleActionABC) -> List[Tuple]:

        if isinstance(tupleAction, UpdateDeviceOnlineAction):
            return self._processUpdateOnline(tupleAction)

    @deferToThreadWrapWithLogger(logger)
    def _processUpdateOnline(self, action: UpdateDeviceOnlineAction) -> List[Tuple]:
        """ Process Online Status Update

        :rtype: Deferred
        """
        session = self._dbSessionCreator()
        try:
            deviceInfo = (
                session.query(DeviceInfoTuple)
                    .filter(DeviceInfoTuple.deviceId == action.deviceId)
                    .one()
            )

            deviceId = deviceInfo.deviceId

            deviceInfo.lastOnline = action.dateTime
            deviceInfo.isOnline = action.isOnline

            session.commit()

            ObservableNotifier.notifyDeviceInfo(deviceId=deviceId,
                                                tupleObservable=self._tupleObservable)

            return []

        except NoResultFound:
            return []

        finally:
            session.close()

    def _setAllDevicesOfflineBlocking(self):
        """ Set All Devices to Offline

        """
        session = self._dbSessionCreator()
        try:
            session.execute(DeviceInfoTuple.__table__.update().values(isOnline=False))
            session.commit()

        finally:
            session.close()
