import {Background, BackgroundVariant} from "react-flow-renderer";
import React, {Fragment} from "react";

const LargeGrid = () => (
    <Background
        color={'rgb(0,0,0)'}
        variant={BackgroundVariant.Lines}
        gap={100}
        size={2}
    />
);

const SmallGrid = () => (
    <Background
        color={'rgb(0,0,0)'}
        variant={BackgroundVariant.Lines}
        gap={20}
        size={1}
    />
);

const WorkspaceBackground = () => (
    <Fragment>
        <LargeGrid/>
        <SmallGrid/>
    </Fragment>
);

export default WorkspaceBackground;