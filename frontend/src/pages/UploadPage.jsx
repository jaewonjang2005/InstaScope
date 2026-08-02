import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, AlertCircle, FileArchive } from 'lucide-react';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.name.endsWith('.zip')) {
      setFile(selected);
      setError('');
    } else {
      setFile(null);
      setError('올바른 ZIP 파일이 아닙니다. 인스타그램에서 다운로드한 ZIP 파일을 선택해주세요.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('파일을 먼저 선택해주세요.');
      return;
    }

    setIsUploading(true);
    setError('');
    
    // Move to loading page immediately, we'll do the upload there
    navigate('/loading', { state: { file } });
  };

  return (
    <div className="card fade-in" style={{ maxWidth: '600px', margin: '2rem auto', textAlign: 'center' }}>
      <h2 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>
        당신의 숨겨진 <span className="highlight">인스타 취향</span>은?
      </h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: '1.6' }}>
        좋아요, 저장, 스토리 시청 기록을 교차 분석하여<br />
        당신이 가장 끌리는 맞춤형 콘텐츠를 실시간으로 찾아드립니다.<br />
        <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>* 분석 후 모든 데이터는 즉시 폐기됩니다.</span>
      </p>

      {error && (
        <div style={{
          background: 'rgba(255, 60, 60, 0.1)',
          border: '1px solid rgba(255, 60, 60, 0.3)',
          padding: '1rem',
          borderRadius: '12px',
          color: '#ff8a8a',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.5rem',
          fontSize: '0.9rem'
        }}>
          <AlertCircle size={18} /> {error}
        </div>
      )}

      <div 
        onClick={() => fileInputRef.current.click()}
        style={{
          border: '2px dashed rgba(255, 255, 255, 0.2)',
          borderRadius: '20px',
          padding: '3rem 2rem',
          cursor: 'pointer',
          background: 'rgba(0, 0, 0, 0.2)',
          transition: 'all 0.3s ease',
          marginBottom: '1.5rem'
        }}
        onMouseOver={(e) => e.currentTarget.style.borderColor = 'var(--primary-color)'}
        onMouseOut={(e) => e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.2)'}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          accept=".zip" 
          style={{ display: 'none' }} 
        />
        
        {file ? (
          <div>
            <FileArchive size={48} color="var(--primary-color)" style={{ margin: '0 auto 1rem' }} />
            <h3 style={{ color: '#fff', marginBottom: '0.5rem' }}>{file.name}</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>
        ) : (
          <div>
            <UploadCloud size={48} color="rgba(255,255,255,0.5)" style={{ margin: '0 auto 1rem' }} />
            <h3 style={{ color: '#fff', marginBottom: '0.5rem' }}>인스타그램 데이터를 업로드하세요</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              클릭하여 ZIP 파일 선택 (최대 권장 1GB)
            </p>
          </div>
        )}
      </div>

      <button 
        className="gradient-btn" 
        style={{ width: '100%', padding: '1rem', fontSize: '1.1rem', display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}
        onClick={handleUpload}
        disabled={!file || isUploading}
      >
        {isUploading ? '분석 준비 중...' : '나의 취향 분석 시작 🔥'}
      </button>
    </div>
  );
}
