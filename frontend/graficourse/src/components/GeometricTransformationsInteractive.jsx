import React, { useState } from "react";
import styled from "styled-components";

/**
 * GeometricTransformationsInteractive
 * Allows users to interactively translate, scale, and rotate a graphics object.
 */
const GeometricTransformationsInteractive = () => {
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [scale, setScale] = useState(1);
  const [rotation, setRotation] = useState(0);

  const reset = () => {
    setX(0);
    setY(0);
    setScale(1);
    setRotation(0);
  };

  return (
    <Container>
      <Header>
        <Title>Геометриялық түрлендірулер лабораториясы</Title>
        <ResetButton onClick={reset}>Бастапқы күйге келтіру</ResetButton>
      </Header>

      <Description>
        Слайдерлерді қолдану арқылы объектінің кеңістіктегі орнын, өлшемін және бағытын қалай өзгертуге болатынын сынап көріңіз.
      </Description>

      <MainLayout>
        <ControlsArea>
          <ControlGroup>
            <LabelRow>
              <Label>Орын ауыстыру (X):</Label>
              <Value>{x}px</Value>
            </LabelRow>
            <Slider
              type="range"
              min="-100"
              max="100"
              value={x}
              onChange={(e) => setX(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Орын ауыстыру (Y):</Label>
              <Value>{y}px</Value>
            </LabelRow>
            <Slider
              type="range"
              min="-100"
              max="100"
              value={y}
              onChange={(e) => setY(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Масштабтау:</Label>
              <Value>{scale.toFixed(1)}x</Value>
            </LabelRow>
            <Slider
              type="range"
              min="0.2"
              max="2"
              step="0.1"
              value={scale}
              onChange={(e) => setScale(parseFloat(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Айналдыру:</Label>
              <Value>{rotation}°</Value>
            </LabelRow>
            <Slider
              type="range"
              min="0"
              max="360"
              value={rotation}
              onChange={(e) => setRotation(parseInt(e.target.value))}
            />
          </ControlGroup>
        </ControlsArea>

        <VisualArea>
          <CoordinateSystem>
            <AxisX />
            <AxisY />
            <Grid />
            <ObjectContainer
              style={{
                transform: `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`
              }}
            >
              <GraphicObject>
                <ObjectIcon>🎨</ObjectIcon>
              </GraphicObject>
              <CoordinateLabel>(x', y')</CoordinateLabel>
            </ObjectContainer>
          </CoordinateSystem>
        </VisualArea>
      </MainLayout>

      <InfoPanel>
        <InfoItem>
          <strong>Математикалық модель:</strong><br />
          <code>P' = S · R · T · P</code>
        </InfoItem>
        <InfoItem>
          <strong>Нәтиже:</strong><br />
          Объект {rotation}° бұрышқа бұрылды, {scale} есе өзгерді және ({x}, {y}) координаталарына жылжыды.
        </InfoItem>
      </InfoPanel>
    </Container>
  );
};

export default GeometricTransformationsInteractive;

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
  transition: all 0.2s;

  &:hover {
    background: #e2e8f0;
    color: #1e293b;
  }
`;

const Description = styled.p`
  margin: 0 0 24px 0;
  color: #64748b;
  font-size: 0.95rem;
`;

const MainLayout = styled.div`
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
  min-height: 350px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ControlsArea = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 16px;
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
  align-items: center;
`;

const Label = styled.span`
  font-size: 0.85rem;
  font-weight: 500;
  color: #334155;
`;

const Value = styled.span`
  font-family: monospace;
  font-size: 0.9rem;
  font-weight: 700;
  color: #1a1f2e;
  background: #dbeafe;
  padding: 2px 6px;
  border-radius: 4px;
`;

const Slider = styled.input`
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  background: #cbd5e1;
  border-radius: 3px;
  outline: none;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    background: #1a1f2e;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }
`;

const VisualArea = styled.div`
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
`;

const CoordinateSystem = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const AxisX = styled.div`
  position: absolute;
  width: 80%;
  height: 1px;
  background: #94a3b8;
  &::after {
    content: 'X';
    position: absolute;
    right: -20px;
    top: -10px;
    font-size: 10px;
    color: #64748b;
  }
`;

const AxisY = styled.div`
  position: absolute;
  height: 80%;
  width: 1px;
  background: #94a3b8;
  &::after {
    content: 'Y';
    position: absolute;
    top: -20px;
    left: -5px;
    font-size: 10px;
    color: #64748b;
  }
`;

const Grid = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(#e2e8f0 1px, transparent 1px),
    linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.5;
`;

const ObjectContainer = styled.div`
  transition: transform 0.1s ease-out;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const GraphicObject = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border: 2px solid white;
`;

const ObjectIcon = styled.span`
  font-size: 1.5rem;
`;

const CoordinateLabel = styled.span`
  position: absolute;
  top: -20px;
  font-size: 10px;
  color: #1a1f2e;
  font-weight: bold;
  white-space: nowrap;
`;

const InfoPanel = styled.div`
  margin-top: 24px;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px dashed #e2e8f0;
`;

const InfoItem = styled.div`
  font-size: 0.85rem;
  color: #475569;
  line-height: 1.5;

  code {
    background: #f1f5f9;
    padding: 2px 4px;
    border-radius: 4px;
    color: #1d4ed8;
    font-weight: bold;
  }
`;
