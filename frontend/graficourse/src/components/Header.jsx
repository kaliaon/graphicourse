import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styled from "styled-components";


const Header = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <HeaderWrapper>
      <HeaderContainer>
        <LogoSection>
          <LogoLink to="/">
            Graphi<LogoAccent>Course</LogoAccent>
          </LogoLink>
        </LogoSection>

        <NavSection>
          <MobileMenuButton onClick={toggleMobileMenu}>
            <MobileMenuIcon open={mobileMenuOpen}>
              <span></span>
              <span></span>
              <span></span>
            </MobileMenuIcon>
          </MobileMenuButton>

          {/* Navigation links removed as requested */}
        </NavSection>


      </HeaderContainer>
    </HeaderWrapper>
  );
};

export default Header;

// Styled Components
const HeaderWrapper = styled.header`
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const HeaderContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
  height: 70px;

  @media (max-width: 768px) {
    position: relative;
  }
`;

const LogoSection = styled.div`
  flex: 0 0 auto;
`;

const LogoLink = styled(Link)`
  font-size: 1.5rem;
  font-weight: 500;
  color: #1a1f2e;
  text-decoration: none;
  display: flex;
  align-items: center;
`;

const LogoAccent = styled.span`
  color: #2b3a55;
`;

const NavSection = styled.nav`
  display: flex;
  align-items: center;

  @media (max-width: 768px) {
    order: 3;
    width: 100%;
  }
`;

const NavLinks = styled.ul`
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;

  @media (max-width: 768px) {
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    flex-direction: column;
    background-color: white;
    box-shadow: 0 10px 10px rgba(0, 0, 0, 0.05);
    padding: 0;
    max-height: ${(props) => (props.open ? "300px" : "0")};
    overflow: hidden;
    transition: max-height 0.3s ease;
  }
`;

const NavItem = styled.li`
  margin: 0 15px;

  @media (max-width: 768px) {
    margin: 0;
  }
`;

const NavLink = styled(Link)`
  text-decoration: none;
  color: #4a5568;
  font-weight: 500;
  font-size: 1rem;
  padding: 10px 0;
  display: block;
  position: relative;
  transition: color 0.2s;

  &:hover {
    color: #3066be;
  }

  &:after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #3066be;
    transition: width 0.3s;
  }

  &:hover:after {
    width: 100%;
  }

  @media (max-width: 768px) {
    padding: 15px 20px;

    &:after {
      display: none;
    }

    &:hover {
      background-color: #f8fafc;
    }
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  margin-left: auto;

  @media (max-width: 768px) {
    display: block;
  }
`;

const MobileMenuIcon = styled.div`
  width: 24px;
  height: 18px;
  position: relative;

  span {
    display: block;
    position: absolute;
    height: 2px;
    width: 100%;
    background: #4a5568;
    border-radius: 2px;
    transition: transform 0.2s ease, opacity 0.2s ease;

    &:nth-child(1) {
      top: ${(props) => (props.open ? "8px" : "0")};
      transform: ${(props) => (props.open ? "rotate(45deg)" : "none")};
    }

    &:nth-child(2) {
      top: 8px;
      opacity: ${(props) => (props.open ? "0" : "1")};
    }

    &:nth-child(3) {
      top: ${(props) => (props.open ? "8px" : "16px")};
      transform: ${(props) => (props.open ? "rotate(-45deg)" : "none")};
    }
  }
`;
