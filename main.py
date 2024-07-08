import os
import gradio as gr
from pathlib import Path
from PIL import Image


def scan_folder(folder_path):
    if folder_path == "":
        gr.Warning("Empty path")
        return

    path = Path(folder_path)

    if not os.path.exists(path):
        gr.Warning(f"Path {path} doesn`t exist")
        return [], 0

    images = sorted(list(path.glob('*.png')))

    return images, f" / {len(images)}"


def update_image(idx: int, all_images: list):
    if len(all_images) == 0:
        return
    idx = int(idx)
    image = Image.open(all_images[idx-1])

    return image


with gr.Blocks() as demo:
    all_images = gr.State([])

    with gr.Row():
        image_folder = gr.Textbox(max_lines=1, placeholder="Put absolute path to images folder", label="Images Root")
        scan_button = gr.Button(value="Load images")

    with gr.Row():
        idx = gr.Number(value=1)
        max_count = gr.HTML(value=f"/")

    with gr.Row():
        image = gr.Image(type="pil", height=512, show_download_button=False, scale=4)
        caption = gr.Textbox(label="Caption", scale=5)

    scan_button.click(scan_folder, inputs=image_folder, outputs=[all_images, max_count]).then(update_image, inputs=[idx, all_images], outputs=image)
    idx.change(update_image, inputs=[idx, all_images], outputs=image)


if __name__ == "__main__":
    demo.launch()
