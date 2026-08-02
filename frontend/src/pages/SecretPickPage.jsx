import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Recommendations from '../components/Recommendations';
import confetti from 'canvas-confetti';
import { Flame, ArrowLeft } from 'lucide-react';

export default function SecretPickPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state;

  useEffect(() => {
    if (!data) {
      navigate('/');
      return;
    }

    try {
      confetti({
        particleCount: 100,
        spread: 120,
        origin: { y: 0.5 },
        colors: ['#ff0000', '#ff6b6b', '#111111']
      });
    } catch (e) {
      console.log('Confetti error:', e);
    }
  }, [data, navigate]);

  if (!data) return null;

  const { hidden_recommendations, hidden_keywords } = data;

  return (
    <div className="fade-in" style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '2rem' }}>
      
      <button 
        onClick={() => navigate(-1)}
        style={{ 
          background: 'none', 
          border: 'none', 
          color: 'var(--text-muted)', 
          display: 'flex', 
          alignItems: 'center', 
          gap: '0.5rem', 
          cursor: 'pointer',
          marginBottom: '2rem',
          fontSize: '1rem'
        }}
      >
        <ArrowLeft size={20} /> 돌아가기
      </button>

      <div style={{ textAlign: 'center', marginBottom: '3rem', padding: '2rem', background: 'rgba(255,107,107,0.05)', borderRadius: '24px', border: '1px solid rgba(255,107,107,0.2)' }}>
        <h2 style={{ fontSize: '1.4rem', color: '#ff6b6b', marginBottom: '1rem', fontWeight: 500 }}>
          <Flame size={28} style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} />
          당신의 진짜 서브 취향 (Secret Pick)
        </h2>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, background: 'linear-gradient(to right, #ff6b6b, #ff8e53)', WebkitBackgroundClip: 'text', color: 'transparent', margin: 0 }}>
          {hidden_keywords?.[0] ? `#${hidden_keywords[0]}` : '비밀의 방'}
        </h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '1rem', lineHeight: '1.6' }}>
          주된 취향은 아니지만, 은밀하게 혹은 무의식적으로 강하게 주시하고 있는 당신의 또 다른 취향입니다.<br/>
          최근 인스타그램 알고리즘이 당신을 위해 주목하고 있는 주제들입니다.
        </p>
      </div>

      <div className="glass-card" style={{ marginBottom: '2rem', padding: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>발견된 서브 취향 키워드</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', justifyContent: 'center' }}>
          {hidden_keywords?.map((kw, i) => (
             <span key={`hidden-${i}`} className="badge" style={{ padding: '0.4rem 0.8rem', background: 'rgba(255,100,100,0.1)', color: '#ff8e53', borderRadius: '20px' }}>#{kw}</span>
          ))}
          {(!hidden_keywords || hidden_keywords.length === 0) && (
            <span style={{ color: 'var(--text-muted)' }}>특별한 서브 취향 태그가 없습니다.</span>
          )}
        </div>
      </div>

      <Recommendations 
        title="Secret Pick 추천 콘텐츠" 
        items={hidden_recommendations} 
        icon={<Flame size={24} color="#ff6b6b" />} 
        colorClass="hidden-glow"
        emptyMessage="이 취향과 관련된 콘텐츠를 충분히 찾지 못했습니다."
      />
    </div>
  );
}
