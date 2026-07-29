import React from 'react';
import { HeartHandshake, UserCheck, ExternalLink, Sparkles, Star } from 'lucide-react';

export default function IdealTypeSection({ data }) {
  if (!data) return null;

  const { top_ideal_type_candidates, top_close_friends, top_favorite_creators, recommended_posts } = data;

  return (
    <section>
      <div className="section-header">
        <h2 className="section-title">
          <HeartHandshake color="#ff4757" size={28} />
          이상형 계정 & 게시물 추천
          <span className="badge badge-fire" style={{ marginLeft: '1rem' }}>MAIN FEATURE</span>
        </h2>
        <p className="section-subtitle">
          좋아요, 저장, 스토리 반응, 탐색 이력을 종합하여 당신이 무의식적으로 가장 인상 깊게 본 이상형 프로필과 맞춤 콘텐츠를 도출합니다
        </p>
      </div>

      {/* Top Ideal Type Candidates List */}
      <div className="glass-card" style={{ marginBottom: '2rem', border: '1px solid rgba(255, 71, 87, 0.3)' }}>
        <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Sparkles color="#ff4757" size={22} />
          당신의 무의식 알고리즘이 가리키는 <span className="gradient-text">이상형 관심 프로필 TOP 10</span>
        </h3>

        <div className="grid-2">
          {top_ideal_type_candidates.map((account, idx) => (
            <div key={idx} className="profile-card">
              <div className="avatar-circle">
                {idx + 1}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontWeight: '800', fontSize: '1.1rem', color: '#f8fafc' }}>
                    @{account.username}
                  </span>
                  <span className="badge badge-fire">관심점수 {account.score}점</span>
                </div>
                <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginTop: '0.3rem', display: 'flex', gap: '0.8rem', flexWrap: 'wrap' }}>
                  <span>좋아요 {account.likes_count}</span>
                  <span>저장 {account.saves_count}</span>
                  <span>스토리반응 {account.story_likes_count}</span>
                </div>
                {account.sample_url && (
                  <a 
                    href={account.sample_url} 
                    target="_blank" 
                    rel="noreferrer" 
                    style={{ color: '#fcb045', fontSize: '0.8rem', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.2rem', marginTop: '0.4rem' }}
                  >
                    대표 관심 게시물 보기 <ExternalLink size={12} />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Posts Section */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Star color="#fcb045" size={22} />
          취향 맞춤 추천 게시물 타임라인
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
          당신이 높은 반응을 보였거나 은밀히 저장해둔 카테고리 중 가장 인상적인 콘텐츠입니다.
        </p>

        <div className="grid-2">
          {recommended_posts.map((post, idx) => (
            <div key={idx} className="post-recommend-card">
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem' }}>
                  <span style={{ fontWeight: '700', color: '#fcb045' }}>@{post.owner}</span>
                  <span className="badge badge-spicy">추천</span>
                </div>
                <p style={{ fontSize: '0.9rem', color: '#e2e8f0', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {post.caption || '인스타그램 콘텐츠 캡션 내용'}
                </p>
                <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginTop: '0.8rem' }}>
                  {post.hashtags.map((tag, tIdx) => (
                    <span key={tIdx} style={{ fontSize: '0.75rem', color: '#94a3b8', background: 'rgba(255,255,255,0.05)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
              <div style={{ marginTop: '1rem', textAlign: 'right' }}>
                <a 
                  href={post.url} 
                  target="_blank" 
                  rel="noreferrer" 
                  className="gradient-btn"
                  style={{ padding: '0.4rem 1rem', fontSize: '0.8rem' }}
                >
                  게시물 방문하기 <ExternalLink size={14} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
