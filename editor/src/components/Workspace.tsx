import React, {useState} from "react";
import ReactFlow, {addEdge, Background, BackgroundVariant, Controls, Edge, MiniMap, Node, removeElements} from "react-flow-renderer";
import WorkspaceBackground from "./WorkspaceBackground";
import initialElements from "./initial_elements";
import CSS from 'csstype';

const workspaceStyle: CSS.Properties = {
  background: 'rgb(125,125,125)',
};

const onLoad = (reactFlowInstance: any) => {
    console.log('flow loaded:', reactFlowInstance);
    reactFlowInstance.fitView();
};


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
        >
            <WorkspaceBackground/>
            <MiniMap
                nodeStrokeColor={(n: Node): string => {
                    if (n.style?.background) return n.style.background as string;
                    if (n.type === 'input') return '#0041d0';
                    if (n.type === 'output') return '#ff0072';
                    if (n.type === 'default') return '#1a192b';

                    return '#eee';
                }}
                nodeColor={(n): string => {
                    if (n.style?.background) return n.style.background as string;

                    return '#fff';
                }}
                nodeBorderRadius={2}
            />
            <Controls />
        </ReactFlow>
    );
};

export default Workspace;
