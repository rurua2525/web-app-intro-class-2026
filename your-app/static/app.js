// APIのURLを /todos から /gunplas に変更
const API_URL = "/gunplas";

// 画面の要素を取得
const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

// ページが読み込まれたら一覧を取得して表示する
window.addEventListener("DOMContentLoaded", () => {
    fetchGunplas();
});

// ガンプラ一覧をサーバーから取得して画面に描画する
async function fetchGunplas() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("データの取得に失敗しました");
        const gunplas = await response.json();
        
        todoList.innerHTML = "";
        gunplas.forEach(gunpla => {
            renderGunpla(gunpla);
        });
    } catch (error) {
        console.error(error);
        alert("エラーが発生しました");
    }
}

// フォームが送信されたとき（新しいガンプラを追加する）
todoForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // ページの再読み込みを防ぐ
    const title = todoInput.value.trim();
    if (!title) return;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title })
        });

        if (!response.ok) throw new Error("追加に失敗しました");
        const newGunpla = await response.json();

        renderGunpla(newGunpla);
        todoInput.value = ""; // 入力欄を空にする
    } catch (error) {
        console.error(error);
        alert("追加に失敗しました");
    }
});

// ガンプラを1件分画面に描画する関数
function renderGunpla(gunpla) {
    const li = document.createElement("li");
    li.className = "todo-item";
    if (gunpla.owned) {
        li.classList.add("completed");
    }

    // チェックボックス (owned)
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = gunpla.owned;
    checkbox.addEventListener("change", () => {
        toggleGunpla(gunpla.id, checkbox.checked, li);
    });

    // タイトル (XSS対策のため textContent を使用)
    const span = document.createElement("span");
    span.className = "todo-title";
    span.textContent = gunpla.title;

    // 削除ボタン
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "削除";
    deleteButton.className = "delete-button";
    deleteButton.addEventListener("click", () => {
        deleteGunpla(gunpla.id, li);
    });

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteButton);
    todoList.appendChild(li);
}

// 所有状態（owned）を更新する
async function toggleGunpla(id, owned, li) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ owned: owned })
        });

        if (!response.ok) throw new Error("更新に失敗しました");

        if (owned) {
            li.classList.add("completed");
        } else {
            li.classList.remove("completed");
        }
    } catch (error) {
        console.error(error);
        alert("更新に失敗しました");
        // エラー時はチェックボックスの状態を元に戻す
        const checkbox = li.querySelector("input[type='checkbox']");
        checkbox.checked = !owned;
    }
}

// ガンプラを削除する
async function deleteGunpla(id, li) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("削除に失敗しました");
        li.remove();
    } catch (error) {
        console.error(error);
        alert("削除に失敗しました");
    }
}
