import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import base64

# === OpenRouter API 설정 ===
API_KEY = "API_키를_입력해주세요"
MODEL_NAME = "moonshotai/kimi-vl-a3b-thinking:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter_api(image_path):
    # 이미지 base64 인코딩
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지를 시각장애인이 이해할 수 있도록 묘사해줘."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    print("🔵 응답 내용:\n", response.text)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            return "응답 파싱에 실패했어요 😥"
    else:
        return f"API 호출 실패: {response.status_code} - {response.text}"

# === GUI 구성 ===
def select_image():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if path:
        load_image(path)
        description_text.set("이미지 설명을 생성 중입니다...")
        root.update()
        description = call_openrouter_api(path)
        description_text.set(description)

def load_image(path):
    img = Image.open(path)
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# === 창 설정 ===
root = tk.Tk()
root.title("시각장애인을 위한 이미지 묘사")
root.geometry("600x700")
root.configure(bg="#B0E0E6")

tk.Label(root, text="이미지 묘사 프로그램", font=("Helvetica", 22, "bold"), bg="#B0E0E6", fg="#003366").pack(pady=20)
tk.Button(root, text="이미지 선택하기", command=select_image, font=("Helvetica", 16), bg="#4682B4", fg="white").pack(pady=10)

image_label = tk.Label(root, bg="#B0E0E6")
image_label.pack(pady=20)

description_text = tk.StringVar()
tk.Label(root, textvariable=description_text, wraplength=550, font=("Helvetica", 15), bg="#B0E0E6", fg="#003366", justify="left").pack(pady=20)

root.mainloop()
