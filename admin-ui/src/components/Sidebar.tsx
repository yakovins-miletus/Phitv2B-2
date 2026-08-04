import React from 'react';
import { LayoutDashboard, FileText, Mail, Layers, Users, ShieldAlert, Sparkles } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'blogs', label: 'Blog Posts', icon: FileText },
    { id: 'contact', label: 'Contact Leads', icon: Mail },
    { id: 'services', label: 'Services', icon: Layers },
    { id: 'team', label: 'Team Members', icon: Users },
  ];

  return (
    <aside style={{ width: '260px', background: '#0d1322', borderRight: '1px solid var(--border-color)', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Brand Header */}
      <div style={{ padding: '24px 20px', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ background: 'linear-gradient(135deg, #6366f1, #a855f7)', width: '36px', height: '36px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 16px rgba(99,102,241,0.4)' }}>
          <Sparkles size={20} color="#fff" />
        </div>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 800, background: 'linear-gradient(90deg, #fff, #a5b4fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Heimdall CMS
          </h2>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
            Phitopolis Admin
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav style={{ padding: '16px 12px', flex: 1 }}>
        <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--text-dim)', padding: '8px 12px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Management
        </div>
        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '4px' }}>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <li key={item.id}>
                <button
                  onClick={() => setActiveTab(item.id)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 14px',
                    borderRadius: '8px',
                    border: 'none',
                    background: isActive ? 'var(--primary-light)' : 'transparent',
                    color: isActive ? '#a5b4fc' : 'var(--text-muted)',
                    fontWeight: isActive ? 700 : 500,
                    cursor: 'pointer',
                    fontSize: '0.9rem',
                    transition: 'all 0.15s ease',
                    textAlign: 'left',
                    boxShadow: isActive ? 'inset 0 0 0 1px rgba(99,102,241,0.3)' : 'none',
                  }}
                >
                  <Icon size={18} color={isActive ? '#6366f1' : 'var(--text-muted)'} />
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer Info */}
      <div style={{ padding: '16px', borderTop: '1px solid var(--border-color)', margin: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <ShieldAlert size={16} color="#10b981" />
          <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#10b981' }}>Tailscale Protected</span>
        </div>
        <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', lineHeight: 1.4 }}>
          Access restricted to authorized private mesh network.
        </p>
      </div>
    </aside>
  );
};
