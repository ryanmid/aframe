import React, { useState } from 'react';
import {FunctionComponent} from "react";

import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

import Workspace from "./Workspace";
import '../styles/index.css';

interface AppProps {}

interface MenuState {
    mouseX: number,
    mouseY: number,
    isMenuOpen: boolean
}

const initialState: MenuState = {
    mouseX: null,
    mouseY: null,
    isMenuOpen: false
};

const App: FunctionComponent<AppProps> = () => {
    const [state, setState] = useState(initialState);

    const handleClick = (event: React.MouseEvent) => {
        if (state.isMenuOpen) {
            setState({
                mouseX: event.clientX - 2,
                mouseY: event.clientY - 4,
                isMenuOpen: false
            });
            handleClose();
        }

        console.log(event.currentTarget);

        const target = (event.target as Element);
        if(target.className === 'react-flow__pane') {
            event.preventDefault();
            event.stopPropagation();
            setState({
                mouseX: event.clientX - 2,
                mouseY: event.clientY - 4,
                isMenuOpen: true
            });
        }
    };

    const handleClose = () => {
        setState(initialState);
    };

    return <div className='contextMenuDiv' onContextMenu={handleClick} style={{cursor: 'context-menu'}}>
        <Workspace />
        <Menu
            keepMounted
            open={state.mouseY !== null}
            onClose={handleClose}
            anchorReference="anchorPosition"
            anchorPosition={
                state.mouseY !== null && state.mouseX !== null
                    ? {top: state.mouseY, left: state.mouseX}
                    : undefined
            }
        >
            <MenuItem onClick={handleClose}>Add Component</MenuItem>
            <MenuItem onClick={handleClose}>Add Connector</MenuItem>
        </Menu>
    </div>
}

export default App;