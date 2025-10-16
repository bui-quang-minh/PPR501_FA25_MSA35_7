#API Crawler
import tkinter

API_URL = 'http://127.0.0.1:8000'

from views.main_view import MainView

def main():
    root = tkinter.Tk()
    app = MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()