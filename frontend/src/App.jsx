import React, { useState } from 'react';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import LoadingSection from './components/LoadingSection';
import TasteDnaSection from './components/TasteDnaSection';
import SecretCollectionSection from './components/SecretCollectionSection';
import IdealTypeSection from './components/IdealTypeSection';
import AlgorithmExposeSection from './components/AlgorithmExposeSection';
import confetti from 'canvas-confetti';
import { Flame, Lock, Heart, Eye, RefreshCw } from 'lucide-react';
import './App.css';

export default function App() {
  const [step, setStep] = useState('upload'); // 'upload' | 'loading' | 'results'
  const [analysisData, setAnalysisData] = useState(null);
  const [activeTab, setActiveTab] = useState('taste'); // 'taste' | 'secret' | 'ideal' | 'expose'

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    
    // Trigger celebratory confetti effect
    try {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (e) {
      console.log('Confetti error:', e);
    }
  };

  const handleReset = () => {
    setAnalysisData(null);
    setStep('upload');
    setActiveTab('taste');
  };

  return (
    <div className="app-container">
      <Header />

      <main style={{ minHeight: '80vh' }}>
        {/* Page 1: Upload Landing Page */}
        {step === 'upload' && (
          <UploadSection 
            onAnalysisComplete={handleAnalysisComplete} 
            setStep={setStep}
          />
        )}

        {/* Page 2: Detective Loading Profiler Page */}
        {step === 'loading' && (
          <LoadingSection />
        )}

        {/* Page 3: Profile Analysis Results Dashboard */}
        {step === 'results' && analysisData && (
          <div>
            {/* Navigation Tabs Bar */}
            <div className="glass-card" style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '0.8rem',
              padding: '0.8rem 1rem',
              borderRadius: '20px',
              margin: '1.5rem 0 2.5rem',
              overflowX: 'auto'
            }}>
              <button 
                className={`gradient-btn ${activeTab === 'taste' ? '' : 'badge-mild'}`}
                style={{ opacity: activeTab === 'taste' ? 1 : 0.6 }}
                onClick={() => setActiveTab('taste')}
              >
                <Flame size={18} /> 🌶️ 취향 DNA 리포트
              </button>

              <button 
                className={`gradient-btn ${activeTab === 'secret' ? '' : 'badge-mild'}`}
                style={{ opacity: activeTab === 'secret' ? 1 : 0.6 }}
                onClick={() => setActiveTab('secret')}
              >
                <Lock size={18} /> 🔒 비밀 컬렉션 해부
              </button>

              <button 
                className={`gradient-btn ${activeTab === 'ideal' ? '' : 'badge-mild'}`}
                style={{ opacity: activeTab === 'ideal' ? 1 : 0.6 }}
                onClick={() => setActiveTab('ideal')}
              >
                <Heart size={18} /> 💕 이상형 계정 추적
              </button>

              <button 
                className={`gradient-btn ${activeTab === 'expose' ? '' : 'badge-mild'}`}
                style={{ opacity: activeTab === 'expose' ? 1 : 0.6 }}
                onClick={() => setActiveTab('expose')}
              >
                <Eye size={18} /> 🕵️ 알고리즘 타겟팅 폭로
              </button>

              <button 
                onClick={handleReset}
                style={{
                  background: 'rgba(255, 255, 255, 0.08)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  color: '#fff',
                  borderRadius: '12px',
                  padding: '0.6rem 1rem',
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  marginLeft: 'auto'
                }}
              >
                <RefreshCw size={14} /> 새 분석하기
              </button>
            </div>

            {/* Active Tab Content Display */}
            {activeTab === 'taste' && (
              <TasteDnaSection data={analysisData.taste_dna} />
            )}

            {activeTab === 'secret' && (
              <SecretCollectionSection data={analysisData.secret_collection} />
            )}

            {activeTab === 'ideal' && (
              <IdealTypeSection data={analysisData.ideal_type} />
            )}

            {activeTab === 'expose' && (
              <AlgorithmExposeSection data={analysisData.algorithm_expose} />
            )}
          </div>
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '2rem 0',
        color: 'var(--text-muted)',
        fontSize: '0.85rem',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        marginTop: '4rem'
      }}>
        InstaScope — 인스타그램 알고리즘 프로파일링 엔진 © 2026. All rights reserved.
      </footer>
    </div>
  );
}
