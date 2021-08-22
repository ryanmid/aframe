import React from 'react';
import {Connection, Handle, Position} from 'react-flow-renderer';
import {Box, FormControl, Input, InputLabel, MenuItem, Select, TextField} from '@material-ui/core';
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    root: {
        background: '#f0f0f0',
        borderRadius: 10,
        paddingTop: 25,
        paddingBottom: 25,
        paddingLeft: 15,
        paddingRight: 15,
        border: '5px solid purple'
    },
    handle: {
        background: '#0000a0',
        padding: 3
    },
    form: {
        display: "flex",
        flexDirection: "column",
        background: '#f0f0f0'
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
        maxWidth: 300,
    },
}));

interface Props {
    data: any;
    isConnectable: boolean;
}


const Task = (props: Props) => {
    let { data, isConnectable } = props;
    const classes = useStyles();
    const ITEM_HEIGHT = 48;
    const ITEM_PADDING_TOP = 8;
    const MenuProps = {
        PaperProps: {
            style: {
                maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
                width: 250,
            },
        },
    };

    return (
        <div className={classes.root}>
            <Handle
                type={"target"}
                position={Position.Top}
                className={classes.handle}
                onConnect={(connection: Connection) => console.log('connecting ', connection)}
                isConnectable={isConnectable}
            />
            <form
                noValidate
                autoComplete="off"
                className={classes.form}
            >
                <TextField
                    id={`task-${data.id}`}
                    variant="outlined"
                    label={data.label}
                    value={data.name}
                />
            </form>
            <form
                noValidate
                autoComplete="off"
                className={classes.form}
            >
                <FormControl className={classes.formControl}>
                    <InputLabel id="demo-mutiple-name-label">Type</InputLabel>
                    <Select
                        labelId="type-label"
                        id={`type-${data.id}`}
                        multiple
                        value={''}
                        onChange={() => undefined}
                        input={<Input />}
                        MenuProps={MenuProps}
                    >
                    </Select>
                </FormControl>
                <FormControl className={classes.formControl}>
                    <TextField
                        id={`requires-${data.id}`}
                        label="Requires"
                        multiline
                        rows={4}
                        value={''}
                        variant="outlined"
                    />
                </FormControl>
                <FormControl className={classes.formControl}>
                    <TextField
                        id={`provides-${data.id}`}
                        label="Provides"
                        multiline
                        rows={4}
                        value={''}
                        variant="outlined"
                    />
                </FormControl>
            </form>
            <Handle
                type={"source"}
                position={Position.Bottom}
                className={classes.handle}
                onConnect={(connection: Connection) => console.log('connecting ', connection)}
                isConnectable={isConnectable}
            />
        </div>
    );
}

export {
    Task
}

