// This file will automatically be loaded by webpack and run in the "renderer" context

import * as React from "react";
import * as ReactDOM from "react-dom";
import {IpcRendererEvent} from "electron";
import App from './components/App';

(() => {
    const electron = window.require('electron');
    const ipcRenderer = electron.ipcRenderer;

    function render(): void {
        ReactDOM.render(
            React.createElement(App, null, null),
            document.getElementById('root')
        );
    }

    function createEventListeners(): void {

        addEventListener('save-architecture', (event, args) => {
            // args['data'] = editor.serialize();
            // event.sender.send('save-architecture', args);
            console.log('Saving architecture...');
        });

        addEventListener('load-architecture', (event, args) => {
            // editor = composeEditor(data);
            console.log('Loading architecture...');
        });

        addEventListener('new-architecture', (event, args) => {
            // editor = composeEditor();
            console.log('Creating new architecture...');
        });

        addEventListener('redraw', (event, args) => {
            console.log('redrawing...');
            render();
        });
    }

    function addEventListener(name: string, eventHandler: (event: IpcRendererEvent, args: Event) => void): void {
        ipcRenderer.on(name, eventHandler);
    }

    createEventListeners();
    render();

})();
