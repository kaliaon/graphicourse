import React, { useState } from "react";
import styled from "styled-components";

/**
 * ThreeDConceptsInteractive
 * An interactive 3D viewer using CSS 3D transforms.
 * Allows users to rotate a cube on X, Y, Z axes and adjust camera "zoom".
 */
const ThreeDConceptsInteractive = () => {
  const [rotX, setRotX] = useState(-20);
  const [rotY, setRotY] = useState(30);
  const [rotZ, setRotZ] = useState(0);
  const [zoom, setZoom] = useState(300);
  const [showVertices, setShowVertices] = useState(true);
  const [showEdges, setShowEdges] = useState(true);
  const [showFaces, setShowFaces] = useState(true);

  const reset = () => {
    setRotX(-20);
    setRotY(30);
    setRotZ(0);
    setZoom(300);
  };

  return (
    <Container>
      <Header>
        <Title>3D Кеңістік және Модельдеу зертханасы</Title>
        <ResetButton onClick={reset}>Қалпына келтіру</ResetButton>
      </Header>
      <Description>
        3D объектінің құрылымын түсіну үшін слайдерлерді қолданыңыз. X, Y, Z осьтері бойынша айналдыру
        арқылы нысанды кез келген бұрыштан көре аласыз.
      </Description>

      <MainLayout>
        <ControlsArea>
          <ControlGroup>
            <LabelRow>
              <Label>X осі бойынша айналдыру:</Label>
              <Value>{rotX}°</Value>
            </LabelRow>
            <Slider
              type="range" min="-180" max="180" value={rotX}
              onChange={(e) => setRotX(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Y осі бойынша айналдыру:</Label>
              <Value>{rotY}°</Value>
            </LabelRow>
            <Slider
              type="range" min="-180" max="180" value={rotY}
              onChange={(e) => setRotY(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Z осі бойынша айналдыру:</Label>
              <Value>{rotZ}°</Value>
            </LabelRow>
            <Slider
              type="range" min="-180" max="180" value={rotZ}
              onChange={(e) => setRotZ(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Камера қашықтығы (Zoom):</Label>
              <Value>{zoom}px</Value>
            </LabelRow>
            <Slider
              type="range" min="150" max="600" value={zoom}
              onChange={(e) => setZoom(parseInt(e.target.value))}
            />
          </ControlGroup>

          <Divider />

          <VisibilityGroup>
            <CheckboxLabel>
              <input
                type="checkbox"
                checked={showFaces}
                onChange={() => setShowFaces(!showFaces)}
              />
              Беттер (Faces)
            </CheckboxLabel>
            <CheckboxLabel>
              <input
                type="checkbox"
                checked={showEdges}
                onChange={() => setShowEdges(!showEdges)}
              />
              Қабырғалар (Edges)
            </CheckboxLabel>
            <CheckboxLabel>
              <input
                type="checkbox"
                checked={showVertices}
                onChange={() => setShowVertices(!showVertices)}
              />
              Нүктелер (Vertices)
            </CheckboxLabel>
          </VisibilityGroup>
        </ControlsArea>

        <VisualArea>
          <Scene style={{ perspective: `${zoom * 2}px` }}>
            <CubeContainer
              style={{
                transform: `translateZ(-100px) rotateX(${rotX}deg) rotateY(${rotY}deg) rotateZ(${rotZ}deg)`
              }}
            >
              {/* Coordinate System Placeholder */}
              <AxisX />
              <AxisY />
              <AxisZ />

              {/* Cube Faces */}
              <Cube showFaces={showFaces} showEdges={showEdges}>
                <Face className="front">Front</Face>
                <Face className="back">Back</Face>
                <Face className="right">Right</Face>
                <Face className="left">Left</Face>
                <Face className="top">Top</Face>
                <Face className="bottom">Bottom</Face>
              </Cube>

              {/* Vertices */}
              {showVertices && (
                <>
                  <Vertex style={{ transform: 'translate3d(-50px, -50px, 50px)' }} />
                  <Vertex style={{ transform: 'translate3d(50px, -50px, 50px)' }} />
                  <Vertex style={{ transform: 'translate3d(-50px, 50px, 50px)' }} />
                  <Vertex style={{ transform: 'translate3d(50px, 50px, 50px)' }} />
                  <Vertex style={{ transform: 'translate3d(-50px, -50px, -50px)' }} />
                  <Vertex style={{ transform: 'translate3d(50px, -50px, -50px)' }} />
                  <Vertex style={{ transform: 'translate3d(-50px, 50px, -50px)' }} />
                  <Vertex style={{ transform: 'translate3d(50px, 50px, -50px)' }} />
                </>
              )}
            </CubeContainer>
          </Scene>
          <OverlayInfo>3D Түрлендіру: {rotX}°, {rotY}°, {rotZ}°</OverlayInfo>
        </VisualArea>
      </MainLayout>

      <Legend>
        <LegendItem><ColorBox color="#ef4444" /> X осі</LegendItem>
        <LegendItem><ColorBox color="#22c55e" /> Y осі</LegendItem>
        <LegendItem><ColorBox color="#3b82f6" /> Z осі</LegendItem>
      </Legend>
    </Container>
  );
};

export default ThreeDConceptsInteractive;

const Container = styled.div`
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  margin: 32px 0;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
`;

const Title = styled.h4`
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
`;

const ResetButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  color: #475569;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  &:hover { background: #e2e8f0; }
`;

const Description = styled.p`
  margin: 0 0 24px 0;
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.5;
`;

const MainLayout = styled.div`
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 32px;
  min-height: 400px;
  @media (max-width: 768px) { grid-template-columns: 1fr; }
`;

const ControlsArea = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
`;

const ControlGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const LabelRow = styled.div`
  display: flex;
  justify-content: space-between;
`;

const Label = styled.span`
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
`;

const Value = styled.span`
  font-family: monospace;
  font-size: 0.85rem;
  color: #1a1f2e;
  font-weight: 700;
`;

const Slider = styled.input`
  width: 100%;
  height: 6px;
  background: #cbd5e1;
  border-radius: 3px;
  outline: none;
`;

const Divider = styled.div`
  height: 1px;
  background: #e2e8f0;
  margin: 10px 0;
`;

const VisibilityGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const CheckboxLabel = styled.label`
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #334155;
  cursor: pointer;
  input { cursor: pointer; }
`;

const VisualArea = styled.div`
  background: #0f172a;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Scene = styled.div`
  width: 300px;
  height: 300px;
  position: relative;
  transform-style: preserve-3d;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const CubeContainer = styled.div`
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out;
`;

const Cube = styled.div`
  width: 100%;
  height: 100%;
  position: absolute;
  transform-style: preserve-3d;

  & > div {
    position: absolute;
    width: 100px;
    height: 100px;
    border: ${props => props.showEdges ? '1px solid rgba(255,255,255,0.8)' : 'none'};
    background: ${props => props.showFaces ? 'rgba(59, 130, 246, 0.4)' : 'transparent'};
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    font-weight: bold;
    backface-visibility: visible;
  }

  .front  { transform: rotateY(0deg) translateZ(50px); }
  .back   { transform: rotateY(180deg) translateZ(50px); }
  .right  { transform: rotateY(90deg) translateZ(50px); }
  .left   { transform: rotateY(-90deg) translateZ(50px); }
  .top    { transform: rotateX(90deg) translateZ(50px); }
  .bottom { transform: rotateX(-90deg) translateZ(50px); }
`;

const Face = styled.div``;

const Vertex = styled.div`
  position: absolute;
  width: 6px;
  height: 6px;
  background: #f59e0b;
  border-radius: 50%;
  margin-left: -3px;
  margin-top: -3px;
  box-shadow: 0 0 10px #f59e0b;
  z-index: 10;
`;

const Axis = styled.div`
  position: absolute;
  width: 1px;
  height: 1px;
  transform-style: preserve-3d;
`;

const AxisX = styled(Axis)`
  width: 250px;
  height: 1px;
  background: rgba(239, 68, 68, 0.5);
  left: -75px;
  top: 50px;
  &::after { content: 'X'; position: absolute; right: -15px; top: -5px; color: #ef4444; font-size: 10px; }
`;

const AxisY = styled(Axis)`
  height: 250px;
  width: 1px;
  background: rgba(34, 197, 94, 0.5);
  top: -75px;
  left: 50px;
  &::after { content: 'Y'; position: absolute; top: -15px; left: -5px; color: #22c55e; font-size: 10px; }
`;

const AxisZ = styled(Axis)`
  width: 1px;
  height: 1px;
  background: blue;
  transform: translateZ(-125px);
  &::after { 
    content: ''; 
    position: absolute; 
    width: 1px; 
    height: 250px; 
    background: rgba(59, 130, 246, 0.5); 
    transform: rotateX(90deg);
  }
`;

const OverlayInfo = styled.div`
  position: absolute;
  bottom: 12px;
  left: 12px;
  color: #94a3b8;
  font-size: 0.75rem;
  font-family: monospace;
`;

const Legend = styled.div`
  margin-top: 24px;
  display: flex;
  gap: 20px;
  justify-content: center;
  border-top: 1px dashed #e2e8f0;
  padding-top: 16px;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
`;

const ColorBox = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background: ${props => props.color};
`;
