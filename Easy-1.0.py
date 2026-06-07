import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import random
import string
import os

# メモリと状態の管理
variables = {}
last_if_condition = True
output_widget = None
SAVE_FILE_NAME = "my_code.txt"  # コードを保存するファイル名

# --- 多言語メッセージの設定 ---
LANG_TEXTS = {
    "日本語": {
        "title": "マスター自作言語エディタ", 
        "label": "コードを入力してください:", 
        "btn": "▶ 実行する", 
        "output": "実行結果:",
        "btn_save": "[保存する]",
        "btn_load": "[読み込む]",
        "btn_close": "❌ 終了",
        "sample": "入力 桁 = パスワードは何桁にする？\nパスワード 生成結果 = 桁\nアニメ 生成したパスワードは以下です：\n表示 生成結果\n音\n警告 完了しました！"
    },
    "English": {
        "title": "Master Custom Editor", 
        "label": "Enter Code:", 
        "btn": "▶ RUN", 
        "output": "Output:",
        "btn_save": "[Save Code]",
        "btn_load": "[Load Code]",
        "btn_close": "❌ CLOSE",
        "sample": "ask length = How many digits?\npassword res = length\ntype Password is:\nprint res\nbeep\nalert Done!"
    }
}

# --- 画面（GUI）の構築 ---
root = tk.Tk()
root.title("My Master Language App")
root.geometry("400x550")  # スマホの横画面でも収まるように高さを少しコンパクトに調整
APP_FONT = ("Helvetica", 11)

# 「保存」ボタンが押されたときの処理
def press_save_file():
    user_code = code_entry.get("1.0", tk.END).strip()
    try:
        with open(SAVE_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(user_code)
        lang = lang_combo.get()
        if lang == "日本語":
            messagebox.showinfo("成功", "コードをファイルに保存しました！")
        else:
            messagebox.showinfo("Success", "Code saved to file successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 「読み込み」ボタンが押されたときの処理
def press_load_file():
    if not os.path.exists(SAVE_FILE_NAME):
        lang = lang_combo.get()
        if lang == "日本語":
            messagebox.showwarning("注意", "保存されたコードファイルが見つかりません。")
        else:
            messagebox.showwarning("Warning", "Saved code file not found.")
        return
        
    try:
        with open(SAVE_FILE_NAME, "r", encoding="utf-8") as f:
            content = f.read()
        code_entry.delete("1.0", tk.END)
        code_entry.insert("1.0", content)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 「終了」ボタンが押されたときの処理
def press_close_app():
    root.destroy()

# 言語が切り替わったときの処理
def on_language_change(event=None):
    lang = lang_combo.get()
    text = LANG_TEXTS[lang]
    root.title(text["title"])
    label_code.config(text=text["label"])
    btn_run.config(text=text["btn"])
    label_out.config(text=text["output"])
    
    # 各種ボタンのテキストを文字化けしない安全なテキストに更新
    btn_save_file.config(text=text["btn_save"])
    btn_load_file.config(text=text["btn_load"])
    btn_close.config(text=text["btn_close"])
    
    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", text["sample"])

# 最上段のレイアウト枠
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=5)

lang_combo = ttk.Combobox(
    frame_top, 
    values=list(LANG_TEXTS.keys()), 
    state="readonly", 
    width=8, 
    font=APP_FONT
)
lang_combo.set("日本語")
lang_combo.pack(side="left")
lang_combo.bind("<<ComboboxSelected>>", on_language_change)

# 保存ボタンと読み込みボタン（上段に配置）
btn_save_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bg="#e1f5fe", command=press_save_file)
btn_save_file.pack(side="left", padx=5)

btn_load_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bg="#efebe9", command=press_load_file)
btn_load_file.pack(side="left", padx=5)

# メインコード入力欄
label_code = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_code.pack(fill="x", padx=10, pady=(5, 2))
code_entry = tk.Text(root, height=8, font=APP_FONT) # 縦幅を少しコンパクトに調整
code_entry.pack(fill="both", expand=True, padx=10, pady=2)

# --- 自作言語の処理エンジン ---
def run_my_language(code):
    global variables, last_if_condition
    lines = code.split("\n")
    outputs = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # [COMMAND] 消去
        if line in ["消去", "clear"]:
            outputs = ["CLEAR_SIGNAL"]
            continue

        # [COMMAND] 音
        if line in ["音", "beep"]:
            root.bell()
            outputs.append("[BEEP] Sound played")
            continue

        # [COMMAND] アプリ終了
        if line in ["アプリ終了", "close"]:
            root.destroy()
            return "CLOSED"

        # [COMMAND] 警告
        if any(line.startswith(cmd + " ") for cmd in ["警告", "alert"]):
            _, msg = line.split(" ", 1)
            msg_val = str(evaluate_expression(msg.strip()))
            messagebox.showwarning("Alert / 警告", msg_val)
            outputs.append(f"[ALERT] Showed: {msg_val}")
            continue

        # [COMMAND] アニメ
        if any(line.startswith(cmd + " ") for cmd in ["アニメ", "type"]):
            _, msg = line.split(" ", 1)
            msg_val = str(evaluate_expression(msg.strip()))
            outputs.append(f"__TYPE_EFFECT__:{msg_val}")
            continue

        # [COMMAND] 待つ
        if any(line.startswith(cmd + " ") for cmd in ["待つ", "wait"]):
            _, sec_str = line.split(" ", 1)
            sec = float(evaluate_expression(sec_str.strip()))
            time.sleep(sec)
            outputs.append(f"[WAIT] {sec} sec")
            continue

        # [COMMAND] 乱数
        if any(line.startswith(cmd + " ") for cmd in ["乱数", "rand"]):
            _, rest = line.split(" ", 1)
            var_name, range_str = rest.split("=", 1)
            min_val, max_val = range_str.strip().split()
            rand_res = random.randint(int(min_val), int(max_val))
            variables[var_name.strip()] = rand_res
            outputs.append(f"[RAND] {var_name.strip()} = {rand_res}")
            continue

        # [COMMAND] 入力
        if any(line.startswith(cmd + " ") for cmd in ["入力", "ask"]):
            _, rest = line.split(" ", 1)
            var_name, prompt_str = rest.split("=", 1)
            user_res = simpledialog.askstring("Input", prompt_str.strip())
            if user_res is None: user_res = ""
            try: variables[var_name.strip()] = int(user_res)
            except: variables[var_name.strip()] = user_res
            outputs.append(f"[INPUT] {var_name.strip()} = {user_res}")
            continue

        # [COMMAND] 合体
        if any(line.startswith(cmd + " ") for cmd in ["合体", "join"]):
            _, rest = line.split(" ", 1)
            var_name, parts_str = rest.split("=", 1)
            parts = parts_str.strip().split()
            combined = ""
            for part in parts:
                if part in variables: combined += str(variables[part])
                else: combined += str(part)
            variables[var_name.strip()] = combined
            outputs.append(f"[JOIN] {var_name.strip()} = {combined}")
            continue

        # [COMMAND] パスワード
        if any(line.startswith(cmd + " ") for cmd in ["パスワード", "password"]):
            _, rest = line.split(" ", 1)
            var_name, length_str = rest.split("=", 1)
            length = int(evaluate_expression(length_str.strip()))
            chars = string.ascii_letters + string.digits
            pw = "".join(random.choice(chars) for _ in range(length))
            variables[var_name.strip()] = pw                
            outputs.append(f"[PASSWORD] {var_name.strip()} = {pw}")
            continue

        # [COMMAND] 保存
        if any(line.startswith(cmd + " ") for cmd in ["保存", "let"]):
            _, expr = line.split(" ", 1)
            var_name, var_expr = expr.split("=", 1)
            result = evaluate_expression(var_expr.strip())
            variables[var_name.strip()] = result
            outputs.append(f"[SAVE] {var_name.strip()} = {result}")
            continue

        # [COMMAND] 表示 / 応援
        if any(line.startswith(cmd + " ") for cmd in ["表示", "print"]):
            _, expr = line.split(" ", 1)
            result = evaluate_expression(expr.strip())
            outputs.append(str(result))
            continue
        if any(line.startswith(cmd + " ") for cmd in ["応援", "cheer"]):
            _, expr = line.split(" ", 1)
            result = evaluate_expression(expr.strip())
            outputs.append(f"[CHEER] >>> {result} <<<")
            continue

    return "\n".join(outputs)

# 式の計算
def evaluate_expression(expr):
    if str(expr) in variables:
        return variables[str(expr)]
    for op in ["+", "-", "*", "/"]:
        if op in str(expr):
            expr = str(expr).replace(op, f" {op} ")
    tokens = str(expr).split()
    if not tokens: return expr
    try:
        first_token = tokens[0]
        result = variables[first_token] if first_token in variables else int(first_token)
        i = 1
        while i < len(tokens):
            op = tokens[i]
            next_token = tokens[i+1]
            next_val = variables[next_token] if next_token in variables else int(next_token)
            if op == "+": result += next_val
            elif op == "-": result -= next_val
            elif op == "*": result *= next_val
            elif op == "/": result = result // next_val
            i += 2
        return result
    except: return expr

# アニメーション処理（テキストを1文字ずつ出すための関数群）
def process_output_lines(lines_list, line_idx=0):
    if line_idx >= len(lines_list): return
    current_line = lines_list[line_idx]
    if current_line.startswith("__TYPE_EFFECT__:"):
        text_to_type = current_line.replace("__TYPE_EFFECT__:", "") + "\n"
        animate_text_char(text_to_type, 0, lines_list, line_idx)
    else:
        output_widget.config(state="normal")
        output_widget.insert(tk.END, current_line + "\n")
        output_widget.config(state="disabled")
        process_output_lines(lines_list, line_idx + 1)

def animate_text_char(text_str, char_idx, lines_list, line_idx):
    if char_idx < len(text_str):
        output_widget.config(state="normal")
        output_widget.insert(tk.END, text_str[char_idx])
        output_widget.config(state="disabled")
        root.after(50, lambda: animate_text_char(text_str, char_idx + 1, lines_list, line_idx))
    else:
        process_output_lines(lines_list, line_idx + 1)

def press_run():
    global output_widget
    user_code = code_entry.get("1.0", tk.END)
    result = run_my_language(user_code)
    if result == "CLOSED": return
    
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    
    if result == "CLEAR_SIGNAL":
        output_widget.config(state="disabled")
        return
        
    output_lines = result.split("\n")
    process_output_lines(output_lines, 0)

# --- 下段のGUIコンポーネント配置（横並びフレーム） ---
frame_actions = tk.Frame(root)
frame_actions.pack(fill="x", padx=10, pady=1)

# 1. 実行ボタン
btn_run = tk.Button(frame_actions, text="", font=APP_FONT, bg="lightblue", height=1, command=press_run)
btn_run.pack(side="left", fill="x", expand=True, padx=(0, 5))

# 2. 終了ボタン
btn_close = tk.Button(frame_actions, text="", font=APP_FONT, bg="#ffebee", height=1, command=press_close_app)
btn_close.pack(side="right", padx=(5, 0))

# 3. 実行結果のタイトルラベル
label_out = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_out.pack(fill="x", padx=10, pady=0)

# 4. 実行結果を表示する出力エリア（はみ出さないように高さを「2行分」にスリム化）
output_widget = tk.Text(root, height=2, font=APP_FONT, state="disabled")
output_widget.pack(fill="x", padx=10, pady=1)

# 【はみ出し対策】上のメインコード入力欄の高さも4行分にキュッと縮める設定
code_entry.config(height=4)

# 初期言語設定の反映とメインループ開始
on_language_change()
root.mainloop()
