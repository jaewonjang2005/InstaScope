import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import UploadPage from './pages/UploadPage';
import LoadingPage from './pages/LoadingPage';
import ResultPage from './pages/ResultPage';
import SecretPickPage from './pages/SecretPickPage';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Header />
        <main style={{ minHeight: '80vh' }}>
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/loading" element={<LoadingPage />} />
            <Route path="/result" element={<ResultPage />} />
            <Route path="/secret" element={<SecretPickPage />} />
          </Routes>
        </main>

        <footer style={{
          textAlign: 'center',
          padding: '2rem 0',
          color: 'var(--text-muted)',
          fontSize: '0.85rem',
          borderTop: '1px solid rgba(255,255,255,0.05)',
          marginTop: '4rem'
        }}>
          Insta Taste Recommender — 당신의 숨겨진 취향을 찾아드립니다 © 2026.
        </footer>
      </div>
    </BrowserRouter>
  );
}
