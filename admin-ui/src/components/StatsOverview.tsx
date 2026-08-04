import React from 'react';
import { FileText, CheckCircle, Edit3, Mail, Layers, Users } from 'lucide-react';
import type { AdminStats } from '../api/adminClient';

interface StatsOverviewProps {
  stats: AdminStats | null;
}

export const StatsOverview: React.FC<StatsOverviewProps> = ({ stats }) => {
  const cards = [
    { label: 'Total Blog Posts', value: stats?.total_blog_posts ?? 0, icon: FileText, color: '#6366f1' },
    { label: 'Published Posts', value: stats?.published_blog_posts ?? 0, icon: CheckCircle, color: '#10b981' },
    { label: 'Draft Posts', value: stats?.draft_blog_posts ?? 0, icon: Edit3, color: '#f59e0b' },
    { label: 'Contact Leads', value: stats?.total_contact_messages ?? 0, icon: Mail, color: '#ec4899' },
    { label: 'Services', value: stats?.total_services ?? 0, icon: Layers, color: '#3b82f6' },
    { label: 'Team Members', value: stats?.total_team_members ?? 0, icon: Users, color: '#8b5cf6' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '28px' }}>
      {cards.map((card, i) => {
        const Icon = card.icon;
        return (
          <div key={i} className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>{card.label}</span>
              <div style={{ background: `${card.color}18`, padding: '8px', borderRadius: '8px', border: `1px solid ${card.color}30` }}>
                <Icon size={18} color={card.color} />
              </div>
            </div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, letterSpacing: '-0.03em' }}>
              {card.value}
            </div>
          </div>
        );
      })}
    </div>
  );
};
