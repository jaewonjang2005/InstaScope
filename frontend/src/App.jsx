import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import TasteDnaSection from './components/TasteDnaSection';
import SecretCollectionSection from './components/SecretCollectionSection';
import IdealTypeSection from './components/IdealTypeSection';
import AlgorithmExposeSection from './components/AlgorithmExposeSection';
import { RotateCcw, Download } from 'lucide-react';

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (resultData) => {
    setAnalysisResult(resultData);
    // Dopamine Confetti Explosion!
    try {
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });
    } catch (e) {
      console.log('Confetti effect failed', e);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
  };

  return (
    <div className="app-container">
      <Header />

      {!analysisResult ? (
        <UploadSection 
          onAnalysisComplete={handleAnalysisComplete} 
          loading={loading} 
          setLoading={setLoading} 
        />
      ) : (
        <div>
          {/* Action Bar */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <span className="badge badge-fire" style={{ fontSize: '0.9rem', padding: '0.4rem 1rem' }}>
                🎉 프로파일링 완료!
              </span>
              <h2 style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem' }}>
                당신의 인스타그램 데이터 종합 해부 대시보드
              </h2>
            </div>

            <div style={{ display: 'flex', gap: '0.8rem' }}>
              <button className="gradient-btn" onClick={() => window.print()} style={{ padding: '0.6rem 1.4rem', fontSize: '0.9rem' }}>
                <Download size={16} /> 리포트 저장 (PDF/인쇄)
              </button>
              <button 
                onClick={handleReset} 
                style={{ 
                  background: 'rgba(255,255,255,0.08)', 
                  border: '1px solid rgba(255,255,255,0.15)', 
                  color: 'white', 
                  borderRadius: '999px', 
                  padding: '0.6rem 1.4rem', 
                  cursor: 'pointer',
                  fontWeight: '600',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.4rem'
                }}
              >
                <RotateCcw size={16} /> 다른 데이터 분석하기
              </button>
            </div>
          </div>

          {/* 1. Taste DNA */}
          <TasteDnaSection data={analysisResult.taste_dna} />

          {/* 2. Secret Collection */}
          <SecretCollectionSection data={analysisResult.secret_collection} />

          {/* 3. Ideal Type Recommendation (MAIN) */}
          <IdealTypeSection data={analysisResult.ideal_type} />

          {/* 4. Algorithm Expose */}
          <AlgorithmExposeSection data={analysisResult.algorithm_expose} />

          {/* Footer note */}
          <footer style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '4rem', borderTop: '1px solid var(--border-color)', paddingTop: '2rem' }}>
            <p>InstaScope — 100% Client/Local Temporary Processing System.</p>
            <p style={{ marginTop: '0.3rem' }}>모든 개인 데이터는 분석 결과 생성 즉시 메모리 및 파일 스토리지에서 자동 삭제됩니다.</p>
          </footer>
        </div>
      )}
    </div>
  );
}
