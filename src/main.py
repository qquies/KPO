from core.home_controller import HomeController
from ui.smart_home_gui import SmartHomeGUI
import tkinter as tk

def main():
    controller = HomeController()
    controller.start_system()

    root = tk.Tk()
    gui = SmartHomeGUI(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()