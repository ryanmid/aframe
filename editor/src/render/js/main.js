const { ipcRenderer } = require('electron');
const { LiteGraph, LGraph, LGraphCanvas } = require('litegraph.js');

class Component {
    constructor() {
        this.title = "Component";
        this.resizable = true;

        this.addInput("input","connector");
        this.addOutput("output","component");
    }
}

class Connector {
    constructor() {
        this.title = "Connector";
        this.resizable = true;

        this.addInput("bridge", "connector");
        this.addInput("input","component");
        this.addOutput("output","connector");

        this.size = [125, 500];
    }

    newInput(name = "input" + (this.inputs.length)) {
        let size = this.size;
        this.addInput(name, "component");
        this.size = size;
    }

    onDblClick() {
        this.newInput()

        // Return true to stop event propagation
        return true;
    }
}

class App {
    constructor(divContainer, architecture = null) {
        this.graph = new LGraph(architecture);
        this.canvas = new LGraphCanvas('#' + divContainer, this.graph);
        this.nodes = [];

        LiteGraph.NODE_TEXT_COLOR = '#000000';
        LiteGraph.NODE_DEFAULT_COLOR = '#252525';
        LiteGraph.NODE_DEFAULT_BGCOLOR = '#f0f0f0';
    }

    addNode(nodeType, xpos, ypos) {
        let node = LiteGraph.createNode(nodeType);
        node.pos = [xpos, ypos];

        this.graph.add(node);
        this.nodes.push(node)
    }

    connectNodes(nodeA, nodeB, portNumber=1) {
        nodeA.connect(0, nodeB, portNumber);
    }

    serialize() {
        return this.graph.serialize();
    }

    run() {
        this.graph.start();
    }
}

function composeEditor(architecture=null) {
    let canvasId = 'editorContainer';
    let app = new App(canvasId, architecture);

    resizeEditorElements();

    return app;
}

function resizeEditorElements() {
    let screenWidth = document.body.clientWidth - 20;
    let screenHeight = document.body.clientHeight - 20;

    let canvasId = 'editorContainer';
    let canvas = document.getElementById(canvasId);

    canvas.width = screenWidth;
    canvas.height = screenHeight;
}

let editor = null;
document.addEventListener('DOMContentLoaded', () => {

    LiteGraph.registerNodeType('arch/component', Component);
    LiteGraph.registerNodeType('arch/connector', Connector);

    editor = composeEditor();
    editor.run();

    window.onresize = resizeEditorElements;
});

ipcRenderer.on('save-architecture', (event, args) => {
    args['data'] = editor.serialize();
    event.sender.send('save-architecture', args);
});

ipcRenderer.on('load-architecture', (event, args) => {
    const { data } = args;
    editor = composeEditor(data);
});

ipcRenderer.on('new-architecture', (event, args) => {
    editor = composeEditor();
});