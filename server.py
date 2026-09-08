from flask import Flask, request
import json
import requests
from tkinter import simpledialog
app = Flask(__name__)

contacts = []
owner ={
    "name":"",
    "age": 0,
    "height": 0.0
}
todo_list = ["เรียนอังกฤษ","ออกกำลังกาย"]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    intent = data["intent"]
    print(f"ได้รับ intent: '{intent}'")
    print(f"ความยาว: {len(intent)}")
    
    if intent == "ชื่ออะไร":
        return {"reply": "ผมชื่อ Jarvis ครับ"}
    elif intent == "บอกเวลาตอนนี้":
        return{"reply": "ขณะนี้ยังไม่รู้เวลาครับ จะเพิ่มระบบให้ทีหลัง"}
    elif intent == "ลบงานทั้งหมด":
        result = clear_todo_list()
        return {"reply": result}
    elif intent == "ดูงาน":
        result = ""
        for i,งาน in enumerate(todo_list, 1):
            result += f"{i}. {งาน}\n"
        return {"reply": f"นี้คืองานทั้งหมดครับ\n{result}\nสู้ๆสำหรับการทำงานนะครับ"}
    elif intent == "ข้อมูลของฉัน":
        result = jarvis_recall()
        return {"reply": result}
    elif intent == "สวัสดี":
        if owner["name"] == "":
            return {"reply": "ยังไม่รู้จักเจ้าของครับ กรุณาบันทึกข้อมูลของคุรก่อนนะครับ"}
        else:
            return {"reply": f"สวัสดีครับ คุณ {owner['name']} มีอะไรให้รับใช้ครับ"}
    elif intent == "ลบข้อมูล":
        owner["name"] = ""
        owner["age"] = 0
        owner["height"] = 0.0
        return {"reply": "ลบข้อมูลเรียบร้อยแล้วครับ"}
    elif intent == "ดูผู้ติดต่อ":
        result = jarvisshow_contact()
        return {"reply": result}
    elif intent == "เซฟข้อมูล":
        result = save_data()
        return {"reply": result}
    elif intent == "โหลดข้อมูล":
        result = load_data()
        return {"reply": result}
    elif intent == "เพิ่มงาน":
        homework = data["homework"]
        todo_list.append(homework)
        return {"reply": f"เพิ่มงาน {homework} แล้วครับ"}
    elif intent == "check BMI":
        weight = data["weight"]
        height = data["height"]
        return {"reply": check_BMI(weight, height)}
    elif intent == "ลบงาน":
        deletehomework = data["deletehomework"]
        if deletehomework in todo_list:
            todo_list.remove(deletehomework)
            return {"reply": f"ลบงาน {deletehomework} แล้วครับ"}
        else:
            return {"reply": "ไม่พบงานนี้ครับ"}
    elif intent == "บันทึกข้อมูล":
        name = data["name"]
        age = data["age"]
        height = data["height"]
        return {"reply": jarvis_memorise(name,age,height)}
    elif intent == "เพิ่มผู้ติดต่อ":
        name = data["name"]
        phone = data["phone"]
        return {"reply": jarvisadd_contact(name,phone)}
    elif intent == "แก้ไขผู้ติดต่อ":
        traget_name = data["traget_name"]
        new_name = data["new_name"]
        new_phone = data["new_phone"]
        return {"reply": jarvisupdate_contact(traget_name,new_name,new_phone)}
    elif intent == "ค้นหาผู้ติดต่อ":
        name = data["name"]
        return {"reply": jarvissearch_contact(name)}
    elif intent == "ทายอายุ":
        name = data["name"]
        return {"reply": jarvis_guess_age(name)}
    else:
        return {"reply": "ไม่เข้าใจคำสั่งนี้ครับ"}

def clear_todo_list():
    todo_list.clear()
    return "ลบงานทั้งหมดแล้วครับ"

def jarvis_recall():
    result = ""
    for key,value in owner.items():
        result += f"{key}: {value}\n"
    return f"นี้คือข้อมูลทั้งหมดครับ\n{result}"

def jarvisshow_contact():
    result = ""
    for contact in contacts:
       result += f"ชื่อ {contact['name']} - เบอร์ {contact['phone']}\n"
    return f"นี้คือข้อมูลทั้งหมดครับ\n{result}"

def save_data():
    data = {
        "owner":owner,
        "contacts":contacts,
        "todo_list":todo_list
    }
    with open("data.json","w") as f:
        json.dump(data, f)
    return "บันทึกแล้วครับ"

def load_data():
    try:
        global owner , contacts , todo_list
        with open("data.json", "r") as f:
            data = json.load(f)
        owner = data["owner"]
        contacts = data["contacts"]
        todo_list = data["todo_list"]
        return "โหลดแล้วครับ"
    except FileNotFoundError:
        return "ยังไม่มีไฟล์ให้โหลด ต้องเซฟก่อนนะครับ"

def check_BMI(weight,height):
    BMI = weight/height**2
    if BMI < 18.5:
        return f"BMI ของคุณคือ {BMI:.2f} อยู่ในเกนณฑ์ ผอม ครับ"
    elif BMI < 23:
        return f"BMI ของคุณคือ {BMI:.2f} อยู่ในเกนณฑ์ ปกติสุขภาพดี ครับ"
    elif BMI < 25:
        return f"BMI ของคุณคือ {BMI:.2f} อยู่ในเกนณฑ์ น้ำหนักเกิน ครับ"
    else:
        return f"BMI ของคุณคือ {BMI:.2f} อยู่ในเกนณฑ์ อ้วน ครับ"

def jarvis_memorise(name,age,height):
        owner["name"] = name
        owner["age"] = int(age)
        owner["height"] = float(height)
        return f"บันทึกข้อมูลเรียบร้อยแล้วครับ คุณ {name} ยินดีต้อนรับครับ"

def jarvisadd_contact(name,phone):
    contacts.append({"name": name , "phone": phone})
    return f"เพิ่มผู้ติดต่อแล้วครับ คุณ {name} เบอร์ {phone}"

def jarvisupdate_contact(traget_name,new_name,new_phone):
    for s in contacts:
        if s["name"] == traget_name:
            s["name"] = new_name
            s["phone"] = new_phone
            return f"อัปเดตแก้ไขข้อมูลของ {traget_name} เป็น {new_name} และ {new_phone} แล้วครับ"
    return "ไม่พบรายชื่อนี้ครับ"

def jarvissearch_contact(name):
    result = ""
    for conteact in contacts:
        if conteact["name"] == name:
            result += f"{conteact['name']} - {conteact['phone']}\n"
            return f"นี้คือข้อมูลที่คุณค้นหาครับ\n{conteact['name']} - {conteact['phone']}"
    return "ไม่พบข้อมูลที่คุณค้นหาครับ"

def jarvis_guess_age(name):
    try:
        respones = requests.get(f"https://api.agify.io/?name={name}")
        data = respones.json()
        return f"ชื่อ {name} น่าจะอายุ {data['age']} ครับ"   
    except Exception as e:
        return "ขณะที่ทางระบบมีปัญหา กรุณาลองใหม่ภายหลังนะครับ"


if __name__ == "__main__":
    app.run(debug=True)