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
countdown_seconds = 10
countdown_id = None

# 호출 버튼 가능 발견 모드 게임 시작 구현보다
def show_words():
    global selected_words, start_time
    show_time = 2000 + (level - 1) * 1000  # 단계별로 1초씩 증가
    selected_words = random.sample(all_words, level)
    word_label.config(text="  ".join(selected_words))
    entry.delete(0, tk.END)
    entry.config(state="disabled")
    check_btn.pack_forget()
    root.after(show_time, hide_words)
    start_time = time.time()
    start_btn.pack_forget()

# ❓ 단어 가리기
def hide_words():
    entry.delete(0, tk.END)
    input_time = countdown_seconds + (level - 1) * 2  # 단계별로 2초씩 증가
    word_label.config(text="❓ " * level)
    entry.config(state="normal")
    check_btn.pack(pady=10)
    start_countdown(input_time)

# ⏱️ 시간 타임머 시작
def start_countdown(seconds):
    global countdown_id
    timer_label.config(text=f"남은 시간: {seconds} 초")
    if seconds > 0:
        countdown_id = root.after(1000, start_countdown, seconds - 1)
    else:
        handle_timeout()

# ❌ 시간 마감 처리
def handle_timeout():
    stats = load_stats()
    stats["plays"] += 1
    stats["incorrect"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_stats(stats)
    messagebox.showinfo("시간 초과!", f"{countdown_seconds}초 초과!")
    reset_game()

# ✅ 정답 확인 및 시간 체크
def check_answer():
    global level, start_time, countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)

    entry.config(state="disabled")
    check_btn.pack_forget()

    user_input = entry.get().strip().split()
    end_time = time.time()
    elapsed = round(end_time - start_time - 3, 2)

    stats = load_stats()
    stats["plays"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user_input == selected_words:
        stats["correct"] += 1
        if stats["best_time"] is None or elapsed < stats["best_time"]:
            stats["best_time"] = elapsed
            message = f"🎉 정답입니다! ({elapsed}초)\n🔥 최고 기본 기록 갱신!"
        else:
            message = f"🎉 정답입니다! ({elapsed}초)"

        save_stats(stats)

        if level < max_level:
            level_up(message)
        else:
            messagebox.showinfo("🎉 완료!", f"5단계까지 모두 성공했어요! \n총 시도: {stats['plays']} 번, 정답률: {stats['correct']}/{stats['plays']}")
            reset_game()
    else:
        stats["incorrect"] += 1
        save_stats(stats)
        messagebox.showinfo("틀렸어요ㅜㅜ", f"정답은: {' '.join(selected_words)}\n{elapsed}초 소요됨\n1단계부터 다시 시작해요~")
        reset_game()

# 🔼 다음 단계로
def level_up(msg):
    global level
    level += 1
    messagebox.showinfo("정답!", f"{msg}{level}단계로 넘어갑니다~")
    entry.delete(0, tk.END)  # 확인 후 입력창 비우기
    show_words()

# ♻️ 게임 리셋
def reset_game():
    global level, countdown_id
    level = 1
    if countdown_id:
        root.after_cancel(countdown_id)
        countdown_id = None
    timer_label.config(text="")
    entry.delete(0, tk.END)  # 입력창 초기화
    entry.config(state="disabled")
    check_btn.pack_forget()
    start_btn.pack(pady=10)
    show_words()

# 🪟 GUI 구성
root = tk.Tk()
root.title("🧐 단계별 단어 기억 게임")
root.geometry("550x420")
root.configure(bg=BG_COLOR)

title = tk.Label(root, text="단계별 단어 기억 게임", font=("Helvetica", 20, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR)
title.pack(pady=10)

word_label = tk.Label(root, text="", font=("Helvetica", 28, "bold"),
                      bg=BG_COLOR, fg=TEXT_COLOR)
word_label.pack(pady=10)

timer_label = tk.Label(root, text="", font=("Helvetica", 16), bg=BG_COLOR, fg="red")
timer_label.pack(pady=5)

entry = tk.Entry(root, font=("Helvetica", 18), justify="center", bg=INPUT_COLOR, state="disabled")
entry.pack(pady=10)

check_btn = tk.Button(root, text="입력 완료", font=("Helvetica", 16),
                      bg=BUTTON_COLOR, fg="white", command=check_answer)

start_btn = tk.Button(root, text="게임 시작", font=("Helvetica", 16),
                      bg="#BA55D3", fg="white", command=reset_game)
start_btn.pack(pady=10)

root.mainloop()
