import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import TopPickCard from '../components/TopPickCard';
import RunnerUpList from '../components/RunnerUpList';
import confetti from 'canvas-confetti';
import { RefreshCw } from 'lucide-react';

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

  const { top_pick, runner_ups, total_accounts_interacted } = data;

  return (
    <div className="fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
          분석 완료! 당신의 <span className="highlight">최애 계정</span>은...
        </h2>
        <p style={{ color: 'var(--text-muted)' }}>
          총 {total_accounts_interacted.toLocaleString()}개의 상호작용 계정 중 1위
        </p>
      </div>

      {top_pick ? (
        <TopPickCard pick={top_pick} />
      ) : (
        <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
          <p>충분한 데이터가 없어 1픽을 선정하지 못했습니다.</p>
        </div>
      )}

      {runner_ups && runner_ups.length > 0 && (
        <RunnerUpList runners={runner_ups} />
      )}

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
