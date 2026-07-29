import React, { useState } from 'react';
import { FileArchive, AlertCircle, HelpCircle, Check } from 'lucide-react';
import JSZip from 'jszip';

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : '';

export default function UploadSection({ onAnalysisComplete, setStep, globalError, setGlobalError }) {
  const [dragActive, setDragActive] = useState(false);
  const [showGuideModal, setShowGuideModal] = useState(false);

  const uploadRawZip = async (file) => {
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
        setGlobalError(data.detail || '파일 업로드 실패. 4.5MB 제한 이하의 가벼운 ZIP으로 시도해 주세요.');
        setStep('upload');
      }
    } catch (err) {
      setGlobalError('API 서버와의 통신에 실패했습니다. 백엔드 상태를 확인하세요.');
      setStep('upload');
    }
  };

  const handleFileUpload = async (file) => {
    if (!file || !file.name.endsWith('.zip')) {
      setGlobalError('ZIP 형식의 인스타그램 데이터 다운로드 파일만 업로드 가능합니다.');
      return;
    }

    setGlobalError('');
    setStep('loading');

    try {
      // 🚀 Client-Side Unzipping: Open ZIP in browser memory & extract strictly your_instagram_activity JSONs!
      const zip = await JSZip.loadAsync(file);
      const extractedFiles = {};

      const targetFilePatterns = [
        'liked_posts.json',
        'saved_posts.json',
        'saved_collections.json',
        'story_likes.json',
        'stories_viewed.json',
        'liked_comments.json'
      ];

      for (const [filename, zipObject] of Object.entries(zip.files)) {
        if (zipObject.dir) continue;
        const lowerName = filename.toLowerCase();

        for (const pattern of targetFilePatterns) {
          if (lowerName.endsWith(pattern)) {
            const contentText = await zipObject.async('string');
            try {
              extractedFiles[filename] = JSON.parse(contentText);
            } catch (e) {
              console.warn('JSON parse error for', filename, e);
            }
            break;
          }
        }
      }

      if (Object.keys(extractedFiles).length === 0) {
        return uploadRawZip(file);
      }

      // Send lightweight ~200KB extracted your_instagram_activity JSON payload
      const res = await fetch(`${API_BASE_URL}/api/upload-payload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files: extractedFiles })
      });
      
      const data = await res.json();
      if (res.ok && data.job_id) {
        fetchResults(data.job_id);
      } else {
        setGlobalError(data.detail || '분석 실패');
        setStep('upload');
      }
    } catch (err) {
      console.warn('Browser JSZip extraction fallback:', err);
      uploadRawZip(file);
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
        활동 데이터(<code style={{ color: '#fcb045' }}>your_instagram_activity</code>) 초고속 분석기 전용으로 가동됩니다.
      </p>

      {/* Guide Banner Button */}
      <div style={{ marginBottom: '2rem', display: 'flex', gap: '0.8rem', justifyContent: 'center' }}>
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
          <HelpCircle size={16} /> ⚡ Ver 2.0 활동 전용 파서 가이드 (your_instagram_activity)
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
            지원 형식: instagram-username-YYYY-MM-DD.zip (활동 전용 0.1초 고속 분석)
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

      {/* Ver 2.0 Guide Modal */}
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
                ⚡ Ver 2.0 활동 전용 파서 가이드
              </h3>
              <button onClick={() => setShowGuideModal(false)} style={{ background: 'none', border: 'none', color: '#fff', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
            </div>

            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.2rem', lineHeight: '1.5' }}>
              InstaScope Ver 2.0 엔진은 광고(`ads_information`) 및 커넥션(`connections`)을 제외하고 <b>오직 내 실활동 폴더(`your_instagram_activity`)만 집중 파싱</b>합니다!
            </p>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem' }}>
              <div style={{ fontWeight: '700', marginBottom: '0.5rem', color: '#fcb045', fontSize: '0.95rem' }}>
                🟢 핵심 활동 분석 항목:
              </div>
              <ul style={{ fontSize: '0.85rem', color: '#ddd', paddingLeft: '1.2rem', lineHeight: '1.6' }}>
                <li>✅ <b>좋아요 한 게시물</b> (your_instagram_activity/likes)</li>
                <li>✅ <b>저장한 게시물 & 컬렉션</b> (your_instagram_activity/saved)</li>
                <li>✅ <b>스토리 반응 & 시청 이력</b> (your_instagram_activity/story_interactions)</li>
              </ul>
              <div style={{ marginTop: '0.8rem', fontSize: '0.85rem', color: '#2ed573', fontWeight: '700' }}>
                💡 미디어 사진/동영상 없이 활동 JSON만 들어가면 200KB 이하 초고속 분석 완료!
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
