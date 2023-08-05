import logging
from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from peek_core_device._private.server.controller.ObservableNotifier import ObservableNotifier
from peek_core_device._private.storage.DeviceInfoTuple import DeviceInfoTuple
from peek_core_device._private.storage.Setting import globalSetting, AUTO_ENROLLMENT
from peek_core_device._private.tuples.EnrolDeviceAction import EnrolDeviceAction
from peek_core_device._private.tuples.UpdateEnrollmentAction import UpdateEnrollmentAction
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Tuple import Tuple
from vortex.TupleAction import TupleActionABC
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

logger = logging.getLogger(__name__)


class EnrollmentController:
    def __init__(self, dbSessionCreator, tupleObservable: TupleDataObservableHandler):
        self._dbSessionCreator = dbSessionCreator
        self._tupleObservable = tupleObservable

    def shutdown(self):
        pass

    def processTupleAction(self, tupleAction: TupleActionABC) -> List[Tuple]:

        if isinstance(tupleAction, EnrolDeviceAction):
            return self._processDeviceEnrolment(tupleAction)

        if isinstance(tupleAction, UpdateEnrollmentAction):
            return self._processAdminUpdateEnrolment(tupleAction)


    @deferToThreadWrapWithLogger(logger)
    def _processDeviceEnrolment(self, action: EnrolDeviceAction) -> List[Tuple]:
        """ Process Device Enrolment

        :rtype: Deferred
        """
        ormSession = self._dbSessionCreator()
        try:
            deviceInfo = DeviceInfoTuple()
            deviceInfo.description = action.description
            deviceInfo.deviceId = action.deviceId
            deviceInfo.deviceType = action.deviceType
            deviceInfo.deviceToken = str(uuid4())
            deviceInfo.createdDate = datetime.utcnow()
            deviceInfo.appVersion = '0.0.0'
            deviceInfo.isEnrolled = globalSetting(ormSession, AUTO_ENROLLMENT)

            # TODO, Move these to their own tuple
            deviceInfo.lastOnline = datetime.utcnow()
            deviceInfo.isOnline = True

            ormSession.add(deviceInfo)
            ormSession.commit()

            ObservableNotifier.notifyDeviceInfo(deviceId=deviceInfo.deviceId,
                                                tupleObservable=self._tupleObservable)

            ormSession.refresh(deviceInfo)
            ormSession.expunge_all()
            return [deviceInfo]

        except IntegrityError as e:
            if "DeviceInfo_deviceId_key" in str(e):
                raise Exception("A device with that identifier already exists")

            if "DeviceInfo_description_key" in str(e):
                raise Exception("A device with that description already exists")

        finally:
            # Always close the session after we create it
            ormSession.close()

    @deferToThreadWrapWithLogger(logger)
    def _processAdminUpdateEnrolment(self, action: UpdateEnrollmentAction) -> List[Tuple]:
        """ Process Admin Update

        :rtype: Deferred
        """
        session = self._dbSessionCreator()
        try:
            deviceInfo = (
                session.query(DeviceInfoTuple)
                    .filter(DeviceInfoTuple.id == action.deviceInfoId)
                    .one()
            )

            deviceId = deviceInfo.deviceId

            if action.remove:
                session.delete(deviceInfo)
            else:
                deviceInfo.isEnrolled = not action.unenroll

            session.commit()

            ObservableNotifier.notifyDeviceInfo(deviceId=deviceId,
                                                tupleObservable=self._tupleObservable)

            return []

        finally:
            # Always close the session after we create it
            session.close()
