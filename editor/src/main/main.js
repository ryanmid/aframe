const { app: ElectronApp, BrowserWindow } = require('electron');
const { MainProcessCore } = require('./core.js');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
  ElectronApp.quit();
}

const core = new MainProcessCore();

ElectronApp.on('ready', () => {
  core.buildGUI();
  core.startRenderProcess('../render/index.html');
});

ElectronApp.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    core.buildGUI();
    core.startRenderProcess('../render/index.html');
  }
});

ElectronApp.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    core.quit();
  }
});
