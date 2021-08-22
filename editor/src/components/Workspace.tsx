import React, {useState} from "react";
import ReactFlow, {addEdge, Background, BackgroundVariant, Controls, Edge, MiniMap, Node, removeElements} from "react-flow-renderer";
import WorkspaceBackground from "./WorkspaceBackground";
import {Phase} from "./Phase";
import initialElements from "./initial_elements";
import CSS from 'csstype';
import {Task} from "./Task";

const workspaceStyle: CSS.Properties = {
  background: 'rgb(75,75,75)',
};

const onLoad = (reactFlowInstance: any) => {
    console.log('flow loaded:', reactFlowInstance);
    reactFlowInstance.fitView();
};

const nodeTypes = {
    phase: Phase,
    task: Task
}

const Workspace = () => {
    const [elements, setElements] = useState(initialElements);
    const onElementsRemove = (elementsToRemove: []) =>
        setElements((els) => removeElements(elementsToRemove, els));
    const onConnect = (params: Edge<any>) => setElements((els) => addEdge(params, els));

    return (
        <ReactFlow
            elements={elements}
            onElementsRemove={onElementsRemove}
            onConnect={onConnect}
            onLoad={onLoad}
            style={workspaceStyle}
            nodeTypes={nodeTypes}
        >
            <WorkspaceBackground/>
            <MiniMap
                nodeStrokeColor={(n: Node): string => {
                    return '#000';
                }}
                nodeColor={(n): string => {
                    return '#0000ff50';
                }}
                nodeBorderRadius={2}
            />
            <Controls />
        </ReactFlow>
    );
};

export default Workspace;
