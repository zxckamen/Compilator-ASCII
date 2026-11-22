
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def pick_image():
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)

    path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[
            ("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
            ("Все файлы", "*.*"),
        ]
    )
    root.destroy()
    return path


def image_to_ascii(image_path, width=100, chars="@%#*+=-:. ", invert=False):
    img = Image.open(image_path)

    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg

    height = max(1, int(width * (img.height / img.width) * 0.55))
    img = img.convert("L").resize((width, height), Image.LANCZOS)

    if invert:
        chars = chars[::-1]

    n = len(chars) - 1
    pixels = list(img.getdata())
    lines = [
        "".join(chars[p * n // 255] for p in pixels[y * width:(y + 1) * width])
        for y in range(height)
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    path = pick_image()

    if not path:
        print("Файл не выбран.")
    else:
        art = image_to_ascii(path, width=100)
        print(art)

        out = os.path.splitext(path)[0] + "_ascii.txt"
        with open(out, "w", encoding="utf-8") as f:
            f.write(art)
        print(f"\nСохранено: {out}")