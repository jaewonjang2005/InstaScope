import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Recommendations from '../components/Recommendations';
import confetti from 'canvas-confetti';
import { Flame, ArrowLeft, Skull } from 'lucide-react';

export default function SecretPickPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state;
  const [isSpicyMode, setIsSpicyMode] = useState(false);

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
        colors: isSpicyMode ? ['#990000', '#ff0000', '#000000'] : ['#ff0000', '#ff6b6b', '#111111']
      });
    } catch (e) {
      console.log('Confetti error:', e);
    }
  }, [data, navigate, isSpicyMode]);

  if (!data) return null;

  const { hidden_recommendations, hidden_keywords, spicy_recommendations, raw_hidden_tags } = data;

  let currentKeywords = hidden_keywords;
  let currentRecommendations = hidden_recommendations;

  if (isSpicyMode && raw_hidden_tags?.length > 0) {
    currentKeywords = raw_hidden_tags;
    currentRecommendations = spicy_recommendations;
  }

  return (
    <div className="fade-in" style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '2rem' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
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
            fontSize: '1rem'
          }}
        >
          <ArrowLeft size={20} /> 돌아가기
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span style={{ 
            color: isSpicyMode ? '#ff0000' : 'var(--text-muted)', 
            fontWeight: 'bold', 
            fontSize: '0.9rem',
            transition: 'color 0.3s ease'
          }}>
            매운맛 🔥
          </span>
          <label style={{
            position: 'relative',
            display: 'inline-block',
            width: '50px',
            height: '24px'
          }}>
            <input 
              type="checkbox" 
              checked={isSpicyMode} 
              onChange={() => setIsSpicyMode(!isSpicyMode)} 
              style={{ opacity: 0, width: 0, height: 0 }} 
            />
            <span style={{
              position: 'absolute',
              cursor: 'pointer',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: isSpicyMode ? '#ff0000' : 'rgba(255,107,107,0.2)',
              transition: '.4s',
              borderRadius: '24px'
            }}>
              <span style={{
                position: 'absolute',
                content: '""',
                height: '16px',
                width: '16px',
                left: isSpicyMode ? '30px' : '4px',
                bottom: '4px',
                backgroundColor: 'white',
                transition: '.4s',
                borderRadius: '50%',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
              }} />
            </span>
          </label>
        </div>
      </div>

      <div style={{
        background: isSpicyMode ? 'rgba(255, 0, 0, 0.05)' : 'rgba(255, 107, 107, 0.03)',
        border: `1px solid ${isSpicyMode ? 'rgba(255, 0, 0, 0.2)' : 'rgba(255, 107, 107, 0.1)'}`,
        borderRadius: '20px',
        padding: '2rem',
        marginBottom: '2rem',
        boxShadow: isSpicyMode ? '0 10px 30px rgba(255, 0, 0, 0.1)' : '0 10px 30px rgba(255, 107, 107, 0.05)',
        transition: 'all 0.5s ease',
        textAlign: 'center'
      }}>
        <h2 style={{ fontSize: '1.4rem', color: isSpicyMode ? '#ff3333' : '#ff6b6b', marginBottom: '1rem', fontWeight: 500 }}>
          {isSpicyMode ? <Skull size={28} style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} /> : <Flame size={28} style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} />}
          {isSpicyMode ? '당신의 진짜 매운맛 취향 (Spicy Pick)' : '당신의 진짜 서브 취향 (Secret Pick)'}
        </h2>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, backgroundImage: isSpicyMode ? 'linear-gradient(to right, #ff0000, #cc0000)' : 'linear-gradient(to right, #ff6b6b, #ff8e53)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', margin: 0 }}>
          {currentKeywords?.[0] ? `#${currentKeywords[0]}` : '비밀의 방'}
        </h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '1rem', lineHeight: '1.6' }}>
          {isBuldakMode
            ? '안전장치 해제. 오직 순도 100% 19금/노출 관련 키워드만을 섬세하게 필터링하여 보여줍니다.'
            : (isSpicyMode 
            ? '수학적 분석을 걷어내고, 인스타그램에서 당신이 남몰래 주시하고 있는 본능적이고 원초적인 19금/서브컬처 키워드만을 적나라하게 보여줍니다.' 
            : '주된 취향은 아니지만, 은밀하게 혹은 무의식적으로 강하게 주시하고 있는 당신의 또 다른 취향입니다.')}
        </p>
      </div>

      <div className="glass-card" style={{ marginBottom: '2rem', padding: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>{isBuldakMode ? '적발된 불닭맛 취향 키워드' : (isSpicyMode ? '적발된 매운맛 취향 키워드' : '발견된 서브 취향 키워드')}</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', justifyContent: 'center' }}>
          {currentKeywords?.map((kw, i) => (
             <span key={`hidden-${i}`} className="badge" style={{ padding: '0.4rem 0.8rem', background: isBuldakMode ? 'rgba(139,0,0,0.2)' : (isSpicyMode ? 'rgba(255,0,0,0.2)' : 'rgba(255,100,100,0.1)'), color: isBuldakMode ? '#8B0000' : (isSpicyMode ? '#ff3333' : '#ff8e53'), borderRadius: '20px' }}>#{kw}</span>
          ))}
          {(!currentKeywords || currentKeywords.length === 0) && (
            <span style={{ color: 'var(--text-muted)' }}>특별한 취향 태그가 없습니다.</span>
          )}
        </div>
      </div>

      <Recommendations 
        title={isBuldakMode ? "Buldak Pick 추천 콘텐츠" : (isSpicyMode ? "Spicy Pick 추천 콘텐츠" : "Secret Pick 추천 콘텐츠")} 
        items={currentRecommendations} 
        icon={isBuldakMode ? <span style={{fontSize: '24px'}}>🌶️</span> : (isSpicyMode ? <Skull size={24} color="#ff3333" /> : <Flame size={24} color="#ff6b6b" />)} 
        colorClass="hidden-glow"
        emptyMessage="이 취향과 관련된 콘텐츠를 충분히 찾지 못했습니다."
      />
    </div>
  );
}
