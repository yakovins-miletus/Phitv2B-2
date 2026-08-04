import React from 'react';
import { RefreshCw, ExternalLink, Activity } from 'lucide-react';

interface HeaderProps {
  title: string;
  onRefresh: () => void;
  loading: boolean;
}

export const Header: React.FC<HeaderProps> = ({ title, onRefresh, loading }) => {
  return (
    <header style={{ padding: '20px 32px', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(17, 24, 39, 0.4)', backdropFilter: 'blur(8px)' }}>
      <div>
        <h1 style={{ fontSize: '1.4rem', fontWeight: 800 }}>{title}</h1>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
          Manage your in-house Phitopolis content and system parameters
        </p>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 12px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 600, color: '#10b981' }}>
          <Activity size={14} className="spin" />
          <span>Backend Live (127.0.0.1:8000)</span>
        </div>

        <button onClick={onRefresh} className="btn btn-secondary" disabled={loading} style={{ padding: '8px 14px' }}>
          <RefreshCw size={14} style={{ animation: loading ? 'spin 1s linear infinite' : 'none' }} />
          <span>Sync Data</span>
        </button>

        <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="btn btn-secondary" style={{ padding: '8px 14px', textDecoration: 'none' }}>
          <span>API Docs</span>
          <ExternalLink size={14} />
        </a>
      </div>
    </header>
  );
};
