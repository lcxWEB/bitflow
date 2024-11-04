"use client";

import Link from 'next/link';
import styled from 'styled-components';
import PredictionPage from './prediction';

const Container = styled.div`
  padding: 2rem;
  text-align: center;
`;

// const StyledLink = styled.a`
//   display: inline-block;
//   padding: 1rem 2rem;
//   background: #0070f3;
//   color: white;
//   border-radius: 4px;
//   text-decoration: none;
  
//   &:hover {
//     background: #0051a2;
//   }
// `;

export default function Home() {
  return (
    <Container>
      <PredictionPage />
    </Container>
  );
}