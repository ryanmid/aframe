import React from 'react';
import {Connection, Handle, Position} from 'react-flow-renderer';
import {TextField} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        paddingTop: 10,
        paddingBottom: 10,
        paddingLeft: 15,
        paddingRight: 15,
        background: '#ffffff',
        borderRadius: 10,
        border: '5px solid rgb(255,0,255)',
    },
    handle: {
        'background': '#0000a0',
        padding: 3
    }
}));

interface Props {
    data: any;
    isConnectable: boolean;
}

const Phase = (props: Props) => {
    let { data, isConnectable } = props;
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Handle
                type={"target"}
                position={Position.Left}
                className={classes.handle}
                onConnect={(connection: Connection) => console.log('connecting ', connection)}
                isConnectable={isConnectable}
            />
            <form
                noValidate
                autoComplete="off"
            >
                <TextField
                    id={`phase-${data.id}`}
                    variant="outlined"
                    value={data.label}
                />
            </form>
            <Handle
                id={`next-phase-${data.id}`}
                type={"source"}
                position={Position.Right}
                className={classes.handle}
                onConnect={(connection: Connection) => console.log('connecting ', connection)}
                isConnectable={isConnectable}
            />
            <Handle
                id={`first-task-${data.id}`}
                type={"source"}
                position={Position.Bottom}
                className={classes.handle}
                onConnect={(connection: Connection) => console.log('connecting ', connection)}
                isConnectable={isConnectable}
            />
        </div>
    )
}

export {
    Phase
}

