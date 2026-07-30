from pydantic import BaseModel
from app.features.blog.schemas import BlogPostOut, BlogPostPage
from app.features.contact.schemas import ContactMessageOut


class AdminStats(BaseModel):
    total_blog_posts: int
    published_blog_posts: int
    draft_blog_posts: int
    total_contact_messages: int
    total_services: int
    total_team_members: int
