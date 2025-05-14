from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse
from datetime import datetime

class URLItem(BaseModel):
    url: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_url(url: str, is_phishing: bool):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "PHISHING" if is_phishing else "SAFE"
    with open("logs.txt", "a") as f:
        f.write(f"[{now}] {url} -> {status}\n")

@app.post("/check")
async def check_url(item: URLItem):
    try:
        parsed = urlparse(item.url)
        hostname = parsed.hostname or ""
        is_phishing = not hostname.endswith(".com")
    except Exception:
        hostname = "INVALID_URL"
        is_phishing = True  # 保守處理無效 URL 為可疑

    log_url(item.url, is_phishing)
    if is_phishing:
        return {"warning": True, "message": "警告：這可能是釣魚網站！"}
    return {"warning": False, "message": "Safe"}

# 本地執行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


