document.addEventListener("DOMContentLoaded", function() {
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("firmware-file-input");
    const logsOutput = document.getElementById("logs-output");

    uploadBtn.addEventListener("click", function() {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a firmware file");
            return;
        }

        // Call the Home Assistant service to upload firmware
        uploadFirmware(file);
    });

    function uploadFirmware(file) {
        const formData = new FormData();
        formData.append("firmware", file);

        // Sending firmware to Home Assistant service
        fetch("/api/ota_arduino/upload_firmware", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            logsOutput.value += "\n" + data.message;
        })
        .catch(error => {
            logsOutput.value += "\nError uploading firmware: " + error;
        });
    }
});
