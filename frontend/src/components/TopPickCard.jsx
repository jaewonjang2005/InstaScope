import React from 'react';
import { Heart, Bookmark, Eye, ThumbsUp, ExternalLink } from 'lucide-react';

export default function TopPickCard({ pick }) {
  return (
    <div className="glass-card" style={{ padding: '3rem 2rem', textAlign: 'center', marginBottom: '2rem', position: 'relative', overflow: 'hidden' }}>
      <div style={{
        position: 'absolute', top: '-50%', left: '-50%', width: '200%', height: '200%',
        background: 'radial-gradient(circle, rgba(255,107,107,0.1) 0%, rgba(0,0,0,0) 50%)',
        zIndex: 0, pointerEvents: 'none'
      }}></div>
      
      <div style={{ position: 'relative', zIndex: 1 }}>
        <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-color)', marginBottom: '1rem', letterSpacing: '2px' }}>
          👑 TOP 1 PICK
        </h3>
        <h1 style={{ fontSize: '3rem', marginBottom: '0.5rem', background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          @{pick.username}
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginBottom: '2rem' }}>
          총 상호작용 점수: {pick.score.toLocaleString()}점
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2.5rem' }}>
          <StatBox icon={<Heart size={24} color="#ff6b6b" />} label="좋아요" value={pick.likes_count} />
          <StatBox icon={<Bookmark size={24} color="#fca048" />} label="비밀 저장" value={pick.saves_count} />
          <StatBox icon={<Eye size={24} color="#a06bff" />} label="스토리 시청" value={pick.story_views_count} />
          <StatBox icon={<ThumbsUp size={24} color="#48a0fc" />} label="스토리 반응" value={pick.story_likes_count} />
        </div>

        {pick.sample_url && (
          <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1.5rem', borderRadius: '15px', textAlign: 'left' }}>
            <h4 style={{ color: 'var(--text-muted)', marginBottom: '0.8rem', fontSize: '0.9rem' }}>최근 상호작용한 게시물</h4>
            <p style={{ fontStyle: 'italic', color: '#ddd', marginBottom: '1rem', lineHeight: '1.5' }}>
              "{pick.sample_caption || '캡션 없음'}"
            </p>
            <a 
              href={pick.sample_url} 
              target="_blank" 
              rel="noreferrer"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary-color)', textDecoration: 'none', fontWeight: 'bold' }}
            >
              인스타그램에서 보기 <ExternalLink size={16} />
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

function StatBox({ icon, label, value }) {
  return (
    <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '15px', border: '1px solid rgba(255,255,255,0.1)' }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '0.5rem' }}>{icon}</div>
      <div style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.2rem' }}>{value.toLocaleString()}</div>
      <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{label}</div>
    </div>
  );
}
