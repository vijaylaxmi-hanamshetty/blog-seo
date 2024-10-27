from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/posts/{post_id}/view")
def increment_view(post_id: int, db: Session = Depends(get_db)):
    return crud.increment_view(db, post_id)

@app.post("/posts/{post_id}/like")
def add_like(post_id: int, db: Session = Depends(get_db)):
    return crud.add_like(db, post_id)

@app.get("/posts/{post_id}/analytics")
def view_analytics(post_id: int, db: Session = Depends(get_db)):
    return crud.get_analytics(db, post_id)

# SEO Routes
@app.get("/sitemap.xml", response_class=PlainTextResponse)
def sitemap(db: Session = Depends(get_db)):
    return crud.generate_sitemap(db)

@app.get("/posts/{post_id}/metadata")
@app.put("/posts/{post_id}/metadata")
def manage_metadata(post_id: int, meta_title: str = None, meta_description: str = None, db: Session = Depends(get_db)):
    return crud.manage_metadata(db, post_id, meta_title, meta_description)

# Post Scheduling Routes
@app.post("/posts/schedule")
def schedule_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.schedule_post(db, post)

@app.post("/posts/publish_pending")
def publish_pending_posts(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return crud.publish_pending_posts(db)
