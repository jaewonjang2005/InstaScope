import React from 'react';

export default function RunnerUpList({ runners }) {
  return (
    <div className="card fade-in" style={{ padding: '2rem' }}>
      <h3 style={{ fontSize: '1.2rem', marginBottom: '1.5rem', color: 'var(--text-muted)' }}>
        🥈 아쉽게 1위를 놓친 계정들
      </h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {runners.map((runner, index) => (
          <div key={runner.username} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '1rem 1.5rem', background: 'rgba(255,255,255,0.03)',
            borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ 
                width: '30px', height: '30px', borderRadius: '50%', 
                background: 'rgba(255,255,255,0.1)', display: 'flex', 
                alignItems: 'center', justifyContent: 'center',
                fontWeight: 'bold', color: 'var(--text-muted)'
              }}>
                {index + 2}
              </div>
              <div style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>@{runner.username}</div>
            </div>
            
            <div style={{ textAlign: 'right' }}>
              <div style={{ color: 'var(--primary-color)', fontWeight: 'bold' }}>
                {runner.score.toLocaleString()}점
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                저장 {runner.saves_count} · 좋아요 {runner.likes_count}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
