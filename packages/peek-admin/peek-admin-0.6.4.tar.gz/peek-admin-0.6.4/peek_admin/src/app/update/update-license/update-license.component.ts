import {Component, OnInit} from "@angular/core";
import {
    VortexService,
    ComponentLifecycleEventEmitter,
    TupleLoader,
    Tuple,
    Payload
} from "@synerty/vortexjs";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";

@Component({
    selector: 'app-update-license',
    templateUrl: './update-license.component.html',
    styleUrls: ['./update-license.component.css']
})
export class UpdateLicenseComponent extends ComponentLifecycleEventEmitter implements OnInit {
    private readonly filt = {
        plugin: "peek_server",
        key: "admin.capabilities.data"
    };

    data: {} = {};
    private loader: TupleLoader;

    // @Output("licenced")
    // licencedOutput : EventEmitter<boolean> = new EventEmitter<boolean>();
    licenced: boolean = false;

    constructor(private vortexService: VortexService,
                private balloonMsg: Ng2BalloonMsgService) {
        super();

        vortexService.createEndpointObservable(this, this.filt)
            .subscribe(payload => this.processPayload(payload));

        // Trigger the server to send the latest data
        vortexService.sendFilt(this.filt);
    }

    ngOnInit() {
    }

    private processPayload(payload: Payload): void {
        if (payload.result) {
            if (payload.result["success"])
                this.balloonMsg.showSuccess(payload.result["message"]);
            else
                this.balloonMsg.showError(payload.result["message"]);
        }

        if (payload.tuples.length) {
            this.data = payload.tuples[0].data;
            this.licenced = !(this.data["supportExceeded"]
                                && !this.data["demoExceeded"]);
        }
    }

    updateLicense() {
        let dataWrapTuple = new Tuple('c.s.r.datawraptuple');
        dataWrapTuple["data"] = this.data["newkey"];
        this.vortexService.sendTuple(this.filt, [dataWrapTuple]);
    }
}
