import React, { useState } from 'react';
import { FileArchive, AlertCircle, HelpCircle, Check, Layers } from 'lucide-react';

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : '';

// 2MB binary chunk size (safely under Vercel 4.5MB request payload limit)
const CHUNK_SIZE = 2 * 1024 * 1024;

export default function UploadSection({ onAnalysisComplete, setStep, globalError, setGlobalError }) {
  const [dragActive, setDragActive] = useState(false);
  const [showGuideModal, setShowGuideModal] = useState(false);
  const [uploadProgressText, setUploadProgressText] = useState('');

  const handleFileUpload = async (file) => {
    if (!file || !file.name.endsWith('.zip')) {
      setGlobalError('ZIP 형식의 인스타그램 데이터 다운로드 파일만 업로드 가능합니다.');
      return;
    }

    setGlobalError('');
    setStep('loading');

    const uploadId = `chunk_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

    try {
      let finalJobId = null;

      // HTTP Chunked Sequential Upload: Bypasses Vercel 4.5MB limit while preserving 100% full dataset context
      for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_SIZE;
        const end = Math.min(start + CHUNK_SIZE, file.size);
        const chunkBlob = file.slice(start, end);

        setUploadProgressText(`대용량 데이터 청크 전송 중... (${i + 1}/${totalChunks})`);

        const formData = new FormData();
        formData.append('upload_id', uploadId);
        formData.append('chunk_index', i);
        formData.append('total_chunks', totalChunks);
        formData.append('file', chunkBlob, file.name);

        const res = await fetch(`${API_BASE_URL}/api/upload-chunk`, {
          method: 'POST',
          body: formData
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || `청크 ${i + 1}/${totalChunks} 조각 업로드 실패`);
        }

        if (data.completed && data.job_id) {
          finalJobId = data.job_id;
        }
      }

      if (finalJobId) {
        fetchResults(finalJobId);
      } else {
        setGlobalError('전체 청크 수신은 완료되었으나 분석 결과를 생성하지 못했습니다.');
        setStep('upload');
      }
    } catch (err) {
      console.error('HTTP Chunked upload error:', err);
      setGlobalError(`청크 분할 전송 중 오류 발생: ${err.message}`);
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
        HTTP 2MB 청크 분할 스트리밍 엔진이 100% 무손실 전체 데이터를 분석합니다.
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
          <Layers size={16} /> 🚀 HTTP 2MB 청크 분할 무손실 엔진 가동 (환각 0% · Vercel 제한 100% 우회)
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
            지원 형식: instagram-username-YYYY-MM-DD.zip (HTTP 청크 100% 전체 무손실 파싱)
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

      {/* Guide Modal */}
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
                🚀 HTTP 2MB 청크 분할 스트리밍 가이드
              </h3>
              <button onClick={() => setShowGuideModal(false)} style={{ background: 'none', border: 'none', color: '#fff', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
            </div>

            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.2rem', lineHeight: '1.5' }}>
              InstaScope 엔진은 대용량 ZIP 파일(8MB~500MB)을 <b>클라이언트 브라우저에서 2MB 이진 조각(Chunk)으로 쪼개서 서버로 연속 전송</b>합니다!
            </p>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem' }}>
              <div style={{ fontWeight: '700', marginBottom: '0.5rem', color: '#fcb045', fontSize: '0.95rem' }}>
                🌟 청크 분할 아키텍처의 3대 장점:
              </div>
              <ul style={{ fontSize: '0.85rem', color: '#ddd', paddingLeft: '1.2rem', lineHeight: '1.6' }}>
                <li>✅ <b>환각(Hallucination) 0%</b>: 100% 전체 JSON 데이터셋을 파이썬 백엔드에서 원본 그대로 분석!</li>
                <li>✅ <b>Vercel 4.5MB 제한 100% 우회</b>: 각 요청 크기가 2MB이므로 Vercel 관문 100% 통과!</li>
                <li>✅ <b>무손실 정확도</b>: 잘라내기 없이 전체 데이터셋 종합 분석 완료!</li>
              </ul>
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
