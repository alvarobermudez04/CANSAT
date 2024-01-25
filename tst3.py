from customtkinter import CTk, CTkLabel
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    root = CTk()
    root.title("Image with Rounded Corners")
    root.configure(bg="black")

    # Crear label
    label = CTkLabel(root)
    label.pack()

    # Crear un DataFrame de ejemplo para Seaborn
    import pandas as pd
    data = {'x': [1, 2, 3, 4, 5], 'y': [10, 5, 8, 2, 7]}
    df = pd.DataFrame(data)

    # Crear un gráfico Seaborn
    sns.set(style="whitegrid")
    sns.lineplot(x='x', y='y', data=df)

    # Crear un lienzo para el gráfico en el GUI
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.get_tk_widget().pack()

    # Añadir la línea para manejar el evento de cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()
