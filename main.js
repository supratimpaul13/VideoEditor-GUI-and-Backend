const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const url = require('url');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // This may not be needed depending on your Electron version
    },
  });

  mainWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, 'index.html'),
      protocol: 'file:',
      slashes: true,
    })
  );

  mainWindow.on('closed', () => {
    mainWindow = null;
  });



  // to give the script file directory
  ipcMain.on('set-video-source', (event, filePath) => {
    // Pass the video file path to your Python script using Python's command-line arguments
    const { spawn } = require('child_process');
    const pythonProcess = spawn('python', ['C:/Tech Variable/Wireframe/Engine/test.py', filePath]);

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python stderr: ${data}`);
    });
  });

  // to generate logs
  ipcMain.on('generate-logs', (event) => {
    // Run your Python script when the 'generate-logs' message is received
    const { spawn } = require('child_process');
    const pythonProcess = spawn('python', ['C:/Tech Variable/Wireframe/Engine/test.py']);

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python stderr: ${data}`);
    });
  });


}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

ipcMain.on('open-file-dialog', (event) => {
  const { dialog } = require('electron');

  dialog
    .showOpenDialog(mainWindow, {
      properties: ['openFile'],
      filters: [
        { name: 'Videos', extensions: ['mp4', 'mkv', 'avi'] },
        { name: 'All Files', extensions: ['*'] },
      ],
    })
    .then((result) => {
      if (!result.canceled && result.filePaths.length > 0) {
        event.sender.send('selected-file', result.filePaths[0]);
      }
    })
    .catch((err) => {
      console.log(err);
    });
});
