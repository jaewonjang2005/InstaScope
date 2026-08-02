import React from 'react';
import { ExternalLink, Hash, Flame } from 'lucide-react';

export default function Recommendations({ title, items, icon, colorClass }) {
  if (!items || items.length === 0) return null;

  return (
    <div className={`glass-card recommendation-section ${colorClass}`} style={{ marginBottom: '2rem', padding: '2rem' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', fontSize: '1.5rem' }}>
        {icon} {title}
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {items.map((item, idx) => (
          <a
            key={idx}
            href={item.url}
            target="_blank"
            rel="noreferrer"
            className="recommendation-item"
            style={{
              display: 'block',
              padding: '1.5rem',
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              borderRadius: '12px',
              textDecoration: 'none',
              color: 'inherit',
              transition: 'all 0.2s ease',
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
              <div>
                <span 
                  style={{
                    display: 'inline-block',
                    padding: '0.2rem 0.6rem',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '20px',
                    fontSize: '0.8rem',
                    marginBottom: '0.5rem',
                    color: 'var(--primary-color)'
                  }}
                >
                  #{item.matched_keyword}
                </span>
                <h4 style={{ fontSize: '1.1rem', margin: '0 0 0.5rem 0', lineHeight: '1.4' }}>{item.title}</h4>
                <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  {item.snippet}
                </p>
              </div>
              <ExternalLink size={20} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
