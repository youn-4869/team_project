import tkinter as tk
import random
import time
from tkinter import messagebox

# 색상 테마
BG_COLOR = "#FFFACD"  # Lemon Chiffon (연노랑 배경)
BUTTON_COLOR = "#FFD700"  # Gold
FLASH_COLOR = "#FFFF00"   # 밝은 노랑

# 전역 변수
sequence = []       # 정답 순서
user_input = []     # 유저가 누른 순서
buttons = []        # 버튼들

# 순서 리셋
def reset_game():
    global sequence, user_input
    sequence = []
    user_input = []
    generate_sequence()

# 순서 생성 및 깜빡이기
def generate_sequence():
    global sequence
    new_index = random.randint(0, 3)
    sequence.append(new_index)
    flash_sequence()

# 버튼 깜빡임 (순차적으로)
def flash_sequence():
    for i, idx in enumerate(sequence):
        root.after(1000 * i, lambda idx=idx: flash_button(idx))

# 깜빡이는 효과 (밝은 색 → 원래 색)
def flash_button(index):
    btn = buttons[index]
    btn.config(bg=FLASH_COLOR)
    root.after(500, lambda: btn.config(bg=BUTTON_COLOR))

# 유저가 버튼 클릭했을 때
def button_click(index):
    global user_input
    user_input.append(index)

    if user_input[len(user_input) - 1] != sequence[len(user_input) - 1]:
        messagebox.showinfo("결과", "틀렸어요! 다시 도전해보세요!")
        reset_game()
        return

    if len(user_input) == len(sequence):
        messagebox.showinfo("결과", "정답입니다! 다음 단계로~")
        user_input = []
        generate_sequence()

# 메인 윈도우
root = tk.Tk()
root.title("🧩 순서 기억 게임")
root.geometry("400x500")
root.configure(bg=BG_COLOR)

# 타이틀
title = tk.Label(root, text="순서 기억 게임", font=("Helvetica", 24, "bold"),
                 bg=BG_COLOR, fg="#8B8000")
title.pack(pady=30)

# 버튼 프레임
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack()

# 4개 버튼 생성
for i in range(4):
    btn = tk.Button(frame, text=f"{i+1}", font=("Helvetica", 18, "bold"),
                    bg=BUTTON_COLOR, width=10, height=4,
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    buttons.append(btn)

# 시작 버튼
start_btn = tk.Button(root, text="게임 시작", font=("Helvetica", 16),
                      command=reset_game, bg="#FFEC8B", fg="black")
start_btn.pack(pady=20)

# 실행
root.mainloop()
