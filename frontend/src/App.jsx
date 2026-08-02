import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import UploadPage from './pages/UploadPage';
import LoadingPage from './pages/LoadingPage';
import ResultPage from './pages/ResultPage';
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
          Insta 1-Pick — 당신의 진짜 최애를 찾아드립니다 © 2026.
        </footer>
      </div>
    </BrowserRouter>
  );
}
