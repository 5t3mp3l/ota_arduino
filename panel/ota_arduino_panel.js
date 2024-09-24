class OtaArduinoPanel extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
    }
  
    connectedCallback() {
      this.render();
      this.fetchBoardList();  // Fetch available boards dynamically
    }
  
    render() {
      this.shadowRoot.innerHTML = `
        <style>
          /* Add your CSS here for styling the panel */
        </style>
        <div class="container">
          <h1>OTA Arduino Panel</h1>
          
          <h2>Select Board</h2>
          <select id="boardList"></select>
  
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
        const selectedBoard = this.shadowRoot.querySelector('#boardList').value;
        if (firmwareFile && selectedBoard) {
          this.uploadFirmware(firmwareFile, selectedBoard);
        }
      });
  
      this.shadowRoot.querySelector('#compileFirmware').addEventListener('click', () => {
        const sketchFile = this.shadowRoot.querySelector('#sketchFile').value;
        const selectedBoard = this.shadowRoot.querySelector('#boardList').value;
        if (sketchFile && selectedBoard) {
          this.compileFirmware(sketchFile, selectedBoard);
        }
      });
    }
  
    async fetchBoardList() {
      // Fetch the available boards dynamically via Arduino CLI
      const response = await fetch('/api/ota_arduino/boards');
      const boards = await response.json();
      const boardList = this.shadowRoot.querySelector('#boardList');
      boards.forEach(board => {
        const option = document.createElement('option');
        option.value = board;
        option.text = board;
        boardList.appendChild(option);
      });
    }
  
    async uploadFirmware(firmwareFile, board) {
      // Upload firmware logic
      const formData = new FormData();
      formData.append('firmware', firmwareFile);
      formData.append('board', board);
      const response = await fetch('/api/ota_arduino/upload_firmware', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      this.shadowRoot.querySelector('#logOutput').innerText = result.message;
    }
  
    async compileFirmware(sketchFile, board) {
      // Compile firmware logic
      const response = await fetch('/api/ota_arduino/compile_firmware', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sketch_file: sketchFile, board: board })
      });
      const result = await response.json();
      this.shadowRoot.querySelector('#logOutput').innerText = result.message;
    }
    async fetchLogs() {
        // Fetch and display logs
        const response = await fetch('/api/ota_arduino/logs');
        const result = await response.json();
        this.shadowRoot.querySelector('#logOutput').innerText = result.logs;
      }
      
  }
  
  customElements.define('ota-arduino-panel', OtaArduinoPanel);
  // Call fetchLogs regularly to update logs dynamically
  setInterval(() => this.fetchLogs(), 3000);