import React from 'react';

import {Node, Edge, ArrowHeadType} from 'react-flow-renderer';

const initialElements: Array<Node | Edge> = [
    {
        id: '1',
        type: 'phase',
        data: {
            label: 'Phase Name',
            name: 'Phase I'
        },
        position: {x: 10, y: 100},
    },
    {
        id: '2',
        type: 'task',
        data: {
            label: 'Task Name',
            name: 'Task I'
        },
        position: {x: 10, y: 250},
    },
    {
        id: '3',
        type: 'task',
        data: {
            label: 'Task Name',
            name: 'Task II'
        },
        position: {x: 10, y: 750},
    },
    {
        id: '4',
        type: 'task',
        data: {
            label: 'Task Name',
            name: 'Task II'
        },
        position: {x: 10, y: 1250},
    },
];

export default initialElements;
