import React, { useState } from "react";
import styled from "styled-components";

/**
 * ColorModelsInteractive
 * An interactive component for the "Color Models" lesson.
 * Allows users to mix RGB colors and see the resulting HEX and CMYK equivalents.
 */
const ColorModelsInteractive = () => {
  const [r, setR] = useState(59);
  const [g, setG] = useState(130);
  const [b, setB] = useState(246);

  // Helper to convert RGB to HEX
  const rgbToHex = (r, g, b) => {
    return "#" + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('').toUpperCase();
  };

  // Helper to convert RGB to CMYK
  const rgbToCmyk = (r, g, b) => {
    let r_prime = r / 255;
    let g_prime = g / 255;
    let b_prime = b / 255;

    let k = 1 - Math.max(r_prime, g_prime, b_prime);

    // Handle black separately to avoid division by zero
    if (k === 1) {
      return { c: 0, m: 0, y: 0, k: 100 };
    }

    let c = (1 - r_prime - k) / (1 - k);
    let m = (1 - g_prime - k) / (1 - k);
    let y = (1 - b_prime - k) / (1 - k);

    return {
      c: Math.round(c * 100),
      m: Math.round(m * 100),
      y: Math.round(y * 100),
      k: Math.round(k * 100)
    };
  };

  const cmyk = rgbToCmyk(r, g, b);
  const hex = rgbToHex(r, g, b);

  return (
    <Container>
      <Title>Интерактивті түстер миксері (RGB)</Title>
      <Description>
        Слайдерлерді жылжыту арқылы RGB түстерінің қалай бірігетінін және олардың CMYK баспа моделіндегі сәйкестігін көріңіз.
      </Description>

      <Layout>
        <Controls>
          <SliderGroup>
            <LabelContainer>
              <Label>Қызыл (Red): <Value color="#ef4444">{r}</Value></Label>
            </LabelContainer>
            <Slider
              type="range"
              min="0"
              max="255"
              value={r}
              accent="#ef4444"
              onChange={(e) => setR(parseInt(e.target.value))}
            />
          </SliderGroup>

          <SliderGroup>
            <LabelContainer>
              <Label>Жасыл (Green): <Value color="#22c55e">{g}</Value></Label>
            </LabelContainer>
            <Slider
              type="range"
              min="0"
              max="255"
              value={g}
              accent="#22c55e"
              onChange={(e) => setG(parseInt(e.target.value))}
            />
          </SliderGroup>

          <SliderGroup>
            <LabelContainer>
              <Label>Көк (Blue): <Value color="#3b82f6">{b}</Value></Label>
            </LabelContainer>
            <Slider
              type="range"
              min="0"
              max="255"
              value={b}
              accent="#3b82f6"
              onChange={(e) => setB(parseInt(e.target.value))}
            />
          </SliderGroup>
        </Controls>

        <PreviewSection>
          <PreviewCard>
            <ColorBox style={{ backgroundColor: `rgb(${r}, ${g}, ${b})` }}>
              <HexValue contrast={r * 0.299 + g * 0.587 + b * 0.114 > 128}>{hex}</HexValue>
            </ColorBox>
            <StatsList>
              <StatRow>
                <StatLabel>RGB:</StatLabel>
                <StatValue>{r}, {g}, {b}</StatValue>
              </StatRow>
              <StatRow>
                <StatLabel>CMYK:</StatLabel>
                <StatValue>
                  <CmykTag color="#00ffff">C {cmyk.c}%</CmykTag>
                  <CmykTag color="#ff00ff">M {cmyk.m}%</CmykTag>
                  <CmykTag color="#ffff00">Y {cmyk.y}%</CmykTag>
                  <CmykTag color="#000000">K {cmyk.k}%</CmykTag>
                </StatValue>
              </StatRow>
            </StatsList>
          </PreviewCard>
        </PreviewSection>
      </Layout>

      <InfoBox>
        <InfoIcon>💡</InfoIcon>
        <InfoText>
          <strong>RGB</strong> — мониторлар мен экрандарда қолданылатын аддитивті модель.
          Ал <strong>CMYK</strong> — субтрактивті модель, ол баспа өнімдерінде қолданылады.
        </InfoText>
      </InfoBox>
    </Container>
  );
};

export default ColorModelsInteractive;

const Container = styled.div`
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  margin: 32px 0;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h4`
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
`;

const Description = styled.p`
  margin: 0 0 24px 0;
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.5;
`;

const Layout = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const Controls = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const SliderGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const LabelContainer = styled.div`
  display: flex;
  justify-content: space-between;
`;

const Label = styled.span`
  font-size: 0.9rem;
  font-weight: 500;
  color: #475569;
`;

const Value = styled.span`
  color: ${props => props.color};
  font-weight: 700;
  font-family: monospace;
`;

const Slider = styled.input`
  -webkit-appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #e2e8f0;
  outline: none;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: ${props => props.accent};
    cursor: pointer;
    box-shadow: 0 0 0 4px white;
    border: 2px solid ${props => props.accent};
    transition: transform 0.1s ease;
  }

  &::-webkit-slider-thumb:hover {
    transform: scale(1.1);
  }
`;

const PreviewSection = styled.div`
  display: flex;
  justify-content: center;
`;

const PreviewCard = styled.div`
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 300px;
`;

const ColorBox = styled.div`
  width: 100%;
  height: 150px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: background-color 0.1s ease;
  border: 1px solid rgba(0,0,0,0.05);
`;

const HexValue = styled.span`
  font-family: monospace;
  font-size: 1.5rem;
  font-weight: 700;
  color: ${props => props.contrast ? '#000000' : '#ffffff'};
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
`;

const StatsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const StatRow = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const StatLabel = styled.span`
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
`;

const StatValue = styled.div`
  font-family: monospace;
  font-size: 0.9rem;
  font-weight: 600;
  color: #334155;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
`;

const CmykTag = styled.span`
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
  border-left: 3px solid ${props => props.color};
`;

const InfoBox = styled.div`
  display: flex;
  gap: 12px;
  align-items: flex-start;
  margin-top: 24px;
  padding: 12px;
  background: #eff6ff;
  border-radius: 8px;
  border: 1px solid #bfdbfe;
`;

const InfoIcon = styled.span`
  font-size: 1.2rem;
`;

const InfoText = styled.p`
  margin: 0;
  font-size: 0.85rem;
  color: #1a1f2e;
  line-height: 1.4;
`;
