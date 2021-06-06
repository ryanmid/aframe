const { app: ElectronApp, BrowserWindow, dialog, Menu, ipcMain } = require('electron');
const path = require('path');
const { readFile, writeFile } = require('fs');

class MainProcessCore {
    buildGUI() {
        this.mainWindow = this.createWindow('Architecture Editor', 800, 600);
        this.mainWindow.maximize();

        this.mainMenu = this.createMainMenu();
        Menu.setApplicationMenu(this.mainMenu);

        this.createEventListeners();
    }

    createWindow(title, width, height) {
        return new BrowserWindow({
            title: title,
            width: width,
            height: height,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
                enableRemoteModule: true
            }
        });
    }

    createMainMenu() {
        return Menu.buildFromTemplate([
            {
                label: 'File',
                submenu: [
                    {
                        label: 'New Architecture',
                        click: () => this.newArchitecture()
                    },
                    {
                        label: 'Load Architecture',
                        click: () => this.loadArchitecture()
                    },
                    {
                        label: 'Save Architecture',
                        click: () => this.saveArchitecture()
                    },
                    {
                        label: 'Open Dev Tools',
                        click: () => this.mainWindow.webContents.openDevTools()
                    },
                    {
                        label: 'Exit',
                        click: () => this.quit()
                    }
                ]
            }
        ]);
    }

    createEventListeners() {
        ipcMain.on('save-architecture', (event, args) => {
            const { filePath, data } = args;
            const json = JSON.stringify(data, null, 2);

            writeFile(filePath, json, () => dialog.showMessageBox({
                message: 'Save complete'
            }));
        });
    }

    newArchitecture() {
        this.mainWindow.webContents.send('new-architecture', {});
    }

    loadArchitecture() {
        const sendData = async (loadInfo) => {
            if (loadInfo && !loadInfo['canceled']) {
                const { filePaths } = loadInfo;
                readFile(filePaths[0], 'utf-8', (err, data) => {
                    const json = JSON.parse(data);
                    this.mainWindow.webContents.send('load-architecture', { data: json });
                });
            }
        };

        dialog.showOpenDialog({
            properties: [ "openFile", "dontAddToRecent" ],
            filters: [
                { name: 'json', extensions: ['json'] }
            ]
        }).then(sendData);
    }

    saveArchitecture() {
        const getData = async (saveInfo) => {
            if (saveInfo && !saveInfo['canceled']) {
                this.mainWindow.webContents.send('save-architecture', { filePath: saveInfo.filePath});
            }
        };

        dialog.showSaveDialog({
            filters: [
                { name: 'json', extensions: ['json'] }
            ]
        }).then(getData);
    }

    startRenderProcess(entryPointFilename) {
        this.mainWindow.loadFile(path.join(__dirname, entryPointFilename));
    }

    quit() {
        ElectronApp.quit();
    }
}

module.exports = {
    MainProcessCore
};