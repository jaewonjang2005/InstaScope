import React from 'react';
import { Sparkles, Instagram, ShieldCheck } from 'lucide-react';

export default function Header() {
  return (
    <header className="header-nav">
      <div className="logo">
        <span className="gradient-text">InstaScope</span>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginLeft: '0.6rem', fontWeight: '400' }}>
          인스타그램 데이터 프로파일러
        </span>
      </div>
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <span className="badge badge-mild">
          <ShieldCheck size={14} /> 100% 임시저장 / 분석후 즉시삭제
        </span>
      </div>
    </header>
  );
}
