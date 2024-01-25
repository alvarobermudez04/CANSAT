from customtkinter import *  # pip install customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def on_closing():
    root.destroy()
    plt.close()


def main():
    global root
    root = CTk()
    root.title("Image with Rounded Corners")
    root.configure(bg="black")

    # Create label
    label = CTkLabel(root, text="Hello, CustomTkinter!", font=("Helvetica", 16))
    label.pack()

    # Create Matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    ax.set_title('Matplotlib Plot')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Embed Matplotlib plot into Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Close Matplotlib plot properly on window close
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()

