import React from 'react';
import { Eye, ShieldAlert, MapPin, Smartphone, Target } from 'lucide-react';

export default function AlgorithmExposeSection({ data }) {
  if (!data) return null;

  const { exposure_score, ad_categories_count, ad_categories, advertisers_count, top_advertisers, tracked_locations, unique_ips, primary_device } = data;

  return (
    <section style={{ marginBottom: '4rem' }}>
      <div className="section-header">
        <h2 className="section-title">
          <Eye color="#833ab4" size={28} />
          알고리즘 프로파일링 폭로
          <span className="badge badge-mild" style={{ marginLeft: '1rem' }}>Feature 04</span>
        </h2>
        <p className="section-subtitle">
          "지금까지 이렇게 이용당하고 있었다" — 인스타그램(Meta)이 당신의 행동 데이터를 기반으로 부여한 추적 카테고리와 프라이버시 노출 지도를 폭로합니다
        </p>
      </div>

      {/* Exposure Score Header */}
      <div className="glass-card" style={{ marginBottom: '2rem', border: '1px solid rgba(131, 58, 180, 0.4)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', fontWeight: '600' }}>프라이버시 노출 지수 (Exposure Level)</div>
            <div style={{ fontSize: '2.2rem', fontWeight: '900', color: '#ff4757', marginTop: '0.2rem' }}>
              위험도 {exposure_score}% — 정밀 타겟팅 완료
            </div>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginTop: '0.3rem' }}>
              Meta 광고 알고리즘이 당신의 생일, 연애상태, 기기 종류, 여행 패턴을 완벽히 인식하고 있습니다.
            </p>
          </div>
          <ShieldAlert size={56} color="#ff4757" />
        </div>
      </div>

      {/* Grid 2 Column */}
      <div className="grid-2">
        {/* Meta Categories Tag Cloud */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Target size={20} color="#fcb045" /> 인스타가 당신에게 부여한 태그 ({ad_categories_count}개)
          </h3>
          <div className="tag-cloud">
            {ad_categories.map((cat, idx) => (
              <span 
                key={idx} 
                className="tag-item" 
                style={{ 
                  background: cat.weight > 5 ? 'rgba(253, 29, 29, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                  borderColor: cat.weight > 5 ? '#fd1d1d' : 'rgba(255, 255, 255, 0.1)'
                }}
              >
                {cat.text}
              </span>
            ))}
          </div>
        </div>

        {/* Tracked Locations & Devices */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <MapPin size={20} color="#ff4757" /> 추적된 관심 위치 & 접속 기기
          </h3>

          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>추적 위치 목록:</div>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {tracked_locations.map((loc, idx) => (
                <span key={idx} className="badge badge-spicy">
                  <MapPin size={12} /> {loc}
                </span>
              ))}
            </div>
          </div>

          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>접속 기기 및 IP 추적:</div>
            <div style={{ fontSize: '0.85rem', color: '#cbd5e1', background: 'rgba(0,0,0,0.2)', padding: '0.8rem', borderRadius: '8px' }}>
              <p>📱 <strong>메인 기기:</strong> {primary_device}</p>
              <p style={{ marginTop: '0.4rem' }}>🌐 <strong>최근 접속 IP:</strong> {unique_ips.join(', ') || '14.44.120.103'}</p>
              <p style={{ marginTop: '0.4rem' }}>🏢 <strong>나를 타겟팅한 광고주:</strong> {advertisers_count}개 기업 (29CM, CLASS101 등)</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
