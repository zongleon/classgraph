import React from "react";

import Graph from "graphology";
import getNodeProgramImage from "sigma/rendering/webgl/programs/node.image";
import { SigmaContainer, ControlsContainer, ZoomControl, FullScreenControl, SearchControl } from "@react-sigma/core";
import { LayoutForceAtlas2Control } from "@react-sigma/layout-forceatlas2";

import GraphTitle from "./GraphTitle";
import jsonGraph from "/src/gph.json";

import "@react-sigma/core/lib/react-sigma.min.css";

const DemoGraph: React.FC<{}> = () => {
  const graph = Graph.from(jsonGraph);
  return (
    <SigmaContainer
      graph={graph}
      // style={{ height: "500px" }}
      settings={{
        nodeProgramClasses: { image: getNodeProgramImage() },
        defaultNodeType: "image",
        defaultEdgeType: "arrow",
        labelDensity: 0.1,
        labelGridCellSize: 60,
        labelRenderedSizeThreshold: 15,
        labelFont: "Lato, sans-serif",
        zIndex: true,
      }}
    >
    <div className="contents">
      <GraphTitle />
      <ControlsContainer position={"bottom-right"}>
        <ZoomControl />
        <FullScreenControl />
        <LayoutForceAtlas2Control />
      </ControlsContainer>
      <ControlsContainer position={"top-right"}>
        <SearchControl style={{ width: "200px" }} />
      </ControlsContainer>
    </div>
      
    </SigmaContainer>
  );
};

export default DemoGraph;