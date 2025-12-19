import pyttsx3

def speak_alert(is_rain):
    engine = pyttsx3.init()
    if is_rain:
        engine.say("Alert! Rain is expected. Please carry an umbrella.")
    else:
        engine.say("No rain expected. Have a great day!")
    engine.runAndWait()
