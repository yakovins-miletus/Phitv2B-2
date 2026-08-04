import React, { useState, useEffect } from 'react';
import { X, Save, Eye, Edit2 } from 'lucide-react';
import type { BlogPost } from '../api/adminClient';

interface BlogEditorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (payload: any) => Promise<void>;
  initialData?: BlogPost | null;
}

export const BlogEditorModal: React.FC<BlogEditorModalProps> = ({ isOpen, onClose, onSave, initialData }) => {
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    category: 'People',
    excerpt: '',
    body: '',
    author: '',
    status: 'published' as 'draft' | 'published',
    published_on: new Date().toISOString().split('T')[0],
    featured: false,
  });

  const [activeTab, setActiveTab] = useState<'write' | 'preview'>('write');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        slug: initialData.slug || '',
        category: initialData.category || 'People',
        excerpt: initialData.excerpt || '',
        body: initialData.body || '',
        author: initialData.author || '',
        status: initialData.status || 'published',
        published_on: initialData.published_on || new Date().toISOString().split('T')[0],
        featured: initialData.featured || false,
      });
    } else {
      setFormData({
        title: '',
        slug: '',
        category: 'People',
        excerpt: '',
        body: '',
        author: 'Phitopolis Team',
        status: 'published',
        published_on: new Date().toISOString().split('T')[0],
        featured: false,
      });
    }
  }, [initialData, isOpen]);

  const handleTitleChange = (title: string) => {
    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    setFormData((prev) => ({ ...prev, title, slug: initialData ? prev.slug : slug }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await onSave(formData);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to save blog post');
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ padding: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
              {initialData ? 'Edit Blog Post' : 'Create New Blog Post'}
            </h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Draft or publish content instantly to Phitopolis Heimdall CMS
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        {error && (
          <div style={{ padding: '12px 16px', background: 'var(--danger-bg)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '8px', color: 'var(--danger)', fontSize: '0.85rem', marginBottom: '16px' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '16px' }}>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Title</label>
              <input
                type="text"
                className="input-field"
                required
                value={formData.title}
                onChange={(e) => handleTitleChange(e.target.value)}
                placeholder="e.g. 2026 Technical Graduate Onboarding Week"
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Category</label>
              <select
                className="input-field"
                value={formData.category}
                onChange={(e) => setFormData((prev) => ({ ...prev, category: e.target.value }))}
              >
                <option value="People">People</option>
                <option value="Community & CSR">Community & CSR</option>
                <option value="Data Engineering / Data Science">Data Science</option>
                <option value="Quantitative Research">Quantitative Research</option>
                <option value="Technology">Technology</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '16px' }}>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>URL Slug</label>
              <input
                type="text"
                className="input-field"
                required
                value={formData.slug}
                onChange={(e) => setFormData((prev) => ({ ...prev, slug: e.target.value }))}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Author</label>
              <input
                type="text"
                className="input-field"
                value={formData.author}
                onChange={(e) => setFormData((prev) => ({ ...prev, author: e.target.value }))}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Publish Status</label>
              <select
                className="input-field"
                value={formData.status}
                onChange={(e) => setFormData((prev) => ({ ...prev, status: e.target.value as any }))}
              >
                <option value="published">Published</option>
                <option value="draft">Draft</option>
              </select>
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Excerpt / Summary</label>
            <input
              type="text"
              className="input-field"
              required
              value={formData.excerpt}
              onChange={(e) => setFormData((prev) => ({ ...prev, excerpt: e.target.value }))}
              placeholder="Short 1-2 sentence preview for cards..."
            />
          </div>

          {/* Write / Preview Tab switcher */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>Article Body (Markdown supported)</label>
              <div style={{ display: 'flex', gap: '4px', background: 'rgba(15,23,42,0.8)', padding: '2px', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                <button
                  type="button"
                  onClick={() => setActiveTab('write')}
                  style={{
                    padding: '4px 10px',
                    fontSize: '0.75rem',
                    border: 'none',
                    borderRadius: '4px',
                    background: activeTab === 'write' ? 'var(--primary)' : 'transparent',
                    color: '#fff',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  <Edit2 size={12} /> Write
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('preview')}
                  style={{
                    padding: '4px 10px',
                    fontSize: '0.75rem',
                    border: 'none',
                    borderRadius: '4px',
                    background: activeTab === 'preview' ? 'var(--primary)' : 'transparent',
                    color: '#fff',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  <Eye size={12} /> Preview
                </button>
              </div>
            </div>

            {activeTab === 'write' ? (
              <textarea
                className="input-field"
                style={{ minHeight: '220px', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}
                required
                value={formData.body}
                onChange={(e) => setFormData((prev) => ({ ...prev, body: e.target.value }))}
                placeholder="Write full article body text..."
              />
            ) : (
              <div style={{ minHeight: '220px', padding: '16px', background: 'rgba(15,23,42,0.9)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)', fontSize: '0.9rem', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                {formData.body || <span style={{ color: 'var(--text-dim)' }}>No content to preview yet.</span>}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '12px', paddingTop: '16px', borderTop: '1px solid var(--border-color)' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.85rem' }}>
              <input
                type="checkbox"
                checked={formData.featured}
                onChange={(e) => setFormData((prev) => ({ ...prev, featured: e.target.checked }))}
              />
              <span>Feature this post on home banner</span>
            </label>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button type="button" onClick={onClose} className="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                <Save size={16} />
                <span>{saving ? 'Saving...' : 'Save Post'}</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
