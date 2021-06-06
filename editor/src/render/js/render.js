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
    constructor(divContainer) {
        this.graph = new LGraph();
        this.canvas = new LGraphCanvas('#' + divContainer, this.graph);
        this.nodes = [];

        LiteGraph.NODE_TEXT_COLOR = '#000000';
        LiteGraph.NODE_DEFAULT_COLOR = '#252525';
        LiteGraph.NODE_DEFAULT_BGCOLOR = '#f0f0f0';
        LiteGraph.registerNodeType('arch/component', Component);
        LiteGraph.registerNodeType('arch/connector', Connector);
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

function composeEditor() {

    let canvasId = 'editorContainer';
    let app = new App(canvasId);

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

    editor = composeEditor();
    editor.run();

    editor.addNode('arch/connector', 50, 50);
    editor.addNode('arch/component', 300, 150);
    editor.addNode('arch/component', 300,250);
    editor.addNode('arch/component', 300, 350);
    editor.addNode('arch/connector', 550, 50);

    editor.nodes[0].title = "Connector1";
    editor.nodes[1].title = "Component1";
    editor.nodes[2].title = "Component2";
    editor.nodes[3].title = "Component3";
    editor.nodes[4].title = "Connector2";

    editor.nodes[4].newInput();
    editor.nodes[4].newInput();

    editor.connectNodes(editor.nodes[0], editor.nodes[4], 0);

    editor.connectNodes(editor.nodes[0], editor.nodes[1], 0);
    editor.connectNodes(editor.nodes[0], editor.nodes[2], 0);
    editor.connectNodes(editor.nodes[0], editor.nodes[3], 0);

    editor.connectNodes(editor.nodes[1], editor.nodes[4], 1);
    editor.connectNodes(editor.nodes[2], editor.nodes[4], 2);
    editor.connectNodes(editor.nodes[3], editor.nodes[4], 3);

    window.onresize = resizeEditorElements;
});

ipcRenderer.on('save-architecture', (event, args) => {
    args['data'] = editor.serialize();
    event.sender.send('save-architecture', args);
});