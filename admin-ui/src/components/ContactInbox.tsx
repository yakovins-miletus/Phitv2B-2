import React, { useState } from 'react';
import { Mail, Calendar, User, MessageSquare, ChevronRight } from 'lucide-react';
import type { ContactMessage } from '../api/adminClient';

interface ContactInboxProps {
  messages: ContactMessage[];
  loading: boolean;
}

export const ContactInbox: React.FC<ContactInboxProps> = ({ messages, loading }) => {
  const [selectedMessage, setSelectedMessage] = useState<ContactMessage | null>(null);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: selectedMessage ? '1fr 1fr' : '1fr', gap: '24px' }}>
      {/* Messages List */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Mail size={18} color="var(--primary)" />
          <span>Incoming Contact Form Submissions ({messages.length})</span>
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {loading ? (
            <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading inbox...</div>
          ) : messages.length === 0 ? (
            <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>No messages received yet.</div>
          ) : (
            messages.map((msg) => {
              const isSelected = selectedMessage?.id === msg.id;
              return (
                <div
                  key={msg.id}
                  onClick={() => setSelectedMessage(msg)}
                  style={{
                    padding: '16px',
                    borderRadius: 'var(--radius-md)',
                    background: isSelected ? 'var(--primary-light)' : 'rgba(15,23,42,0.6)',
                    border: `1px solid ${isSelected ? 'var(--primary)' : 'var(--border-color)'}`,
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#fff' }}>{msg.name}</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {new Date(msg.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#a5b4fc', marginBottom: '4px' }}>
                    {msg.subject}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {msg.message}
                  </p>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Message Detail Pane */}
      {selectedMessage && (
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>{selectedMessage.subject}</h3>
            <button onClick={() => setSelectedMessage(null)} className="btn btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
              Close Pane
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', background: 'rgba(15,23,42,0.8)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
              <User size={16} color="var(--primary)" />
              <span style={{ fontWeight: 700, color: '#fff' }}>{selectedMessage.name}</span>
              <span style={{ color: 'var(--text-muted)' }}>&lt;{selectedMessage.email}&gt;</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              <Calendar size={14} />
              <span>Received {new Date(selectedMessage.created_at).toLocaleString()}</span>
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <MessageSquare size={14} /> Message Content
            </div>
            <div style={{ background: '#0f172a', padding: '20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', fontSize: '0.9rem', lineHeight: 1.6, whiteSpace: 'pre-wrap', color: '#e2e8f0' }}>
              {selectedMessage.message}
            </div>
          </div>

          <div style={{ paddingTop: '12px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'flex-end' }}>
            <a href={`mailto:${selectedMessage.email}?subject=Re: ${encodeURIComponent(selectedMessage.subject)}`} className="btn btn-primary">
              <span>Reply via Email</span>
              <ChevronRight size={16} />
            </a>
          </div>
        </div>
      )}
    </div>
  );
};
