import React, { useState } from "react";
import styled from "styled-components";

const RasterVectorComparison = () => {
    const [zoomLevel, setZoomLevel] = useState(1);
    const [activeTab, setActiveTab] = useState("raster");

    return (
        <Container>
            <Title>Интерактивті салыстыру: Растр vs Вектор</Title>
            <ControlPanel>
                <ToggleGroup>
                    <ToggleButton
                        active={activeTab === "raster"}
                        onClick={() => setActiveTab("raster")}
                    >
                        Растрлық (JPEG/PNG)
                    </ToggleButton>
                    <ToggleButton
                        active={activeTab === "vector"}
                        onClick={() => setActiveTab("vector")}
                    >
                        Векторлық (SVG)
                    </ToggleButton>
                </ToggleGroup>

                <ZoomControl>
                    <label>Масштаб: {zoomLevel}x</label>
                    <input
                        type="range"
                        min="1"
                        max="10"
                        step="0.1"
                        value={zoomLevel}
                        onChange={(e) => setZoomLevel(parseFloat(e.target.value))}
                    />
                </ZoomControl>
            </ControlPanel>

            <CanvasContainer>
                <Canvas>
                    {activeTab === "raster" ? (
                        <RasterExample zoom={zoomLevel} />
                    ) : (
                        <VectorExample zoom={zoomLevel} />
                    )}
                </Canvas>
                <InfoOverlay>
                    {activeTab === "raster" ? (
                        <p>
                            Растрлық графика пиксельдерден тұрады. Үлкейткенде ({zoomLevel}x)
                            пиксельдену пайда болады және сапасы жоғалады.
                        </p>
                    ) : (
                        <p>
                            Векторлық графика формулалармен сипатталады. Үлкейткенде ({zoomLevel}
                            x) сызықтар тегіс болып қалады және сапасы жоғалмайды.
                        </p>
                    )}
                </InfoOverlay>
            </CanvasContainer>
        </Container>
    );
};

// Visual components simulating raster/vector behavior
const RasterExample = ({ zoom }) => (
    <ExampleWrapper>
        <CircleBase
            style={{
                transform: `scale(${zoom})`,
                // Simulate pixelation with CSS filter or distinct rendering
                imageRendering: zoom > 1 ? "pixelated" : "auto",
                filter: zoom > 2 ? `blur(${zoom * 0.5}px)` : "none", // Blur to simulate quality loss perception or just pixelate
            }}
        >
            <svg width="200" height="200" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" fill="#3066be" />
                <image
                    href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCI+PGNpcmNsZSBjeD0iMTAiIGN5PSIxMCIgcj0iMTAiIGZpbGw9IiMzMDY2YmUiLz48L3N2Zz4=" // Placeholder
                    width="200"
                    height="200"
                />
                {/* We actually render a vector here but simulate raster effects via CSS */}
            </svg>
            {/* Better simulation: CSS Grid of div pixels? Too heavy. 
          Use a small CSS shapes or pseudo-elements to show "pixels" appearing?
          Simple approach: CSS transform with pixelation.
      */}
            <RasterSimulation />
        </CircleBase>
    </ExampleWrapper>
);

const VectorExample = ({ zoom }) => (
    <ExampleWrapper>
        <CircleBase
            style={{
                transform: `scale(${zoom})`,
                // Vector stays sharp
            }}
        >
            <svg width="200" height="200" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" fill="#27ae60" />
                <text
                    x="100"
                    y="110"
                    textAnchor="middle"
                    fill="white"
                    fontSize="40"
                    fontWeight="bold"
                >
                    V
                </text>
            </svg>
        </CircleBase>
    </ExampleWrapper>
);

export default RasterVectorComparison;

// Styled Components
const Container = styled.div`
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin: 30px 0;
  width: 100%;
  max-width: 600px;
`;

const Title = styled.h3`
  margin: 0 0 20px 0;
  color: #333;
  text-align: center;
`;

const ControlPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
  @media (min-width: 500px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
`;

const ToggleGroup = styled.div`
  display: flex;
  background: #f0f0f0;
  border-radius: 8px;
  padding: 4px;
  gap: 4px;
`;

const ToggleButton = styled.button`
  border: none;
  background: ${(props) => (props.active ? "white" : "transparent")};
  color: ${(props) => (props.active ? "#3066be" : "#666")};
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  box-shadow: ${(props) =>
        props.active ? "0 2px 4px rgba(0,0,0,0.1)" : "none"};
  transition: all 0.2s;
`;

const ZoomControl = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #555;

  input {
    cursor: pointer;
  }
`;

const CanvasContainer = styled.div`
  position: relative;
  height: 300px;
  background: #f8f9fa;
  border: 1px dashed #ccc;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Canvas = styled.div`
  /* Center the content */
`;

const InfoOverlay = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 15px;
  border-top: 1px solid #eee;
  font-size: 0.9rem;
  color: #333;
  text-align: center;
`;

const ExampleWrapper = styled.div`
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CircleBase = styled.div`
  transition: transform 0.1s linear; /* Fast transition for zoom */
  transform-origin: center;
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const RasterSimulation = styled.div`
  /* A trick to simulate pixels: a small background pattern that scales up */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(45deg, #ccc 25%, transparent 25%), 
    linear-gradient(-45deg, #ccc 25%, transparent 25%), 
    linear-gradient(45deg, transparent 75%, #ccc 75%), 
    linear-gradient(-45deg, transparent 75%, #ccc 75%);
  background-size: 10px 10px; /* Small pixels originally */
  background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
  opacity: 0.05;
  pointer-events: none;
`;
