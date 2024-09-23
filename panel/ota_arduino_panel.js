class OtaArduinoPanel extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
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
          <button id="compileFirmware">Compile</button>
  
          <h2>Logs</h2>
          <div id="logOutput"></div>
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
        if (sketchFile) {
          this.compileFirmware(sketchFile);
        }
      });
    }
  
    async uploadFirmware(firmwareFile) {
      // Upload firmware logic
      const formData = new FormData();
      formData.append('firmware', firmwareFile);
      const response = await fetch('/api/ota_arduino/upload_firmware', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      this.shadowRoot.querySelector('#logOutput').innerText = result.message;
    }
  
    async compileFirmware(sketchFile) {
      // Compile firmware logic
      const response = await fetch('/api/ota_arduino/compile_firmware', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sketch_file: sketchFile })
      });
      const result = await response.json();
      this.shadowRoot.querySelector('#logOutput').innerText = result.message;
    }
  }
  
  customElements.define('ota-arduino-panel', OtaArduinoPanel);
  