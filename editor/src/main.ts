import {app as ElectronApp, BrowserWindow, ipcMain, Menu} from "electron";

// These "magic variable" are set by webpack according to the @electron-forge/plugin-webpack entrypoints declared
// in the project package.json
declare const MAIN_WINDOW_WEBPACK_ENTRY: string;
declare const SPLASH_WEBPACK_ENTRY: string;

(() => {
    const DEFAULT_APP_NAME: string = 'AFrame Architecture Editor';
    const DEFAULT_APP_RES: [number, number] = [800, 600];

    let splashWindow: BrowserWindow = null;
    let appWindow: BrowserWindow = null;
    let appMenu: Menu = null;

    function launchSplashWindow(): void {
        splashWindow = new BrowserWindow({
            width: 400,
            height: 600,
            titleBarStyle: 'hidden',
            frame: false,
            alwaysOnTop: false,
            show: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
                enableRemoteModule: true
            }
        });
        splashWindow.on('ready-to-show', splashWindow.show);
        splashWindow.loadURL(SPLASH_WEBPACK_ENTRY);
    }

    function launchAppWindow(): void {
        appWindow = new BrowserWindow({
            title: DEFAULT_APP_NAME,
            width: DEFAULT_APP_RES[0],
            height: DEFAULT_APP_RES[1],
            show: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
                enableRemoteModule: true
            }
        });

        // Once the app window is ready then close the splash screen and show the app window
        appWindow.once('ready-to-show', () => {
            splashWindow.destroy();
            appWindow.maximize();
            appWindow.show();
        });

        // Redraw the app window when it is resized
        appWindow.on('resize', () => {
            ipcMain.emit('redraw');
        });

        // Build the window menu
        appMenu = Menu.buildFromTemplate([
            {
                label: 'File',
                submenu: [
                    {
                        label: 'New Architecture',
                        click: () => null //newArchitecture()
                    },
                    {
                        label: 'Load Architecture',
                        click: () => null //loadArchitecture()
                    },
                    {
                        label: 'Save Architecture',
                        click: () => null //saveArchitecture()
                    },
                    {
                        label: 'Open Dev Tools',
                        click: () => appWindow.webContents.openDevTools()
                    },
                    {
                        label: 'Exit',
                        click: () => ElectronApp.quit()
                    }
                ]
            }
        ]);
        Menu.setApplicationMenu(appMenu);

        // Load app index file into the window
        appWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);
    }

    // Handle creating/removing shortcuts on Windows when installing/uninstalling
    if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
        ElectronApp.quit();
    }

    // Called when Electron has finished initialization and is ready to create browser windows
    ElectronApp.on('ready', () => {
        launchSplashWindow();
        launchAppWindow();
    });

    ElectronApp.on('activate', () => {
        // On macOS it's common to re-create a window in the app when the dock icon is clicked with no other windows open
        if (process.platform === 'darwin' && BrowserWindow.getAllWindows().length === 0) {
            launchAppWindow();
        }
    });

    // Quit when all windows are closed, except on macOS where users must explicitly quit the process
    ElectronApp.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            ElectronApp.quit();
        }
    });

})();
