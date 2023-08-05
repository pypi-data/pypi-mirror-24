import {Component, OnInit} from "@angular/core";
import {TitleService} from "@synerty/peek-util";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";

import {
    DeviceNavService,
    DeviceServerService,
    DeviceTupleService,
    EnrolDeviceAction,
    ServerInfoTuple
} from "@peek/peek_core_device/_private";

import {DeviceInfoTuple} from "@peek/peek_core_device";
import {DeviceTypeEnum} from "@peek/peek_core_device/_private/hardware-info/hardware-info.abstract";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";


@Component({
    selector: 'core-device-enroll',
    templateUrl: 'connect.component.web.html',
    moduleId: module.id
})
export class ConnectComponent extends ComponentLifecycleEventEmitter implements OnInit {

    server: ServerInfoTuple | null = null;

    httpPortStr: string = '8000';
    websocketPortStr: string = '8001';

    deviceType: DeviceTypeEnum;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private titleService: TitleService,
                private tupleService: DeviceTupleService,
                private nav: DeviceNavService,
                private deviceServerService: DeviceServerService) {
        super();

        this.deviceType = this.tupleService.hardwareInfo.deviceType();
        this.server = new ServerInfoTuple();

        // Make sure we're not on this page when things are fine.
        this.doCheckEvent
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this._checkNav());

    }

    ngOnInit() {
        //
        switch (this.deviceType) {
            case DeviceTypeEnum.MOBILE_WEB:
            case DeviceTypeEnum.DESKTOP_WEB:
                // If this is a web service, always use the host from the URL
                this.server.host = location.host.split(':')[0];
                this.server.useSsl = location.protocol.toLowerCase() == "https";

                if (location.host.split(':').length > 1) {
                    this.server.httpPort = parseInt(location.host.split(':')[1]);
                } else {
                    this.server.httpPort = this.server.useSsl ? 443 : 80;
                }

                this.httpPortStr = this.server.httpPort.toString();
                break;

            default:
                break;
        }

    }

    private _checkNav() {
        if (this.deviceServerService.isConnected)
            this.nav.toHome();
        else if (this.deviceServerService.isSetup)
            this.nav.toConnecting()
    }

    connectEnabled(): boolean {

        if (this.server != null) {
            if (this.server.host == null || !this.server.host.length)
                return false;

            if (!parseInt(this.websocketPortStr))
                return false;

            if (!parseInt(this.httpPortStr))
                return false;

        }
        return true;
    }

    connectClicked() {
        try {
            this.server.httpPort = parseInt(this.httpPortStr);
            this.server.websocketPort = parseInt(this.websocketPortStr);

        } catch (e) {
            this.balloonMsg.showError("Port numbers must be integers.");
            return;
        }

        this.deviceServerService.setServer(this.server)
            .then(() => this.nav.toConnecting());


    }


}