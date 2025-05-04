from fastapi import Depends, FastAPI,HTTPException,status,Response

#permission
from fastapi.middleware.cors import CORSMiddleware

#databse import
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db,engine


import models




app=FastAPI()



models.Base.metadata.create_all(bind=engine)

#permission for all connection
origins = [
    #"http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    
    

        

@app.get("/")
def index():
    return{'Data':"Hello world..............."}


#for getting all posts
@app.get("/post")
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

#create posts
@app.post("/post")
def create_post(post:Post,db:Session=Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/post/{id}")
def update_post(id:int,post:Post,db:Session=Depends(get_db)):
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if (posts==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesn't exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
   
@app.delete("/post/{id}") 
def delete_post(id:int,db:setattr=Depends(get_db)):
    
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/post/{id}")
def get_post(id:int,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if (posts==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesn't exist")
    
    return posts
