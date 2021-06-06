const { app: ElectronApp, BrowserWindow, dialog, Menu, ipcMain } = require('electron');
const path = require('path');
const { writeFile } = require('fs');

class MainProcessCore {
    buildGUI() {
        this.mainWindow = this.createWindow('Architecture Editor', 800, 600);

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
            const json = JSON.stringify(data, null, 4);

            writeFile(filePath, json, () => dialog.showMessageBox({
                message: 'Save complete'
            }));
        });
    }

    saveArchitecture() {
        const getData = async (saveInfo) => {
            if (saveInfo && !saveInfo['canceled']) {
                this.mainWindow.webContents.send('save-architecture', { filePath: saveInfo.filePath});
            }
        };

        dialog.showSaveDialog({
            filters: [
                { name: 'json', 'extensions': ['json'] }
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