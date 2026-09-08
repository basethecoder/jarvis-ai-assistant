import requests
import os
import tkinter as tk
from tkinter import simpledialog
import threading
import edge_tts
import asyncio
from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
import uuid

AUDIO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reply.mp3")
    
def jarvis_respond(command,original_text):
    if command == "check BMI":
        weight = ask_value("check BMI","กรอกน้ำหนัก (กก.): ","float")
        height = ask_value("check BMI","กรอกส่วนสูง (ม.): ","float")
        if weight is None or height is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "check BMI", "weight": weight, "height": height})
        return response.json()["reply"]
    elif command == "บอกเวลาตอนนี้":
        return"ขณะนี้ยังไม่รู้เวลาครับ จะเพิ่มระบบให้ทีหลัง"
    elif command == "ชื่ออะไร":
        return"ผมชื่อ Jarvis ครับ"
    elif command == "เพิ่มงาน":
        homework = ask_value("เพิ่มงาน","งานคืออะไรครับ: ")
        if homework is None:
            return "ยกเลิกการเพิ่มงานแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "เพิ่มงาน", "homework":homework})
        return response.json()["reply"]
    elif command == "ลบงาน":
        deletehomework = ask_value("ลบงาน","ลบงานอะไรครับ: ")
        if deletehomework is None:
            return "ยกเลิกการลบงานแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ลบงาน", "deletehomework":deletehomework})
        return response.json()["reply"]
    elif command == "ลบงานทั้งหมด":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ลบงานทั้งหมด"})
        return response.json()["reply"]
    elif command == "ดูงาน":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ดูงาน"})
        return response.json()["reply"]
    elif command == "บันทึกข้อมูล":
        name = ask_value("บันทึกข้อมูล","กรอกชื่อของคุณ(ชื่อเล่น): ")
        age = ask_value("บันทึกข้อมูล","กรอกอายุของคุณ(ปี): ","integer")
        height = ask_value("บันทึกข้อมูล","กรอกส่วนสูงของ(ม.): ","float")
        if name is None or age is None or height is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "บันทึกข้อมูล", "name":name, "age":age, "height":height})
        return response.json()["reply"]
    elif command == "ข้อมูลของฉัน":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ข้อมูลของฉัน"})
        return response.json()["reply"]
    elif command == "สวัสดี":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "สวัสดี"})
        return response.json()["reply"]
    elif command == "ลบข้อมูล":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ลบข้อมูล"})
        return response.json()["reply"]
    elif command == "เพิ่มผู้ติดต่อ":
        name = ask_value("เพิ่มผู้ติดต่อ","กรอกชื่อของคุณ(ชื่อเล่น): ")
        phone = ask_value("เพิ่มผู้ติดต่อ","กรอกเบอร์ของคุณ: ")
        if name is None or phone is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "เพิ่มผู้ติดต่อ", "name":name, "phone":phone})
        return response.json()["reply"]
    elif command == "ดูผู้ติดต่อ":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ดูผู้ติดต่อ"})
        return response.json()["reply"]
    elif command == "ค้นหาผู้ติดต่อ":
        name = ask_value("ค้นหาผู้ติดต่อ","กรอกชื่อที่จะค้นหา(ชิ่อเล่น): ")
        if name is None:
            return "ยกเลิกการค้นหาผู้ติดต่อแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ค้นหาผู้ติดต่อ", "name":name})
        return response.json()["reply"]
    elif command == "แก้ไขผู้ติดต่อ":
        traget_name = ask_value("แก้ไขผู้ต่อ","กรอกชื่อผู้ติดต่อที่คุณจะแก้ไข: ")
        if traget_name is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        new_name = ask_value("ชื่อใหม่","กรอกชื่อใหม่: ")
        new_phone = ask_value("เบอร์ใหม่","กรอกเบอร์ใหม่: ")
        if new_name is None or new_phone is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "แก้ไขผู้ติดต่อ", "traget_name":traget_name, "new_name": new_name, "new_phone": new_phone})
        return response.json()["reply"]
    elif command == "เซฟข้อมูล":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "เซฟข้อมูล"})
        return response.json()["reply"]
    elif command == "โหลดข้อมูล":
        response = requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "โหลดข้อมูล"})
        return response.json()["reply"]
    elif command == "ทายอายุ":
        name = ask_value("ทายอายุ","กรอกชื่อภาษาอังกฤษที่คุณจะทาย: ")
        if name is None:
            return "ยกเลิกการกรอกข้อมูลแล้วครับ"
        response= requests.post("http://127.0.0.1:5000/chat",
                                json={"intent": "ทายอายุ", "name":name})
        return response.json()["reply"]
    else:
        return ask_ai(original_text)
    
def ask_value(title, promt, ask_type="string"):
    if ask_type == "string":
        value = simpledialog.askstring(title, promt)
    elif ask_type == "float":
        value = simpledialog.askfloat(title, promt)
    elif ask_type == "integer":
        value = simpledialog.askinteger(title, promt)
    return value          

API_KEY = os.environ.get("MY_AI_KEY")
def ask_ai(question):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model":"claude-sonnet-5",
        "max_tokens": 300,
        "messages":[
            {"role":"user","content":question}
        ]
    }
    try:
        reponse = requests.post(url, headers=headers, json=body)
        data = reponse.json()
        return data["content"][0]["text"]
    except Exception as e:
        return "ขณะนี้ทางระบบมีปัญหา กรุณาลองใหม่อีกครั้งนะครับ"
    
def classify_intent(user_text):
    command = "check BMI, บอกเวลาตอนนี้, ชื่ออะไร, เพิ่มงาน, ลบงาน, ลบงานทั้งหมด, ดูงาน, บันทึกข้อมูล, ข้อมูลของฉัน, สวัสดี, ลบข้อมูล, เพิ่มผู้ติดต่อ, ดูผู้ติดต่อ, ค้นหาผู้ติดต่อ, แก้ไขผู้ติดต่อ, เซฟข้อมูล, โหลดข้อมูล, ทายอายุ"

    prompt = f"""คุณคือระบบจัดการหมวดหมู่คำสั่ง ตอบกลับด้วยชื่อคำสั่งที่ตรงที่สุดจากลิวต์นี้เท่านั้น: {command}

กฏ: ตอบแค่ชื่อคำสั่งเท่านั้น ห้ามมีคำอื่นปน ห้ามมีเครื่องหมายวรรคตอน ถ้าไม่ตรงกับคำสั่งไหนเลยให้ตอบว่า none

ข้อความผู้ใช้: "{user_text}" """
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-sonnet-5",
        "max_tokens": 20,
        "messages":[
            {"role": "user","content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        return data["content"][0]["text"]
    except Exception as e:
        return "none"

def speak(text):
    try:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"reply_{uuid.uuid4().hex}.mp3")
        asyncio.run(generate_speech(text, filename))
        playsound(filename)
    except Exception as e:
        print(f"พูดไม่ได้: {e}")

async def generate_speech(text, filename):
    communicate = edge_tts.Communicate(text, "th-TH-PremwadeeNeural")
    await communicate.save(filename)

def voice_input():
    mic_button.config(state="disabled")
    entry.config(state="disabled")
    button.config(state="disabled")
    status_label.config(text="🎙️ กำลังฟัง... พูดได้เลยครับ")
    threading.Thread(target=record_and_transcribe, daemon=True).start()

def record_and_transcribe():
    SAMPEL_RATE = 16000
    DURATION = 5
    try:
        recording = sd.rec(int(DURATION * SAMPEL_RATE), samplerate=SAMPEL_RATE, channels=1, dtype="int16")
        sd.wait()
        recognizer = sr.Recognizer()
        audio_data = sr.AudioData(recording.tobytes(), SAMPEL_RATE, 2)
        text = recognizer.recognize_google(audio_data, language="th-TH")
        Window.after(0, lambda: fill_and_send(text))
    except sr.UnknownValueError:
        Window.after(0, lambda: voice_error("ฟังไม่ออกครับ ลองพูดใหม่อีกครั้ง"))
    except Exception as e:
        Window.after(0, lambda: voice_error(f"กิดข้อผิดพลาด: {e}"))

def fill_and_send(text):
    mic_button.config(state="normal")
    entry.config(state="normal")
    button.config(state="normal")
    status_label.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, text)
    on_send()

def voice_error(msg):
    mic_button.config(state="normal")
    entry.config(state="normal")
    button.config(state="normal")
    status_label.config(text=msg)
    Window.after(2500, lambda: status_label.config(text=""))

def call_jarvis_async(user_text):
    intent = classify_intent(user_text)
    reply = jarvis_respond(intent, user_text)
    Window.after(0, lambda: show_reply(reply))

def on_send():
    user_text = entry.get()
    if user_text.strip() == "":
        return
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"คุณ: {user_text}\n", "user")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)
    entry.delete(0, tk.END)
    entry.config(state="disabled")
    button.config(state="disabled")
    start_loading_dots()
    threading.Thread(target=call_jarvis_async, args=(user_text,), daemon=True).start()

def on_enter_key(event):
    on_send()

# ---------- Loading dots ----------
loading_job = None
dots_count = 0

def start_loading_dots():
    global dots_count
    dots_count = 0
    animate_dots()

def animate_dots():
    global dots_count, loading_job
    dots_count = (dots_count % 3) + 1
    status_label.config(text="J.A.R.V.I.S กำลังคิด" + "." * dots_count)
    loading_job = Window.after(400, animate_dots)

def stop_loading_dots():
    global loading_job
    if loading_job:
        Window.after_cancel(loading_job)
        loading_job = None
    status_label.config(text="")

# ---------- Typing effect ----------
def show_reply(reply):
    stop_loading_dots()
    chat_box.config(state="normal")
    chat_box.insert(tk.END, "J.A.R.V.I.S: ", "bot")
    chat_box.config(state="disabled")
    type_char(reply, 0)

def type_char(text, i):
    if i < len(text):
        chat_box.config(state="normal")
        chat_box.insert(tk.END, text[i], "bot")
        chat_box.see(tk.END)
        chat_box.config(state="disabled")
        Window.after(15, lambda: type_char(text, i + 1))
    else:
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "\n\n")
        chat_box.config(state="disabled")
        entry.config(state="normal")
        button.config(state="normal")
        entry.focus()
        speak(text)

# ---------- Pulsing indicator ----------
pulse_colors = ["#00e5ff", "#00a8cc", "#5ec8f0", "#7fffff"]
pulse_index = 0

def animate_pulse():
    global pulse_index
    pulse_index = (pulse_index + 1) % len(pulse_colors)
    pulse_canvas.itemconfig(pulse_dot, fill=pulse_colors[pulse_index])
    Window.after(500, animate_pulse)

# ===== หน้าตาแอป =====
BG_COLOR = "#050d1a"        
CHAT_BG = "#0a1826"        
USER_COLOR = "#5ec8f0"      
BOT_COLOR = "#00e5ff"       
TEXT_COLOR = "#a8d8e8"      
ACCENT_COLOR = "#00c8ff"    

Window = tk.Tk()
Window.title("J.A.R.V.I.S")
Window.geometry("450x580")
Window.configure(bg=BG_COLOR)
Window.resizable(False, False)

header_frame = tk.Frame(Window, bg=BG_COLOR)
header_frame.pack(pady=(15, 0))

pulse_canvas = tk.Canvas(header_frame, width=14, height=14, bg=BG_COLOR, highlightthickness=0)
pulse_dot = pulse_canvas.create_oval(2, 2, 12, 12, fill=pulse_colors[0], outline="")
pulse_canvas.pack(side=tk.LEFT, padx=(0, 8))

header = tk.Label(header_frame, text="J.A.R.V.I.S", font=("Segoe UI", 18, "bold"),
                   bg=BG_COLOR, fg=ACCENT_COLOR)
header.pack(side=tk.LEFT)

# ===== Pack input_frame และ status_label ก่อน chat_frame =====
input_frame = tk.Frame(Window, bg=BG_COLOR)
input_frame.pack(side=tk.BOTTOM, padx=15, pady=(5, 15), fill=tk.X)

entry = tk.Entry(input_frame, font=("Segoe UI", 12), bg="#313244", fg=TEXT_COLOR,
                  insertbackground=TEXT_COLOR, bd=0)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
entry.bind("<Return>", on_enter_key)

mic_button = tk.Button(input_frame, text="🎙️", font=("Segoe UI", 11, "bold"),
                       bg="#313244", fg=TEXT_COLOR, bd=0, padx=15,
                       command=voice_input, cursor="hand2")
mic_button.pack(side=tk.RIGHT, padx=(0,8))

button = tk.Button(input_frame, text="ส่ง", font=("Segoe UI", 11, "bold"),
                    bg=ACCENT_COLOR, fg="#1e1e2e", bd=0, padx=20,
                    command=on_send, cursor="hand2")
button.pack(side=tk.RIGHT)

status_label = tk.Label(Window, text="", font=("Segoe UI", 9, "italic"),
                         bg=BG_COLOR, fg="#7f849c")
status_label.pack(side=tk.BOTTOM, padx=15, anchor="w")

# ===== chat_frame pack ทีหลังสุด ให้กินพื้นที่ที่เหลือทั้งหมด =====
chat_frame = tk.Frame(Window, bg=BG_COLOR)
chat_frame.pack(padx=15, pady=(10, 5), fill=tk.BOTH, expand=True)

chat_box = tk.Text(chat_frame, bg=CHAT_BG, fg=TEXT_COLOR, font=("Segoe UI", 11),
                    wrap=tk.WORD, bd=0, padx=10, pady=10, state="disabled")
chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box.config(yscrollcommand=scrollbar.set)

chat_box.tag_config("user", foreground=USER_COLOR, font=("Segoe UI", 11, "bold"))
chat_box.tag_config("bot", foreground=BOT_COLOR, font=("Segoe UI", 11, "bold"))

animate_pulse()
Window.mainloop()



