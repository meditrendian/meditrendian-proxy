from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import snscrape.modules.twitter as sntwitter
from pytube import YouTube

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/youtube")
def get_youtube_info(video_url: str = Query(..., description="YouTube video URL")):
    try:
        yt = YouTube(video_url)
        return {
            "title": yt.title,
            "views": yt.views,
            "author": yt.author,
            "description": yt.description[:300]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/twitter")
def get_twitter_trends(query: str = Query(...)):
    try:
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i > 10: break
            tweets.append({
                "user": tweet.user.username,
                "content": tweet.content,
                "date": str(tweet.date)
            })
        return {"tweets": tweets}
    except Exception as e:
        return {"error": str(e)}

@app.get("/instagram")
def get_instagram_info(username: str = Query(...)):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "username": profile.username,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount
        }
    except Exception as e:
        return {"error": str(e)}
