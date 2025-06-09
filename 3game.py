import tkinter as tk
import random
import time
import os
import json
from datetime import datetime
from tkinter import messagebox

# 💜 색상 테마
BG_COLOR = "#E6E6FA"
TEXT_COLOR = "#4B0082"
INPUT_COLOR = "#D8BFD8"
BUTTON_COLOR = "#9370DB"

# 📂 단어 파일 불러오기
def load_words(filepath="team_project/words_30000.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        messagebox.showerror("에러", f"{filepath} 파일을 찾을 수 없어요!")
        return []

# 📁 통계 저장 파일 경로
stats_file = "game_stats.json"

# 📊 통계 로딩
def load_stats():
    if os.path.exists(stats_file):
        with open(stats_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"plays": 0, "correct": 0, "incorrect": 0, "best_time": None, "last_play": None}

# 📊 통계 저장
def save_stats(stats):
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

# 📚 단어 리스트
all_words = load_words()

# 🎮 게임 상태
level = 1
max_level = 5
selected_words = []
start_time = 0

# 🌟 단어 보여주기
def show_words():
    global selected_words, start_time
    selected_words = random.sample(all_words, level)
    word_label.config(text="  ".join(selected_words))
    entry.delete(0, tk.END)
    root.after(2000, hide_words)
    start_time = time.time()

# ❓ 단어 가리기
def hide_words():
    word_label.config(text="❓ " * level)

# ✅ 정답 확인 및 시간 체크
def check_answer():
    global level, start_time
    user_input = entry.get().strip().split()
    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    stats = load_stats()
    stats["plays"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if elapsed > 10:
        messagebox.showinfo("시간 초과!", f"10초 초과! ({elapsed}초 소요됨)\n1단계부터 다시 시작해요~")
        stats["incorrect"] += 1
        save_stats(stats)
        reset_game()
        return

    if user_input == selected_words:
        stats["correct"] += 1
        if stats["best_time"] is None or elapsed < stats["best_time"]:
            stats["best_time"] = elapsed
            message = f"🎉 정답입니다! ({elapsed}초)\n🔥 최고 기록 갱신!"
        else:
            message = f"🎉 정답입니다! ({elapsed}초)"

        save_stats(stats)

        if level < max_level:
            level_up(message)
        else:
            messagebox.showinfo("🎉 완벽!", f"5단계까지 모두 성공했어요! 최고!\n총 시도: {stats['plays']}번, 정답률: {stats['correct']}/{stats['plays']}")
            reset_game()
    else:
        stats["incorrect"] += 1
        save_stats(stats)
        messagebox.showinfo("틀렸어요!", f"정답은: {' '.join(selected_words)}\n{elapsed}초 소요됨\n1단계부터 다시 시작해요~")
        reset_game()

# 🔼 다음 단계로
def level_up(msg):
    global level
    level += 1
    messagebox.showinfo("정답!", f"{msg}\n{level}단계로 넘어갑니다~")
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
