import customtkinter as ctk
import threading
import time
import pyautogui
import ctypes

# Configuración inicial de la GUI
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class DrinkingBirdApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Anti-Away para Teams")
        self.iconbitmap("img/drinking_bird_icon.ico")
        self.geometry("300x160")
        self.resizable(False, False)

        self.running = False
        self.thread = None

        self.label = ctk.CTkLabel(self, text="Estado: Inactivo", text_color="red", font=ctk.CTkFont(size=16))
        self.label.pack(pady=20)

        self.toggle_btn = ctk.CTkButton(self, text="Iniciar", command=self.toggle)
        self.toggle_btn.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle(self):
        if not self.running:
            self.running = True
            self.label.configure(text="Estado: Activo", text_color="green")
            self.toggle_btn.configure(text="Detener")
            self.thread = threading.Thread(target=self.keep_awake, daemon=True)
            self.thread.start()
        else:
            self.running = False
            self.label.configure(text="Estado: Inactivo", text_color="red")
            self.toggle_btn.configure(text="Iniciar")

    def keep_awake(self):
        while self.running:
            # Mueve el ratón 1px y vuelve
            pyautogui.moveRel(1, 0)
            time.sleep(0.2)
            pyautogui.moveRel(-1, 0)

            # Simula pulsar Shift
            ctypes.windll.user32.keybd_event(0xA0, 0, 0, 0)  # Shift izquierdo (presionar)
            time.sleep(0.05)
            ctypes.windll.user32.keybd_event(0xA0, 0, 2, 0)  # soltar

            for _ in range(30):  # Espera 30 segundos en intervalos de 1s para permitir detener
                if not self.running:
                    break
                time.sleep(1)

    def on_close(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = DrinkingBirdApp()
    app.mainloop()
