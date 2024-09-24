class OtaArduinoPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.logInterval = null;
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                /* Add your CSS here for styling the panel */
            </style>
            <div class="container">
                <h1>OTA Arduino Panel</h1>

                <h2>Upload Firmware</h2>
                <input type="file" id="firmwareFile" />
                <button id="uploadFirmware">Upload</button>

                <h2>Compile Firmware</h2>
                <input type="text" id="sketchFile" placeholder="Enter Sketch File Path" />
                <input type="text" id="board" placeholder="Enter Board (e.g., arduino:avr:uno)" />
                <button id="compileFirmware">Compile</button>

                <h2>Logs</h2>
                <div id="logOutput"></div>
                <button id="startLogs">Start Log Stream</button>
                <button id="stopLogs">Stop Log Stream</button>
            </div>
        `;

        this.shadowRoot.querySelector('#uploadFirmware').addEventListener('click', () => {
            const firmwareFile = this.shadowRoot.querySelector('#firmwareFile').files[0];
            if (firmwareFile) {
                this.uploadFirmware(firmwareFile);
            }
        });

        this.shadowRoot.querySelector('#compileFirmware').addEventListener('click', () => {
            const sketchFile = this.shadowRoot.querySelector('#sketchFile').value;
            const board = this.shadowRoot.querySelector('#board').value;
            if (sketchFile && board) {
                this.compileFirmware(sketchFile, board);
            }
        });

        this.shadowRoot.querySelector('#startLogs').addEventListener('click', () => {
            this.startFetchingLogs();
        });

        this.shadowRoot.querySelector('#stopLogs').addEventListener('click', () => {
            this.stopFetchingLogs();
        });
    }

    async uploadFirmware(firmwareFile) {
        const formData = new FormData();
        formData.append('firmware', firmwareFile);
        const response = await fetch('/api/ota_arduino/upload_firmware', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        this.showLogs(result.message);
    }

    async compileFirmware(sketchFile, board) {
        const response = await fetch('/api/ota_arduino/compile_firmware', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sketch_file: sketchFile, board })
        });
        const result = await response.json();
        this.showLogs(result.message);
    }

    showLogs(logs) {
        const logOutput = this.shadowRoot.querySelector('#logOutput');
        logOutput.innerText = logs;
    }

    async startFetchingLogs() {
        this.logInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/ota_arduino/logs');
                const result = await response.json();
                this.showLogs(result.logs);
            } catch (error) {
                this.showLogs(`Failed to fetch logs: ${error.message}`);
            }
        }, 3000);  // Poll every 3 seconds
    }

    stopFetchingLogs() {
        if (this.logInterval) {
            clearInterval(this.logInterval);
            this.logInterval = null;
        }
    }
}

customElements.define('ota-arduino-panel', OtaArduinoPanel);
