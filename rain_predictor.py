import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from model import train_model, predict_rain
from voice_alert import speak_alert

# Train model
try:
    train_model()
except Exception as e:
    print(f"Model training failed: {e}")

# App setup
app = tk.Tk()
app.title("🌦 RainPredictor: Smart Rain Alert")
app.geometry("700x600")
app.resizable(False, False)

# Load background image from URL
try:
    url = "https://img.freepik.com/free-vector/realistic-background-monsoon-season_23-2150428848.jpg?t=st=1746873198~exp=1746876798~hmac=5bb017208bfc9454669a9977036146483118328b4025bed0d8bdff30bd671ddd&w=1380"
    response = requests.get(url)
    bg_image = Image.open(BytesIO(response.content))
    bg_image = bg_image.resize((700, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Failed to load background from URL: {e}")

# Semi-transparent panel
panel = tk.Frame(app, bg="#ffffff", bd=2, relief="ridge")
panel.place(x=50, y=100, width=600, height=350)

# Real-time clock
def update_clock():
    current_time = time.strftime("%I:%M:%S %p")
    clock_label.config(text="🕒 " + current_time)
    app.after(1000, update_clock)

clock_label = tk.Label(app, font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#000000", bd=2, relief="solid")
clock_label.place(x=520, y=20)
update_clock()

# Animated quote
quote_text = "❝ Let the rain wash away the worries of yesterday ❞"
quote_label = tk.Label(app, text=quote_text, font=("Comic Sans MS", 16, "bold italic"), 
                       fg="#004d99", bg="#ffffff")
quote_label.place(x=100, y=60)  # Adjusted the position to move it below the clock

# Animate quote glow
quote_colors = ["#004d99", "#007acc", "#3399ff"]
def glow_effect(index=0):
    quote_label.config(fg=quote_colors[index])
    app.after(700, glow_effect, (index + 1) % len(quote_colors))
glow_effect()

# Input creation
def create_input(label_text, y):
    label = tk.Label(panel, text=label_text, font=("Arial", 13, "bold"), bg="#ffffff", fg="#333")
    label.place(x=30, y=y)
    entry = tk.Entry(panel, font=("Arial", 13), width=20, bd=2, relief="groove")
    entry.place(x=250, y=y)
    return entry

temp_entry = create_input("🌡 Temperature (°C):", 30)
hum_entry = create_input("💧 Humidity (%):", 90)
pres_entry = create_input("🌬 Pressure (hPa):", 150)

# Show graph
def show_chart():
    import pandas as pd
    data = pd.read_csv("weather.csv")
    plt.figure(figsize=(6, 4))
    plt.plot(data["temperature"], data["humidity"], marker='o', color='blue', label='Humidity vs Temp')
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.title("Humidity vs Temperature")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Prediction logic
def check_rain():
    try:
        temp = float(temp_entry.get())
        hum = float(hum_entry.get())
        pres = float(pres_entry.get())

        result = predict_rain(temp, hum, pres)
        speak_alert(result)

        if result == 1:
            messagebox.showinfo("Rain Alert ☔", "🌧 Rain is expected. Carry an umbrella!")
        else:
            messagebox.showinfo("Rain Alert ☀", "No rain expected. Have a great day!")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Button styles
predict_btn = tk.Button(panel, text="🔍 Predict Rain", font=("Arial", 14, "bold"),
                        bg="#28a745", fg="white", padx=20, pady=8, bd=0,
                        activebackground="#218838", command=check_rain)
predict_btn.place(x=190, y=220)

chart_btn = tk.Button(panel, text="📊 Show Weather Chart", font=("Arial", 12, "bold"),
                      bg="#007acc", fg="white", padx=12, pady=6, bd=0,
                      activebackground="#005580", command=show_chart)
chart_btn.place(x=200, y=280)

# Footer
footer = tk.Label(app, text="Made by Mehak | BTech CSE Project", font=("Arial", 10, "italic"),
                  bg="#ffffff", fg="#555")
footer.pack(side="bottom", pady=10)

app.mainloop() 