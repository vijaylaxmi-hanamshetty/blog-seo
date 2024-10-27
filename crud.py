from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models
import schemas

def increment_view(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.views += 1
    db.commit()
    return {"views": post.views}

def add_like(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes += 1
    db.commit()
    return {"likes": post.likes}

def get_analytics(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"views": post.views, "likes": post.likes}

def generate_sitemap(db: Session):
    posts = db.query(models.Post).filter(models.Post.published == True).all()
    sitemap_content = "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"
    for post in posts:
        sitemap_content += f"<url><loc>http://example.com/posts/{post.id}</loc><lastmod>{post.created_at.isoformat()}</lastmod></url>\n"
    sitemap_content += "</urlset>"
    return sitemap_content

def manage_metadata(db: Session, post_id: int, meta_title: str = None, meta_description: str = None):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if meta_title or meta_description:
        if meta_title:
            post.meta_title = meta_title
        if meta_description:
            post.meta_description = meta_description
        db.commit()
    return {"meta_title": post.meta_title, "meta_description": post.meta_description}

def schedule_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(title=post.title, content=post.content, scheduled_at=post.scheduled_at, published=False)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"message": "Post scheduled", "scheduled_at": post.scheduled_at}

def publish_pending_posts(db: Session):
    posts_to_publish = db.query(models.Post).filter(models.Post.scheduled_at <= datetime.utcnow(), models.Post.published == False).all()
    for post in posts_to_publish:
        post.published = True
    db.commit()
    return {"message": f"{len(posts_to_publish)} posts published"}
