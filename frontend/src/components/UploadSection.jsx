import React, { useState } from 'react';
import { FileArchive, AlertCircle, HelpCircle, Check } from 'lucide-react';

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : '';

export default function UploadSection({ onAnalysisComplete, setStep, globalError, setGlobalError }) {
  const [dragActive, setDragActive] = useState(false);
  const [showGuideModal, setShowGuideModal] = useState(false);

  const handleFileUpload = async (file) => {
    if (!file || !file.name.endsWith('.zip')) {
      setGlobalError('ZIP 형식의 인스타그램 데이터 다운로드 파일만 업로드 가능합니다.');
      return;
    }

    setGlobalError('');
    setStep('loading');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (res.ok && data.job_id) {
        fetchResults(data.job_id);
      } else {
        setGlobalError(data.detail || '파일 업로드 실패. 파일 용량이 Vercel 제한(4.5MB)을 초과했는지 확인하세요.');
        setStep('upload');
      }
    } catch (err) {
      setGlobalError('API 서버와의 통신에 실패했습니다. 파일 용량(4.5MB 제한) 또는 백엔드 상태를 확인하세요.');
      setStep('upload');
    }
  };

  const fetchResults = async (jobId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/results/${jobId}`);
      const data = await res.json();
      if (res.ok && data.data) {
        onAnalysisComplete(data.data);
        setStep('results');
      } else {
        setGlobalError('결과 조회 실패: 서버에서 분석 데이터를 가져오지 못했습니다.');
        setStep('upload');
      }
    } catch (err) {
      setGlobalError('결과 데이터를 불러오는데 실패했습니다.');
      setStep('upload');
    }
  };

  return (
    <div style={{ textAlign: 'center', margin: '2rem 0 4rem' }}>
      <h1 style={{ fontSize: '2.8rem', fontWeight: '800', lineHeight: '1.2' }}>
        인스타가 숨겨둔 <br />
        <span className="gradient-text">당신의 비밀 취향 & 이상형</span>을 해부합니다
      </h1>
      
      <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginTop: '1rem', maxWidth: '650px', margin: '1rem auto 1.5rem' }}>
        인스타그램 설정 &gt; 내 정보 다운로드에서 받은 <code style={{ color: '#fcb045', background: 'rgba(252, 176, 69, 0.1)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>.zip</code> 파일 하나만 드롭하세요.
        알고리즘 프로파일러가 즉시 동작합니다.
      </p>

      {/* Guide Banner Button */}
      <div style={{ marginBottom: '2rem' }}>
        <button 
          onClick={() => setShowGuideModal(true)}
          style={{
            background: 'rgba(131, 58, 180, 0.15)',
            border: '1px solid rgba(131, 58, 180, 0.4)',
            color: '#fcb045',
            padding: '0.6rem 1.2rem',
            borderRadius: '20px',
            fontSize: '0.9rem',
            fontWeight: '600',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            transition: 'all 0.2s ease'
          }}
        >
          <HelpCircle size={16} /> 💡 4.5MB 이하 초슬림 ZIP 준비 가이드 (용량 초과 방지)
        </button>
      </div>

      {/* Dropzone */}
      <div 
        className={`dropzone ${dragActive ? 'active' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragActive(false);
          if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileUpload(e.dataTransfer.files[0]);
          }
        }}
        onClick={() => document.getElementById('zip-input').click()}
      >
        <input 
          id="zip-input" 
          type="file" 
          accept=".zip" 
          style={{ display: 'none' }} 
          onChange={(e) => e.target.files && handleFileUpload(e.target.files[0])}
        />
        
        <div>
          <FileArchive size={52} color="#fd1d1d" style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.3rem', fontWeight: '700' }}>
            여기로 ZIP 파일을 끌어다 놓거나 클릭하여 업로드
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
            지원 형식: instagram-username-YYYY-MM-DD.zip (추천: 4.5MB 이하)
          </p>
        </div>
      </div>

      {/* Global Error Banner */}
      {globalError && (
        <div style={{
          marginTop: '1.8rem',
          color: '#ff4757',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.6rem',
          background: 'rgba(255, 71, 87, 0.12)',
          border: '1px solid rgba(255, 71, 87, 0.4)',
          padding: '1rem 1.5rem',
          borderRadius: '16px',
          maxWidth: '650px',
          margin: '1.8rem auto 0',
          fontSize: '0.95rem',
          lineHeight: '1.4'
        }}>
          <AlertCircle size={22} style={{ flexShrink: 0 }} /> 
          <div style={{ textAlign: 'left' }}>{globalError}</div>
        </div>
      )}

      {/* Ultra Slim ZIP Guide Modal */}
      {showGuideModal && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '1rem'
        }}>
          <div className="glass-card" style={{ maxWidth: '540px', width: '100%', padding: '2rem', borderRadius: '24px', textAlign: 'left' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.3rem', fontWeight: '800' }} className="gradient-text">
                📦 초슬림 데이터 셋 가이드 (&lt; 1MB)
              </h3>
              <button onClick={() => setShowGuideModal(false)} style={{ background: 'none', border: 'none', color: '#fff', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
            </div>

            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.2rem', lineHeight: '1.5' }}>
              Vercel 무료 서버리스의 4.5MB 용량 제한을 넘지 않도록, 인스타그램 다운로드 선택 화면에서 **아래 5개 핵심 항목만 체크**하거나 **`media/` (사진/영상) 폴더를 지우고 압축**하면 500KB의 초슬림 ZIP이 만들어집니다!
            </p>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem' }}>
              <div style={{ fontWeight: '700', marginBottom: '0.5rem', color: '#fcb045', fontSize: '0.95rem' }}>
                🟢 인스타 다운로드 시 필수 체크 5가지:
              </div>
              <ul style={{ fontSize: '0.85rem', color: '#ddd', paddingLeft: '1.2rem', lineHeight: '1.6' }}>
                <li>✅ <b>좋아요</b> (your_instagram_activity/likes)</li>
                <li>✅ <b>저장됨</b> (your_instagram_activity/saved)</li>
                <li>✅ <b>스토리 반응</b> (your_instagram_activity/story_stanzas)</li>
                <li>✅ <b>팔로워 및 팔로잉</b> (connections/followers_and_following)</li>
                <li>✅ <b>광고 및 주제</b> (ads_information)</li>
              </ul>
              <div style={{ marginTop: '0.8rem', fontSize: '0.85rem', color: '#ff4757', fontWeight: '700' }}>
                ❌ [미디어] (사진/동영상) 박스는 꼭 체크 해제하세요! (용량 99% 원인)
              </div>
            </div>

            <button className="gradient-btn" style={{ width: '100%', padding: '0.8rem' }} onClick={() => setShowGuideModal(false)}>
              <Check size={18} /> 확인했습니다
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
