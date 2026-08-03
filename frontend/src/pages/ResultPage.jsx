import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Recommendations from '../components/Recommendations';
import confetti from 'canvas-confetti';
import { RefreshCw, Hash, Flame, Sparkles } from 'lucide-react';

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state?.data;

  useEffect(() => {
    if (!data) {
      navigate('/');
      return;
    }

    try {
      confetti({
        particleCount: 150,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#ff6b6b', '#ff8e53', '#fca048']
      });
    } catch (e) {
      console.log('Confetti error:', e);
    }
  }, [data, navigate]);

  if (!data) return null;

  const { keywords, sfw_recommendations, hidden_recommendations } = data;
  const totalTags = keywords?.total_tags_found || 0;

  const topKeyword = keywords?.search_sfw_queries?.[0] || '탐험가';
  
  return (
    <div className="fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem', padding: '2rem', background: 'rgba(255,255,255,0.02)', borderRadius: '24px', border: '1px solid rgba(255,255,255,0.05)' }}>
        <h2 style={{ fontSize: '1.4rem', color: 'var(--text-muted)', marginBottom: '1rem', fontWeight: 500 }}>
          분석 완료! 당신의 인스타 자아는...
        </h2>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem', letterSpacing: '-1px' }}>
          <span className="gradient-text">#{topKeyword}</span> 마니아
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
          총 {totalTags.toLocaleString()}개의 흔적을 분석해 맞춤 콘텐츠를 찾았습니다.
        </p>
      </div>
      
      <div className="glass-card" style={{ marginBottom: '2rem', padding: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>추출된 핵심 취향 키워드</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', justifyContent: 'center' }}>
          {keywords?.search_sfw_queries?.map((kw, i) => (
             <span key={`sfw-${i}`} className="badge" style={{ padding: '0.4rem 0.8rem', background: 'rgba(255,255,255,0.1)', borderRadius: '20px' }}>#{kw}</span>
          ))}
        </div>
      </div>

      <Recommendations 
        title="맞춤 추천" 
        items={sfw_recommendations} 
        icon={<Sparkles size={24} color="#fcb045" />} 
        colorClass="sfw-glow"
        emptyMessage="일반 취향 키워드를 충분히 찾지 못했습니다. 더 많은 인스타 활동이 필요해요!"
      />

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
        <button 
          onClick={() => navigate('/secret', { 
            state: { 
              hidden_recommendations: hidden_recommendations,
              hidden_keywords: keywords?.search_hidden_queries,
              spicy_recommendations: data.spicy_recommendations,
              raw_hidden_tags: keywords?.raw_hidden_tags,
              buldak_recommendations: data.buldak_recommendations,
              buldak_tags: keywords?.buldak_tags
            } 
          })}
          className="glass-card"
          style={{ 
            padding: '1.2rem 2.5rem', 
            fontSize: '1.2rem', 
            fontWeight: 'bold',
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '0.8rem', 
            cursor: 'pointer', 
            border: '1px solid rgba(255,107,107,0.4)', 
            background: 'linear-gradient(45deg, rgba(255,107,107,0.1), rgba(255,142,83,0.1))',
            color: '#ff8e53',
            borderRadius: '50px',
            boxShadow: '0 4px 15px rgba(255, 107, 107, 0.2)'
          }}
        >
          <Flame size={24} color="#ff6b6b" /> 당신의 진짜 숨겨진 취향 확인하기 🔒
        </button>
      </div>

      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '3.5rem' }}>
        <button 
          className="glass-card"
          style={{ padding: '1rem 2rem', fontSize: '1.1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', border: '1px solid rgba(255,255,255,0.2)', color: '#fff' }}
          onClick={() => {
            navigator.clipboard.writeText(window.location.href);
            alert('결과 페이지 링크가 복사되었습니다!');
          }}
        >
          🔗 결과 공유하기
        </button>
        <button 
          className="gradient-btn"
          style={{ padding: '1rem 2rem', fontSize: '1.1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}
          onClick={() => navigate('/')}
        >
          <RefreshCw size={18} /> 다시 테스트하기
        </button>
      </div>
    </div>
  );
}
