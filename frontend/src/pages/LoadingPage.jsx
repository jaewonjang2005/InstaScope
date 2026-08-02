import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Search } from 'lucide-react';

export default function LoadingPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const file = location.state?.file;
  
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('파일을 준비하는 중...');

  useEffect(() => {
    if (!file) {
      navigate('/');
      return;
    }

    const uploadFile = async () => {
      try {
        const chunkSize = 2 * 1024 * 1024; // 2MB
        const totalChunks = Math.ceil(file.size / chunkSize);
        const uploadId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
        
        for (let i = 0; i < totalChunks; i++) {
          const start = i * chunkSize;
          const end = Math.min(start + chunkSize, file.size);
          const chunk = file.slice(start, end);
          
          const formData = new FormData();
          formData.append('upload_id', uploadId);
          formData.append('chunk_index', i.toString());
          formData.append('total_chunks', totalChunks.toString());
          formData.append('file', chunk, file.name);

          setStatusText(`데이터 전송 중... (${i + 1}/${totalChunks})`);
          
          const apiUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';
          const response = await axios.post(`${apiUrl}/upload-chunk`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });

          // Update progress bar
          setProgress(Math.round(((i + 1) / totalChunks) * 100));

          if (response.data.completed) {
            setStatusText('데이터 분석 중... 거의 다 왔습니다!');
            
            // Poll for results
            const jobId = response.data.job_id;
            pollResults(jobId);
            break;
          }
        }
      } catch (err) {
        console.error('Upload error:', err);
        alert('업로드 중 오류가 발생했습니다. 다시 시도해주세요.');
        navigate('/');
      }
    };

    uploadFile();
  }, [file, navigate]);

  const pollResults = async (jobId) => {
    try {
      // Allow the backend a moment to process the in-memory extraction
      setTimeout(async () => {
        try {
          const apiUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';
          const res = await axios.get(`${apiUrl}/results/${jobId}`);
          if (res.data.status === 'success') {
            navigate('/result', { state: { data: res.data.data } });
          }
        } catch (e) {
          if (e.response && e.response.status === 404) {
            // Not ready yet, poll again
            setTimeout(() => pollResults(jobId), 1500);
          } else {
            console.error('Result error:', e);
            alert('분석 결과를 가져오는데 실패했습니다.');
            navigate('/');
          }
        }
      }, 1500);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="card fade-in" style={{ maxWidth: '600px', margin: '2rem auto', textAlign: 'center', padding: '4rem 2rem' }}>
      <div style={{
        width: '80px', height: '80px', borderRadius: '50%', 
        background: 'rgba(255,107,107,0.1)', display: 'flex', 
        alignItems: 'center', justifyContent: 'center', margin: '0 auto 2rem'
      }}>
        <Search size={40} color="var(--primary-color)" className="pulse-anim" />
      </div>
      
      <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>당신의 취향을 분석하고 추천하는 중...</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>{statusText}</p>

      <div style={{
        width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)',
        borderRadius: '4px', overflow: 'hidden'
      }}>
        <div style={{
          width: `${progress}%`, height: '100%',
          background: 'var(--gradient-primary)',
          transition: 'width 0.3s ease'
        }}></div>
      </div>
      <p style={{ marginTop: '1rem', fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
        {progress}%
      </p>
    </div>
  );
}
