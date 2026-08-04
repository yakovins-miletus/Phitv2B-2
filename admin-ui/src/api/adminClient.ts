const API_BASE = 'http://127.0.0.1:8000/api/v1';

export interface AdminStats {
  total_blog_posts: number;
  published_blog_posts: number;
  draft_blog_posts: number;
  total_contact_messages: number;
  total_services: number;
  total_team_members: number;
}

export interface BlogPost {
  id: string;
  slug: string;
  title: string;
  category: str;
  excerpt: str;
  body?: str;
  image_url: string | null;
  author: string | null;
  status: 'draft' | 'published';
  published_on: string;
  featured: boolean;
}

export interface BlogPostPage {
  items: BlogPost[];
  total: number;
  limit: number;
  offset: number;
}

export interface ContactMessage {
  id: string;
  name: string;
  email: string;
  subject: string;
  message: string;
  created_at: string;
}

export const adminApi = {
  async getStats(): Promise<AdminStats> {
    const res = await fetch(`${API_BASE}/heimdall/admin/stats`);
    if (!res.ok) throw new Error('Failed to fetch admin stats');
    return res.json();
  },

  async listBlogs(limit = 50, offset = 0, q = '', category = ''): Promise<BlogPostPage> {
    const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
    if (q) params.append('q', q);
    if (category) params.append('category', category);
    const res = await fetch(`${API_BASE}/heimdall/admin/blogs?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch blog posts');
    return res.json();
  },

  async createBlog(payload: Omit<BlogPost, 'id'>): Promise<BlogPost> {
    const res = await fetch(`${API_BASE}/heimdall/admin/blogs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to create blog post' }));
      throw new Error(err.detail || 'Failed to create blog post');
    }
    return res.json();
  },

  async updateBlog(slug: string, payload: Partial<BlogPost>): Promise<BlogPost> {
    const res = await fetch(`${API_BASE}/heimdall/admin/blogs/${slug}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update blog post');
    return res.json();
  },

  async deleteBlog(slug: string): Promise<void> {
    const res = await fetch(`${API_BASE}/heimdall/admin/blogs/${slug}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete blog post');
  },

  async listContactMessages(limit = 50, offset = 0): Promise<ContactMessage[]> {
    const res = await fetch(`${API_BASE}/heimdall/admin/contact-messages?limit=${limit}&offset=${offset}`);
    if (!res.ok) throw new Error('Failed to fetch contact messages');
    return res.json();
  },

  async listServices(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/services`);
    if (!res.ok) throw new Error('Failed to fetch services');
    return res.json();
  },

  async listTeam(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/team`);
    if (!res.ok) throw new Error('Failed to fetch team members');
    return res.json();
  },
};
