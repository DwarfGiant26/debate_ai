export class Backend {
    private _backendUrl: string;

    constructor(backendUrl: string) {
        this._backendUrl = backendUrl;
    }

    async startDebate()  {
        await fetch(this._backendUrl + "/startDebate");
    }
}

export {}
