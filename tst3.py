import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def round_corners(image_path):
    original_image = Image.open(image_path)
    rounded_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
    mask = Image.new("L", original_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, original_image.width, original_image.height], 20, fill=255)
    rounded_image.paste(original_image, (0, 0), mask)
    return rounded_image

def main():
    root = tk.Tk()
    root.title("Image with Rounded Corners")
    root.configure(bg="black")
    # Ruta de la imagen
    image_path = r"GroundStation\team logo.jpg"  # Reemplaza con la ruta de tu imagen

    # Crear imagen con esquinas redondeadas
    rounded_image = round_corners(image_path)

    # Convertir la imagen redondeada a PhotoImage
    rounded_image_tk = ImageTk.PhotoImage(rounded_image)

    # Crear label y mostrar la imagen
    label = tk.Label(root, image=rounded_image_tk)
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
