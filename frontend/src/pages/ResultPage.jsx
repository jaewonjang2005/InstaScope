import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Recommendations from '../components/Recommendations';
import confetti from 'canvas-confetti';
import { RefreshCw, Hash, Flame } from 'lucide-react';

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

  const { keywords, sfw_recommendations, nsfw_recommendations } = data;
  const totalTags = keywords?.total_tags_found || 0;

  return (
    <div className="fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
          분석 완료! 당신의 <span className="highlight">인스타 취향 추천</span>은...
        </h2>
        <p style={{ color: 'var(--text-muted)' }}>
          총 {totalTags.toLocaleString()}개의 태그 및 키워드를 분석한 결과입니다.
        </p>
      </div>
      
      <div className="glass-card" style={{ marginBottom: '2rem', padding: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>추출된 핵심 취향 키워드</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', justifyContent: 'center' }}>
          {keywords?.search_sfw_queries?.map((kw, i) => (
             <span key={`sfw-${i}`} className="badge" style={{ padding: '0.4rem 0.8rem', background: 'rgba(255,255,255,0.1)', borderRadius: '20px' }}>#{kw}</span>
          ))}
          {keywords?.search_nsfw_queries?.map((kw, i) => (
             <span key={`nsfw-${i}`} className="badge" style={{ padding: '0.4rem 0.8rem', background: 'rgba(255,100,100,0.1)', color: '#ff8e53', borderRadius: '20px' }}>#{kw}</span>
          ))}
        </div>
      </div>

      <Recommendations 
        title="일반 맞춤 추천 (SFW)" 
        items={sfw_recommendations} 
        icon={<Hash size={24} />} 
        colorClass="sfw-glow"
      />

      <Recommendations 
        title="은밀한 취향 추천 (NSFW/우회됨)" 
        items={nsfw_recommendations} 
        icon={<Flame size={24} color="#ff6b6b" />} 
        colorClass="nsfw-glow"
      />

      <div style={{ textAlign: 'center', marginTop: '3rem' }}>
        <button 
          className="gradient-btn"
          style={{ padding: '1rem 2rem', fontSize: '1.1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}
          onClick={() => navigate('/')}
        >
          <RefreshCw size={18} /> 다른 계정 데이터로 다시 분석하기
        </button>
      </div>
    </div>
  );
}
