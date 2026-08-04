import React, { useState } from 'react';
import { Plus, Search, Filter, Edit, Trash2, CheckCircle, Clock } from 'lucide-react';
import type { BlogPost } from '../api/adminClient';

interface BlogManagerProps {
  blogs: BlogPost[];
  onOpenCreate: () => void;
  onOpenEdit: (blog: BlogPost) => void;
  onDelete: (slug: string) => Promise<void>;
  onToggleStatus: (blog: BlogPost) => Promise<void>;
  loading: boolean;
}

export const BlogManager: React.FC<BlogManagerProps> = ({
  blogs,
  onOpenCreate,
  onOpenEdit,
  onDelete,
  onToggleStatus,
  loading,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'published' | 'draft'>('all');

  const filteredBlogs = blogs.filter((blog) => {
    const matchesSearch =
      blog.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      blog.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
      blog.slug.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' ? true : blog.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      {/* Controls Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1, minWidth: '280px' }}>
          <div style={{ position: 'relative', width: '100%', maxWidth: '360px' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search posts by title, category, or slug..."
              className="input-field"
              style={{ paddingLeft: '38px' }}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(15,23,42,0.8)', padding: '4px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <Filter size={14} style={{ marginLeft: '8px', color: 'var(--text-muted)' }} />
            {(['all', 'published', 'draft'] as const).map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                style={{
                  padding: '6px 12px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  border: 'none',
                  borderRadius: '6px',
                  background: statusFilter === st ? 'var(--primary-light)' : 'transparent',
                  color: statusFilter === st ? '#a5b4fc' : 'var(--text-muted)',
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                }}
              >
                {st}
              </button>
            ))}
          </div>
        </div>

        <button onClick={onOpenCreate} className="btn btn-primary">
          <Plus size={18} />
          <span>New Blog Post</span>
        </button>
      </div>

      {/* Posts Table */}
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Title & Category</th>
              <th>Status</th>
              <th>Published Date</th>
              <th>Author</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                  Loading blog posts...
                </td>
              </tr>
            ) : filteredBlogs.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                  No blog posts found matching your criteria.
                </td>
              </tr>
            ) : (
              filteredBlogs.map((blog) => (
                <tr key={blog.id}>
                  <td>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#fff', marginBottom: '4px' }}>
                        {blog.title}
                        {blog.featured && <span style={{ marginLeft: '8px', fontSize: '0.7rem', background: '#f59e0b20', color: '#f59e0b', padding: '2px 6px', borderRadius: '4px' }}>Featured</span>}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', gap: '8px' }}>
                        <span style={{ color: '#a5b4fc', fontWeight: 600 }}>{blog.category}</span>
                        <span>•</span>
                        <code style={{ fontSize: '0.7rem' }}>/{blog.slug}</code>
                      </div>
                    </div>
                  </td>

                  <td>
                    <button
                      onClick={() => onToggleStatus(blog)}
                      style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}
                      title="Click to toggle Draft / Published"
                    >
                      {blog.status === 'published' ? (
                        <span className="badge badge-success">
                          <CheckCircle size={12} /> Published
                        </span>
                      ) : (
                        <span className="badge badge-warning">
                          <Clock size={12} /> Draft
                        </span>
                      )}
                    </button>
                  </td>

                  <td style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    {blog.published_on}
                  </td>

                  <td style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    {blog.author || 'N/A'}
                  </td>

                  <td style={{ textAlign: 'right' }}>
                    <div style={{ display: 'inline-flex', gap: '8px' }}>
                      <button
                        onClick={() => onOpenEdit(blog)}
                        className="btn btn-secondary"
                        style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                        title="Edit post"
                      >
                        <Edit size={14} />
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Are you sure you want to delete "${blog.title}"?`)) {
                            onDelete(blog.slug);
                          }
                        }}
                        className="btn btn-danger"
                        style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                        title="Delete post"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
