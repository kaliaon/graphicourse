import React, { useState } from "react";
import styled from "styled-components";

/**
 * LightingVisualizationInteractive
 * Demonstrates how light source position and intensity affect shadows and object visibility.
 */
const LightingVisualizationInteractive = () => {
  const [lightPos, setLightPos] = useState(50); // percentage across X axis
  const [intensity, setIntensity] = useState(100);
  const [ambient, setAmbient] = useState(30);

  const reset = () => {
    setLightPos(50);
    setIntensity(100);
    setAmbient(30);
  };

  return (
    <Container>
      <Header>
        <Title>Жарықтандыру және Көлеңке лабораториясы</Title>
        <ResetButton onClick={reset}>Бастапқы күй</ResetButton>
      </Header>

      <Description>
        Жарық көзінің орнын жылжыту арқылы көлеңкенің қалай өзгеретінін бақылаңыз.
        Жарық қарқындылығы объектінің айқындығына әсер етеді.
      </Description>

      <MainLayout>
        <ControlsArea>
          <ControlGroup>
            <LabelRow>
              <Label>Жарық көзінің орны:</Label>
              <Value>{lightPos}%</Value>
            </LabelRow>
            <Slider
              type="range" min="0" max="100" value={lightPos}
              onChange={(e) => setLightPos(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Жарық қарқындылығы (Direct):</Label>
              <Value>{intensity}%</Value>
            </LabelRow>
            <Slider
              type="range" min="0" max="200" value={intensity}
              onChange={(e) => setIntensity(parseInt(e.target.value))}
            />
          </ControlGroup>

          <ControlGroup>
            <LabelRow>
              <Label>Шашыраңқы жарық (Ambient):</Label>
              <Value>{ambient}%</Value>
            </LabelRow>
            <Slider
              type="range" min="0" max="100" value={ambient}
              onChange={(e) => setAmbient(parseInt(e.target.value))}
            />
          </ControlGroup>
        </ControlsArea>

        <VisualArea>
          <Stage>
            {/* Light Source Visual */}
            <LightSource style={{ left: `${lightPos}%`, opacity: intensity / 100 }} />

            {/* 3D-like Sphere/Object */}
            <ObjectContainer>
              <ObjectBase style={{
                background: `radial-gradient(circle at ${lightPos}% 20%, 
                  rgba(255,255,255,${intensity / 100}) 0%, 
                  #3b82f6 ${30 + (intensity / 10)}%, 
                  #1d4ed8 100%)`,
                boxShadow: `inset 0 0 ${40 - intensity / 5}px rgba(0,0,0,0.5)`,
                opacity: (intensity + ambient) / 100
              }} />

              {/* Dynamic Shadow */}
              <Shadow style={{
                left: `${lightPos}%`,
                transform: `translateX(-50%) scaleX(${1.5 + Math.abs(50 - lightPos) / 20})`,
                opacity: (intensity / 100) * 0.6,
                filter: `blur(${10 + Math.abs(50 - lightPos) / 5}px)`
              }} />
            </ObjectContainer>
          </Stage>
          <StatusText>
            Визуализация: {intensity > 150 ? "Жоғары жарық" : intensity < 50 ? "Төмен жарық" : "Қалыпты"}
          </StatusText>
        </VisualArea>
      </MainLayout>

      <InfoGrid>
        <InfoItem>
          <strong>Нүктелік жарық:</strong> Жарық көзінен барлық бағытқа таралады.
        </InfoItem>
        <InfoItem>
          <strong>Көлеңке:</strong> Жарық өтпейтін аймақ, объект пішінін көрсетеді.
        </InfoItem>
      </InfoGrid>
    </Container>
  );
};

export default LightingVisualizationInteractive;

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
  margin-bottom: 12px;
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
  cursor: pointer;
  &:hover { background: #e2e8f0; }
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
  @media (max-width: 768px) { grid-template-columns: 1fr; }
`;

const ControlsArea = styled.div`
  display: flex;
  flex-direction: column;
  gap: 24px;
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
  font-size: 0.85rem;
  font-weight: 500;
  color: #334155;
`;

const Value = styled.span`
  font-family: monospace;
  font-weight: bold;
  color: #1a1f2e;
`;

const Slider = styled.input`
  width: 100%;
  height: 6px;
  background: #cbd5e1;
  border-radius: 3px;
  outline: none;
`;

const VisualArea = styled.div`
  background: #1e293b;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
`;

const Stage = styled.div`
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 40px;
`;

const LightSource = styled.div`
  position: absolute;
  top: 20px;
  width: 30px;
  height: 30px;
  background: #fef08a;
  border-radius: 50%;
  box-shadow: 0 0 40px #facc15, 0 0 80px #facc15;
  z-index: 10;
  transition: left 0.2s ease-out;
`;

const ObjectContainer = styled.div`
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ObjectBase = styled.div`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  position: relative;
  z-index: 5;
  transition: background 0.2s ease-out;
`;

const Shadow = styled.div`
  position: absolute;
  bottom: -20px;
  width: 120px;
  height: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  z-index: 1;
  transition: all 0.2s ease-out;
`;

const StatusText = styled.div`
  padding: 8px 16px;
  background: rgba(0,0,0,0.3);
  color: #94a3b8;
  font-size: 0.75rem;
  font-family: monospace;
`;

const InfoGrid = styled.div`
  margin-top: 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  border-top: 1px dashed #e2e8f0;
  padding-top: 16px;
`;

const InfoItem = styled.div`
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
  strong { color: #334155; }
`;
