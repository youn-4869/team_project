import tkinter as tk
import random
from tkinter import messagebox

# 색상 테마
BG_COLOR = "#CCFFCC"
BUTTON_COLOR = "#66CC99"
HIGHLIGHT_COLOR = "#99FFCC"

# 전역 변수
buttons = []
target_indexes = []
user_clicks = []

# 게임 초기화
def reset_game():
    global target_indexes, user_clicks
    user_clicks = []
    target_indexes = random.sample(range(9), 3)  # 3칸만 깜빡이게
    flash_targets()

# 타겟 위치 깜빡이기
def flash_targets():
    for i, idx in enumerate(target_indexes):
        root.after(i * 700, lambda idx=idx: flash_button(idx))

# 깜빡임 효과
def flash_button(index):
    btn = buttons[index]
    btn.config(bg=HIGHLIGHT_COLOR)
    root.after(400, lambda: btn.config(bg=BUTTON_COLOR))

# 유저 클릭
def button_click(index):
    global user_clicks

    if index in user_clicks:
        return  # 같은 곳 중복 클릭 방지

    user_clicks.append(index)

    if len(user_clicks) == len(target_indexes):
        check_result()

# 정답 확인
def check_result():
    if sorted(user_clicks) == sorted(target_indexes):
        messagebox.showinfo("정답!", "잘했어요! 다음 단계로~")
        reset_game()
    else:
        messagebox.showinfo("땡!", "틀렸어요! 다시 도전해봐요!")
        reset_game()

# 윈도우 생성
root = tk.Tk()
root.title("🧠 위치 기억 게임")
root.geometry("400x500")
root.configure(bg=BG_COLOR)

title = tk.Label(root, text="위치 기억 게임", font=("Helvetica", 24, "bold"),
                 bg=BG_COLOR, fg="#336633")
title.pack(pady=30)

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack()

# 3x3 버튼 만들기
for i in range(9):
    btn = tk.Button(frame, text=" ", width=8, height=4, bg=BUTTON_COLOR,
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

start_btn = tk.Button(root, text="게임 시작", font=("Helvetica", 16),
                      command=reset_game, bg="#A0E7A0")
start_btn.pack(pady=20)

# 실행
root.mainloop()
