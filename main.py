from tkinter import Tk
from menu import MainMenu

def main():
    root = Tk()
    menu = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
