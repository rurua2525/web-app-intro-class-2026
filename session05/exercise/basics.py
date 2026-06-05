"""
第5回 実習3: Pythonスクリプトの作成

スライドの手順に従って、このファイルを編集してください。
  1. TODOリスト（辞書のリスト）を定義する
  2. show_todos 関数を実装する
  3. show_todos(todos) を呼び出す

実行方法:
  python basics.py

期待される出力例:
  [ ] 1: 課題を出す
  [x] 2: 買い物する
  [ ] 3: 自分のTODO
"""

# ヒント: TODOリストを作成する
todos = [
    {"id": 1, "title": "課題を出す", "done": False},
    {"id": 2, "title": "買い物する", "done": True},
    {"id": 3, "title": "自分のTODO", "done": False},
]

# show_todos 関数を実装する
def show_todos(todo_list):
    for todo in todo_list:
        status = "[x]" if todo["done"] else "[ ]"
        print(f"'{status} {todo['id']}: {todo['title']}'")

# show_todos(todos) を呼び出す
show_todos(todos)

@app.get("/hello/{松﨑}")
def hello(name: str):
return {"message": f"こんにちは、{松﨑}さん！"}

{
"id": 1,
"title": "レポートを書く"
,
"done": false
}

todos = [
  {"id": 1,"title": "レポートを書く","done": False},
  {"id": 2,"title": "買い物に行く","done": True},
  {"id": 3,"title": "自分のTODOを追加","done": False},
]


@app.get("/todos")
def get_todos():
  return todos


@app.get("/todos")
def get_todo(id):
    index = int(id) - 1
    return todos[index]
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)