import os
import gradio as gr
from pathlib import Path
from PIL import Image
import clipboard
from config import samples, default_path


def scan_folder(folder_path):
    if folder_path == "":
        gr.Warning("Empty path")
        return

    path = Path(folder_path)

    if not os.path.exists(path):
        gr.Warning(f"Path {path} doesn`t exist")
        return [], 0

    images = sorted(list(path.glob('*.png')))
    txt_paths = [Path(str(path).replace(".png", ".txt")) for path in images]

    result = [(image, txt_path) for image, txt_path in zip(images, txt_paths)]

    return result


def update_image(idx: int, all_images: list):
    if len(all_images) == 0:
        return
    
    image_path, caption_path = all_images[idx - 1]

    image = Image.open(image_path)

    if os.path.exists(caption_path):
        with open(caption_path, "r") as fin:
            caption = fin.read().strip()
    else:
        caption = ""

    return image, caption


def save_caption(caption, idx, all_images):
    _, caption_path = all_images[idx - 1]

    with open(caption_path, "w") as fout:
        print(caption, file=fout)

    gr.Info("Caption is saved")

def helper_select(value, event: gr.EventData):
    clipboard.copy(value[0])


with gr.Blocks() as demo:
    all_images = gr.State([])

    with gr.Row():
        image_folder = gr.Textbox(max_lines=1, placeholder="Put absolute path to images folder", label="Images Root", value=default_path)
        scan_button = gr.Button(value="Load images")

    with gr.Row():
        with gr.Column():
            idx = gr.Number(label="Image Number", value=1, precision=0, minimum=1)
        with gr.Column():
            with gr.Group():
                next_button = gr.Button(icon="arrow_up.svg", value="Next")
                prev_button = gr.Button(icon="arrow_down.svg", value="Prev")

    with gr.Row():
        image = gr.Image(type="pil", height=512, show_download_button=False, scale=4)
        with gr.Column(scale=5):
            template = gr.Textbox(interactive=False, container=False, value="{Subject}, {Hair}, {Action}, {Clothes}, {Emotions}, {Showing}, {indoors/outdoors}, {place}, {shot type}")
            caption = gr.Textbox(label="Caption", interactive=True)
            helpers = gr.Dataset(label="Helpers", components=[caption], samples=samples, samples_per_page=100)
                
            save_caption_button = gr.Button("Save caption")

    scan_button.click(scan_folder, inputs=image_folder, outputs=all_images).then(update_image, inputs=[idx, all_images], outputs=[image, caption])
    idx.change(update_image, inputs=[idx, all_images], outputs=[image, caption])
    idx.submit(update_image, inputs=[idx, all_images], outputs=[image, caption])
    next_button.click(lambda x: x+1, inputs=idx, outputs=idx)
    prev_button.click(lambda x: x-1 if x > 1 else x, inputs=idx, outputs=idx)
    helpers.select(helper_select, inputs=helpers)
    save_caption_button.click(save_caption, inputs=[caption, idx, all_images])


if __name__ == "__main__":
    demo.queue(max_size=1)
    demo.launch()
