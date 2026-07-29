import React from 'react';
import { Radar, Bar } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  RadialLinearScale, 
  PointElement, 
  LineElement, 
  Filler, 
  Tooltip, 
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js';
import { Flame, Compass, Clock, Hash } from 'lucide-react';

ChartJS.register(
  RadialLinearScale, 
  PointElement, 
  LineElement, 
  Filler, 
  Tooltip, 
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

export default function TasteDnaSection({ data }) {
  if (!data) return null;

  const { spicy_score, spicy_level, spicy_desc, radar_data, top_hashtags, time_distribution, interaction_pyramid } = data;

  // Radar Chart Data
  const radarChartData = {
    labels: radar_data.map(r => r.category),
    datasets: [
      {
        label: '취향 몰입도',
        data: radar_data.map(r => r.score),
        backgroundColor: 'rgba(253, 29, 29, 0.25)',
        borderColor: '#fd1d1d',
        borderWidth: 2,
        pointBackgroundColor: '#fcb045',
      }
    ]
  };

  const radarOptions = {
    scales: {
      r: {
        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        pointLabels: { color: '#f8fafc', font: { size: 13, weight: 'bold' } },
        ticks: { display: false }
      }
    },
    plugins: { legend: { display: false } }
  };

  // Time Distribution Data (Hourly)
  const timeLabels = Object.keys(time_distribution || {});
  const timeValues = Object.values(time_distribution || {});

  const barChartData = {
    labels: timeLabels.map(h => `${h}시`),
    datasets: [
      {
        label: '활동 횟수',
        data: timeValues,
        backgroundColor: timeLabels.map(h => {
          const hour = parseInt(h);
          if (hour >= 0 && hour < 6) return '#ff4757'; // Dawn (Red)
          if (hour >= 18) return '#833ab4'; // Night (Purple)
          return '#fcb045'; // Day (Orange)
        }),
        borderRadius: 4
      }
    ]
  };

  const barOptions = {
    scales: {
      x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
      y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
    },
    plugins: { legend: { display: false } }
  };

  return (
    <section>
      <div className="section-header">
        <h2 className="section-title">
          <Flame color="#fd1d1d" size={28} />
          취향 DNA 리포트
          <span className="badge badge-fire" style={{ marginLeft: '1rem' }}>Feature 01</span>
        </h2>
        <p className="section-subtitle">
          상호작용 데이터, 해시태그 분석, 소비 시간대를 결합하여 추론한 당신의 진짜 취향 스펙트럼
        </p>
      </div>

      {/* Spicy Gauge Banner */}
      <div className="glass-card" style={{ marginBottom: '2rem', background: 'linear-gradient(135deg, rgba(131,58,180,0.15), rgba(253,29,29,0.15))' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div>
            <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: '600' }}>취향 매운맛 측정기</div>
            <div style={{ fontSize: '2.2rem', fontWeight: '900', marginTop: '0.2rem' }} className="gradient-text">
              {spicy_level}
            </div>
            <p style={{ marginTop: '0.4rem', color: '#e2e8f0', fontSize: '0.95rem' }}>{spicy_desc}</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '3.5rem', fontWeight: '900', color: '#ff4757', lineHeight: '1' }}>
              {spicy_score}<span style={{ fontSize: '1.5rem' }}>점</span>
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>스펙트럼: 순한맛 0 ↔ 100 불닭</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div style={{ width: '100%', height: '12px', background: 'rgba(255,255,255,0.1)', borderRadius: '999px', marginTop: '1.5rem', overflow: 'hidden' }}>
          <div 
            style={{ 
              width: `${spicy_score}%`, 
              height: '100%', 
              background: 'var(--insta-gradient)', 
              borderRadius: '999px',
              transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1)' 
            }} 
          />
        </div>
      </div>

      {/* Grid 2 Column */}
      <div className="grid-2">
        {/* Radar Chart */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Compass size={20} color="#fcb045" /> 카테고리별 취향 분포 (Radar)
          </h3>
          <div style={{ padding: '1rem 0' }}>
            <Radar data={radarChartData} options={radarOptions} />
          </div>
        </div>

        {/* Time Distribution */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Clock size={20} color="#833ab4" /> 시간대별 인스타 소비 히트맵
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            🔴 빨간색 바는 00시~06시 새벽 심야 활동을 나타냅니다.
          </p>
          <div style={{ height: '230px' }}>
            <Bar data={barChartData} options={barOptions} />
          </div>
        </div>
      </div>

      {/* Top Hashtags & Interaction Pyramid */}
      <div className="grid-2" style={{ marginTop: '1.75rem' }}>
        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Hash size={20} color="#fd1d1d" /> 최다 반응 해시태그 TOP 15
          </h3>
          <div className="tag-cloud">
            {top_hashtags.map((tag, idx) => (
              <span key={idx} className="tag-item">
                #{tag.tag} <strong style={{ color: '#fcb045', marginLeft: '0.2rem' }}>{tag.count}</strong>
              </span>
            ))}
          </div>
        </div>

        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1.5rem' }}>
            📊 상호작용 깊이 (Interaction Pyramid)
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
            {interaction_pyramid.map((step, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(255,255,255,0.03)', padding: '0.8rem 1.2rem', borderRadius: 'var(--radius-md)' }}>
                <span style={{ fontWeight: '600' }}>{step.stage}</span>
                <span style={{ fontWeight: '800', color: '#fcb045', fontSize: '1.1rem' }}>{step.count.toLocaleString()}회</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
