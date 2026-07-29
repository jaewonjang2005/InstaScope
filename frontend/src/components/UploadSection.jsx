import React, { useState } from 'react';
import { Upload, FileArchive, Zap, CheckCircle2, AlertCircle } from 'lucide-react';

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : '';

export default function UploadSection({ onAnalysisComplete, loading, setLoading }) {
  const [dragActive, setDragActive] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleFileUpload = async (file) => {
    if (!file || !file.name.endsWith('.zip')) {
      setErrorMsg('ZIP 형식의 인스타그램 데이터 다운로드 파일만 업로드 가능합니다.');
      return;
    }

    setErrorMsg('');
    setLoading(true);

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
        setErrorMsg(data.detail || '파일 업로드 실패');
        setLoading(false);
      }
    } catch (err) {
      setErrorMsg('API 서버와의 통신에 실패했습니다.');
      setLoading(false);
    }
  };

  const handleLocalDemo = async () => {
    setErrorMsg('');
    setLoading(true);
    try {
      const localPath = "c:\\Users\\jjaew\\OneDrive\\바탕 화면\\2026 2학기 부트캠프 스터디\\7-8월 토이프로젝트(인스타 알고리즘 분석)\\instagram-lex_xelop-전체데이터(7.28.2026 기준)";
      const res = await fetch(`${API_BASE_URL}/api/analyze-local?dir_path=${encodeURIComponent(localPath)}`, {
        method: 'POST'
      });
      const data = await res.json();
      if (res.ok && data.job_id) {
        fetchResults(data.job_id);
      } else {
        setErrorMsg(data.detail || '샘플 데이터 분석 실패');
        setLoading(false);
      }
    } catch (err) {
      setErrorMsg('API 서버 연결 오류. 백엔드 서버 상태를 확인하세요.');
      setLoading(false);
    }
  };

  const fetchResults = async (jobId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/results/${jobId}`);
      const data = await res.json();
      if (res.ok && data.data) {
        onAnalysisComplete(data.data);
      } else {
        setErrorMsg('결과 조회 실패');
      }
    } catch (err) {
      setErrorMsg('결과 데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', margin: '2rem 0 4rem' }}>
      <h1 style={{ fontSize: '2.8rem', fontWeight: '800', lineHeight: '1.2' }}>
        인스타가 숨겨둔 <br />
        <span className="gradient-text">당신의 비밀 취향 & 이상형</span>을 해부합니다
      </h1>
      <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginTop: '1rem', maxWidth: '650px', margin: '1rem auto 2.5rem' }}>
        인스타그램 설정 &gt; 내 정보 다운로드에서 받은 <code style={{ color: '#fcb045', background: 'rgba(252, 176, 69, 0.1)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>.zip</code> 파일 하나만 드롭하세요.
        알고리즘 분석기가 즉시 동작합니다.
      </p>

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
        
        {loading ? (
          <div>
            <div className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: '800' }}>
              🧠 알고리즘 데이터 해부 및 정밀 분석 중...
            </div>
            <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
              좋아요 내역, 저장한 게시물, 본 스토리, 광고 타겟팅 카테고리를 교차 검증하고 있습니다.
            </p>
          </div>
        ) : (
          <div>
            <FileArchive size={52} color="#fd1d1d" style={{ marginBottom: '1rem' }} />
            <h3 style={{ fontSize: '1.3rem', fontWeight: '700' }}>
              여기로 ZIP 파일을 끌어다 놓거나 클릭하여 업로드
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
              지원 형식: instagram-username-YYYY-MM-DD.zip
            </p>
          </div>
        )}
      </div>

      {errorMsg && (
        <div style={{ marginTop: '1rem', color: '#ff4757', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
          <AlertCircle size={18} /> {errorMsg}
        </div>
      )}

      {/* Local Fast Demo Button */}
      <div style={{ marginTop: '2rem' }}>
        <button className="gradient-btn" onClick={handleLocalDemo} disabled={loading}>
          <Zap size={18} /> 샘플 데이터로 즉시 분석해보기 (Fast Demo)
        </button>
      </div>
    </div>
  );
}
