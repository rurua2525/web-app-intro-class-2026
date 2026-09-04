from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# 静的ファイル（HTML, CSS, JS）の配信設定
app.mount("/static", StaticFiles(directory="static"), name="static")
# ルートURLにアクセスしたときに index.html を返す
@app.get("/")
def read_root():
    return FileResponse("static/index.html")
DB_NAME = "gunplas.db"

# データベースとテーブルの初期化
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gunplas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            owned INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# アプリ起動時にテーブルを作成
init_db()

# Pydanticモデルの定義
class GunplaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class GunplaUpdate(BaseModel):
    owned: bool

# 1. 一覧取得 (GET /gunplas)
@app.get("/gunplas")
def get_gunplas():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, owned FROM gunplas ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    gunplas = []
    for row in rows:
        gunplas.append({
            "id": row["id"],
            "title": row["title"],
            "owned": bool(row["owned"])
        })
    return gunplas

# 2. 追加 (POST /gunplas)
@app.post("/gunplas")
def create_gunpla(gunpla: GunplaCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO gunplas (title, owned) VALUES (?, 0)",
        (gunpla.title,)
    )
    conn.commit()
    gunpla_id = cursor.lastrowid
    conn.close()
    
    return {"id": gunpla_id, "title": gunpla.title, "owned": False}

# 3. 状態更新 (PUT /gunplas/{id})
@app.put("/gunplas/{id}")
def update_gunpla(id: int, gunpla: GunplaUpdate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE gunplas SET owned = ? WHERE id = ?",
        (1 if gunpla.owned else 0, id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Gunpla not found")
    conn.commit()
    conn.close()
    return {"id": id, "owned": gunpla.owned}

# 4. 削除 (DELETE /gunplas/{id})
@app.delete("/gunplas/{id}")
def delete_gunpla(id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gunplas WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Gunpla not found")
    conn.commit()
    conn.close()
    return {"message": "Deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
if __name__ == "__main__":
    # host="0.0.0.0" で外部からのアクセスも受け付ける。ポート8000で待ち受ける
    uvicorn.run(app, host="0.0.0.0", port=8000)
