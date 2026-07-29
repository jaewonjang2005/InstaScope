import React from 'react';
import { Lock, Bookmark, Heart, FolderArchive, Sparkles } from 'lucide-react';

export default function SecretCollectionSection({ data }) {
  if (!data) return null;

  const { total_saved, total_liked, secret_posts_count, secret_ratio_percentage, secret_hashtags, collections } = data;

  return (
    <section>
      <div className="section-header">
        <h2 className="section-title">
          <Lock color="#fcb045" size={28} />
          비밀 컬렉션 해부
          <span className="badge badge-spicy" style={{ marginLeft: '1rem' }}>Feature 02</span>
        </h2>
        <p className="section-subtitle">
          저장은 했지만 타인에게 들키지 않기 위해 좋아요는 안 누른 은밀한 게시물과 비공개 컬렉션을 해부합니다
        </p>
      </div>

      {/* Hero Stats */}
      <div className="grid-3" style={{ marginBottom: '2rem' }}>
        <div className="glass-card" style={{ textAlign: 'center', padding: '1.75rem' }}>
          <Bookmark size={32} color="#fcb045" style={{ margin: '0 auto 0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: '800', color: '#f8fafc' }}>{total_saved.toLocaleString()}개</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>총 저장한 게시물 수</div>
        </div>

        <div className="glass-card" style={{ textAlign: 'center', padding: '1.75rem', borderColor: 'rgba(255, 71, 87, 0.4)' }}>
          <Lock size={32} color="#ff4757" style={{ margin: '0 auto 0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: '800', color: '#ff4757' }}>{secret_posts_count.toLocaleString()}개</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>저장 O + 좋아요 X (비밀 저장)</div>
        </div>

        <div className="glass-card" style={{ textAlign: 'center', padding: '1.75rem' }}>
          <Sparkles size={32} color="#833ab4" style={{ margin: '0 auto 0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: '800' }} className="gradient-text">{secret_ratio_percentage}%</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>비밀 취향 은닉 비율</div>
        </div>
      </div>

      {/* Secret Taste Hashtags */}
      <div className="glass-card" style={{ marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Heart size={20} color="#ff4757" /> 비밀 저장 게시물 속에 숨겨진 관심 키워드
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
          피드에는 좋아요를 누르지 않았지만 비밀스럽게 저장만 해둔 콘텐츠의 주요 해시태그입니다.
        </p>
        <div className="tag-cloud">
          {secret_hashtags.map((tag, idx) => (
            <span key={idx} className="tag-item" style={{ background: 'rgba(253, 29, 29, 0.1)', borderColor: 'rgba(253, 29, 29, 0.3)' }}>
              #{tag.tag} <strong style={{ color: '#ff4757', marginLeft: '0.3rem' }}>{tag.count}</strong>
            </span>
          ))}
        </div>
      </div>

      {/* Collections List */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FolderArchive size={20} color="#833ab4" /> 사용자 비밀 컬렉션 분류 ({collections.length}개)
        </h3>

        <div className="grid-3">
          {collections.map((col, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: '700', fontSize: '1.05rem', color: '#fcb045' }}>{col.name}</span>
                <span className="badge badge-spicy">{col.privacy}</span>
              </div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.8rem' }}>
                저장된 콘텐츠: <strong>{col.posts_count}개</strong>
              </div>
              {col.sample_posts.length > 0 && (
                <div style={{ fontSize: '0.8rem', color: '#cbd5e1', background: 'rgba(0,0,0,0.2)', padding: '0.6rem', borderRadius: '6px' }}>
                  "{col.sample_posts[0].caption || '저장 항목 메타데이터'}"
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
