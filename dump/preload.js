const { ipcRenderer } = require('electron');

window.openVideo = () => {
  ipcRenderer.send('open-file-dialog');
};

ipcRenderer.on('selected-file', (event, filePath) => {
  const videoPlayer = document.getElementById('videoPlayer');
  videoPlayer.src = filePath;
  videoPlayer.play();
});
