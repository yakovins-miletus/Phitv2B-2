import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { StatsOverview } from './components/StatsOverview';
import { BlogManager } from './components/BlogManager';
import { BlogEditorModal } from './components/BlogEditorModal';
import { ContactInbox } from './components/ContactInbox';
import { adminApi } from './api/adminClient';
import type { AdminStats, BlogPost, ContactMessage } from './api/adminClient';
import { Layers, Users, ShieldAlert } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [blogs, setBlogs] = useState<BlogPost[]>([]);
  const [contactMessages, setContactMessages] = useState<ContactMessage[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [team, setTeam] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [editingBlog, setEditingBlog] = useState<BlogPost | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsData, blogsData, contactData, servicesData, teamData] = await Promise.all([
        adminApi.getStats().catch(() => null),
        adminApi.listBlogs().catch(() => ({ items: [], total: 0, limit: 50, offset: 0 })),
        adminApi.listContactMessages().catch(() => []),
        adminApi.listServices().catch(() => []),
        adminApi.listTeam().catch(() => []),
      ]);

      if (statsData) setStats(statsData);
      if (blogsData) setBlogs(blogsData.items);
      if (contactData) setContactMessages(contactData);
      if (servicesData) setServices(servicesData);
      if (teamData) setTeam(teamData);
    } catch (err) {
      console.error('Failed to load Heimdall admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenCreate = () => {
    setEditingBlog(null);
    setIsEditorOpen(true);
  };

  const handleOpenEdit = (blog: BlogPost) => {
    setEditingBlog(blog);
    setIsEditorOpen(true);
  };

  const handleSaveBlog = async (payload: any) => {
    if (editingBlog) {
      await adminApi.updateBlog(editingBlog.slug, payload);
    } else {
      await adminApi.createBlog(payload);
    }
    await loadData();
  };

  const handleDeleteBlog = async (slug: string) => {
    await adminApi.deleteBlog(slug);
    await loadData();
  };

  const handleToggleStatus = async (blog: BlogPost) => {
    const newStatus = blog.status === 'published' ? 'draft' : 'published';
    await adminApi.updateBlog(blog.slug, { status: newStatus });
    await loadData();
  };

  const getTitle = () => {
    switch (activeTab) {
      case 'dashboard': return 'System Overview';
      case 'blogs': return 'Blog Post Manager';
      case 'contact': return 'Contact Form Submissions';
      case 'services': return 'Services Catalog';
      case 'team': return 'Team Directory';
      default: return 'Admin Panel';
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-primary)' }}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflowX: 'hidden' }}>
        <Header title={getTitle()} onRefresh={loadData} loading={loading} />

        <div style={{ padding: '32px', flex: 1 }}>
          <StatsOverview stats={stats} />

          {activeTab === 'dashboard' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '1.1rem', marginBottom: '12px' }}>Welcome to Heimdall CMS</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
                  Heimdall is your in-house Content Management System serving public endpoints to <strong>Phitopolis Fresko</strong> and private admin routes over Tailscale Mesh VPN. Use the sidebar menu to create blog posts, manage drafts, and inspect user contact inquiries.
                </p>
              </div>
              <BlogManager
                blogs={blogs}
                onOpenCreate={handleOpenCreate}
                onOpenEdit={handleOpenEdit}
                onDelete={handleDeleteBlog}
                onToggleStatus={handleToggleStatus}
                loading={loading}
              />
            </div>
          )}

          {activeTab === 'blogs' && (
            <BlogManager
              blogs={blogs}
              onOpenCreate={handleOpenCreate}
              onOpenEdit={handleOpenEdit}
              onDelete={handleDeleteBlog}
              onToggleStatus={handleToggleStatus}
              loading={loading}
            />
          )}

          {activeTab === 'contact' && (
            <ContactInbox messages={contactMessages} loading={loading} />
          )}

          {activeTab === 'services' && (
            <div className="glass-panel" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Layers size={18} color="var(--primary)" />
                <span>Services Catalog ({services.length})</span>
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
                {services.map((svc) => (
                  <div key={svc.id} style={{ background: 'rgba(15,23,42,0.8)', padding: '20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#fff', marginBottom: '4px' }}>{svc.name}</div>
                    <div style={{ fontSize: '0.8rem', color: '#a5b4fc', marginBottom: '8px' }}>{svc.tagline}</div>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5, marginBottom: '12px' }}>{svc.description}</p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {svc.highlights?.map((h: string, idx: number) => (
                        <span key={idx} className="badge badge-purple">{h}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'team' && (
            <div className="glass-panel" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Users size={18} color="var(--primary)" />
                <span>Team Members Directory ({team.length})</span>
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
                {team.map((m) => (
                  <div key={m.id} style={{ background: 'rgba(15,23,42,0.8)', padding: '20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#fff', marginBottom: '4px' }}>{m.name}</div>
                    <div style={{ fontSize: '0.8rem', color: '#10b981', fontWeight: 600, marginBottom: '8px' }}>{m.role}</div>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5, marginBottom: '12px' }}>{m.bio}</p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {m.focus_areas?.map((fa: string, idx: number) => (
                        <span key={idx} className="badge badge-success">{fa}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      <BlogEditorModal
        isOpen={isEditorOpen}
        onClose={() => setIsEditorOpen(false)}
        onSave={handleSaveBlog}
        initialData={editingBlog}
      />
    </div>
  );
};
