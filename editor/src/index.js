import { LiteGraph, LGraph, LGraphCanvas } from 'litegraph.js';
import 'litegraph.js/css/litegraph.css';

class Component {
    constructor() {
        this.title = "Component";
        this.horizontal = true;
        this.resizable = true;

        this.addInput("input","connector");
        this.addOutput("output","component");
    }

    onExecute() {
    }
}

class Connector {
    constructor() {
        this.title = "Connector";
        this.horizontal = true;
        this.resizable = true;

        this.addInput("input","component");
        this.addOutput("output","connector");

        this.size = [1000, 25];
    }

    onDblClick() {
        let size = this.size;
        this.addInput("input" + (this.inputs.length + 1), "component");
        this.size = size;
    }
}

class App {
    constructor(divContainer) {
        this.graph = new LGraph();
        this.canvas = new LGraphCanvas(divContainer, this.graph);
        this.nodes = [];

        LiteGraph.registerNodeType('arch/component', Component);
        LiteGraph.registerNodeType('arch/connector', Connector);
    }

    addNode(nodeType, xpos, ypos) {
        let node = LiteGraph.createNode(nodeType);
        node.pos = [xpos, ypos];

        this.graph.add(node);
        this.nodes.push(node)
    }

    connectNodes(nodeA, nodeB) {
        nodeA.connect(0, nodeB, 0);
    }

    run() {
        this.graph.start()
    }
}

let editor = new App('#editorContainer');
editor.run();

editor.addNode('arch/connector', 50, 100);
editor.addNode('arch/component', 300, 250);
editor.addNode('arch/component', 500, 250);
editor.addNode('arch/component', 700, 250);
editor.addNode('arch/connector', 50, 400);
