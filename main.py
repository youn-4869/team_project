import tkinter as tk
from tkinter import messagebox
import subprocess 

# 색상 테마
BACKGROUND_COLOR = "#F0F8FF"  # Alice Blue
BUTTON_COLOR = "#87CEEB"      # Sky Blue
TEXT_COLOR = "#003366"        # 진한 파랑

def start_order_game():
    subprocess.Popen(["python", "1game.py"])  # 순서 기억 게임 실행

def start_position_game():
    subprocess.Popen(["python", "2game.py"]) # 위치 기억 게임 실행


def start_word_game():
    subprocess.Popen(["python", "3game.py"])# 단어 기억 게임 실행



# 메인 윈도우 생성
root = tk.Tk()
root.title("기억해해!GAME")
root.geometry("500x400")
root.configure(bg=BACKGROUND_COLOR)

# 타이틀
title = tk.Label(root, text="🧠 기억해!GAME 🧠", font=("Helvetica", 24, "bold"),
                 fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
title.pack(pady=30)

# 버튼 스타일
def make_button(text, command):
    return tk.Button(root, text=text, command=command,
                     font=("Helvetica", 16), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                     activebackground="#B0E0E6",  # 버튼 누를 때 색
                     width=25, height=2)

# 게임 버튼
btn1 = make_button("🧩 순서 기억 게임", start_order_game)
btn2 = make_button("🧠 위치 기억 게임", start_position_game)
btn3 = make_button("🔤 단어 기억 게임", start_word_game)

btn1.pack(pady=10)
btn2.pack(pady=10)
btn3.pack(pady=10)

# 실행
root.mainloop()
