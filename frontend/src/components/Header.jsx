import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function Header() {
  return (
    <header className="header-nav">
      <div className="logo">
        <span className="gradient-text">Insta Taste Recommender</span>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginLeft: '0.6rem', fontWeight: '400' }}>
          인스타 취향 분석 추천기
        </span>
      </div>
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <span className="badge badge-mild">
          <ShieldCheck size={14} /> 안전한 데이터 분석 및 보관
        </span>
      </div>
    </header>
  );
}
