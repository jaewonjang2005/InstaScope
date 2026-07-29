import React, { useState, useEffect } from 'react';
import { Search, ShieldAlert, Cpu, Sparkles } from 'lucide-react';

const ANALYSIS_STEPS = [
  { icon: Search, title: "알고리즘 레이더 조준 중...", detail: "인스타그램 빅데이터 패턴을 정밀 스캔하고 있습니다." },
  { icon: ShieldAlert, title: "비밀 저장함 & 좋아요 교차 검증 중...", detail: "남에게 보여주지 않는 당신의 음침한/비밀 취향을 추적 중입니다." },
  { icon: Cpu, title: "무의식 이상형 계정 딥 파싱 중...", detail: "가장 오래 머물고 상호작용한 계정들의 공통 패턴을 계산합니다." },
  { icon: Sparkles, title: "Meta 광고 타겟팅 카테고리 폭로 중...", detail: "알고리즘이 당신에게 부여한 타겟팅 카테고리를 추출하고 있습니다." }
];

export default function LoadingSection() {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [progress, setProgress] = useState(15);

  useEffect(() => {
    // Step text relay timer
    const stepInterval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < ANALYSIS_STEPS.length - 1) return prev + 1;
        return prev;
      });
    }, 1500);

    // Progress bar smooth animation with fallback creep
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 90) {
          const stepAdd = Math.floor(Math.random() * 8) + 4;
          return Math.min(prev + stepAdd, 90);
        } else if (prev < 99) {
          // Creep smoothly towards 99%
          return prev + 1;
        }
        return prev;
      });
    }, 300);

    return () => {
      clearInterval(stepInterval);
      clearInterval(progressInterval);
    };
  }, []);

  const CurrentIcon = ANALYSIS_STEPS[currentStepIndex].icon;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '3rem 1rem',
      textAlign: 'center',
      minHeight: '65vh'
    }}>
      {/* Detective Profile Graphic Banner */}
      <div style={{ position: 'relative', width: '220px', height: '220px', marginBottom: '2rem' }}>
        <div style={{
          position: 'absolute',
          top: '-10px',
          left: '-10px',
          right: '-10px',
          bottom: '-10px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(131,58,180,0.5) 0%, rgba(253,29,29,0.3) 50%, rgba(252,176,69,0) 80%)',
          animation: 'pulse 2s infinite ease-in-out'
        }} />
        
        <img 
          src="/detective.png" 
          alt="Detective Profiler Scanner" 
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            borderRadius: '24px',
            border: '2px solid rgba(253, 29, 45, 0.4)',
            boxShadow: '0 0 30px rgba(131, 58, 180, 0.5)'
          }}
        />

        <div style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          borderRadius: '24px',
          background: 'linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(253,29,29,0.2) 50%, rgba(255,255,255,0) 100%)',
          backgroundSize: '100% 200%',
          animation: 'scan 2s infinite linear',
          pointerEvents: 'none'
        }} />
      </div>

      {/* Main Loading Status Header */}
      <div className="glass-card" style={{ maxWidth: '580px', width: '100%', padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.8rem', marginBottom: '1rem' }}>
          <CurrentIcon size={28} color="#fcb045" style={{ animation: 'spin-slow 4s infinite linear' }} />
          <h2 className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: '800' }}>
            {ANALYSIS_STEPS[currentStepIndex].title}
          </h2>
        </div>

        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1.8rem', lineHeight: '1.5' }}>
          {ANALYSIS_STEPS[currentStepIndex].detail}
        </p>

        {/* Custom Neon Progress Bar */}
        <div style={{
          width: '100%',
          height: '12px',
          background: 'rgba(255,255,255,0.06)',
          borderRadius: '10px',
          overflow: 'hidden',
          border: '1px solid rgba(255,255,255,0.1)',
          position: 'relative'
        }}>
          <div style={{
            width: `${progress}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%)',
            borderRadius: '10px',
            transition: 'width 0.3s ease-out',
            boxShadow: '0 0 15px rgba(253, 29, 29, 0.8)'
          }} />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.8rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          <span>탐정 파싱 프로세스</span>
          <span style={{ fontWeight: '700', color: '#fcb045' }}>{progress}%</span>
        </div>
      </div>
    </div>
  );
}
