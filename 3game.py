import tkinter as tk
import random
from tkinter import messagebox

# 💜 색상 테마
BG_COLOR = "#E6E6FA"
TEXT_COLOR = "#4B0082"
INPUT_COLOR = "#D8BFD8"
BUTTON_COLOR = "#9370DB"

# 📂 단어 파일 불러오기
def load_words(filepath="words_30000.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        messagebox.showerror("에러", f"{filepath} 파일을 찾을 수 없어요!")
        return []

# 📚 단어 리스트
all_words = load_words()

# 🎮 게임 상태
level = 1
max_level = 5
selected_words = []

# 🌟 단어 보여주기
def show_words():
    global selected_words
    selected_words = random.sample(all_words, level)
    word_label.config(text="  ".join(selected_words))
    entry.delete(0, tk.END)
    root.after(2000, hide_words)

# ❓ 단어 가리기
def hide_words():
    word_label.config(text="❓ " * level)

# ✅ 정답 확인
def check_answer():
    global level
    user_input = entry.get().strip().split()
    if user_input == selected_words:
        if level < max_level:
            level_up()
        else:
            messagebox.showinfo("🎉 완벽!", "5단계까지 모두 성공했어요! 최고!")
            reset_game()
    else:
        messagebox.showinfo("틀렸어요!", f"정답은: {' '.join(selected_words)}\n1단계부터 다시 시작해요~")
        reset_game()

# 🔼 다음 단계로
def level_up():
    global level
    level += 1
    messagebox.showinfo("정답!", f"{level}단계로 넘어갑니다~")
    show_words()

# ♻️ 게임 리셋
def reset_game():
    global level
    level = 1
    show_words()

# 🪟 GUI 구성
root = tk.Tk()
root.title("🧠 단계별 단어 기억 게임")
root.geometry("550x400")
root.configure(bg=BG_COLOR)

title = tk.Label(root, text="단계별 단어 기억 게임", font=("Helvetica", 20, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR)
title.pack(pady=30)

word_label = tk.Label(root, text="", font=("Helvetica", 28, "bold"),
                      bg=BG_COLOR, fg=TEXT_COLOR)
word_label.pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 18), justify="center", bg=INPUT_COLOR)
entry.pack(pady=10)

check_btn = tk.Button(root, text="입력 완료", font=("Helvetica", 16),
                      bg=BUTTON_COLOR, fg="white", command=check_answer)
check_btn.pack(pady=10)

start_btn = tk.Button(root, text="게임 시작", font=("Helvetica", 16),
                      bg="#BA55D3", fg="white", command=reset_game)
start_btn.pack(pady=20)

root.mainloop()