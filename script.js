const { ipcRenderer } = require('electron');
const videoPlayer = document.getElementById('videoPlayer');

function openVideo() {
  ipcRenderer.send('open-file-dialog');
}

ipcRenderer.on('selected-file', (event, filePath) => {
  console.log(filePath);
  videoPlayer.src = filePath;
  videoPlayer.play();
});

// // console.log(videoPlayer.src);

// var str = String(videoPlayer.src)

// var h1 = document.getElementById("source_file_contents_h1");
// console.log(str);
// h1.textContent = str;

let path;

ipcRenderer.on('selected-file', (event, filePath) => {
  console.log(filePath);
  // Send the selected video file path to Python
  ipcRenderer.send('set-video-source', filePath);
});

document.getElementById('generateLogsButton').addEventListener('click', () => {
  // Send a message to the main process to run the Python script
  ipcRenderer.send('generate-logs');
});
