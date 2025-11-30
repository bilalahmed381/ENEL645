import gradio as gr

from main.detector import pothole_detector

# define gradio interface
input_file = gr.File(
    label="upload image or video"
)  # file input to upload image or video
input_preview = gr.Image(
    label="input preview", interactive=False
)  # image preview of the uploaded input
output_preview_image = gr.Image(
    label="detected image output", interactive=False, visible=False
)  # image output preview
output_preview_video = gr.Video(
    label="detected video output", interactive=False, visible=False
)  # video output preview
output_download = gr.File(
    label="download output", interactive=True
)  # file output for downloading the result

with gr.Blocks() as iface:
    gr.Markdown(
        "## 🛣️ pothole detection & severity estimation with yolov12"
    )  # markdown header for the app

    with gr.Row():
        with gr.Column():
            # render file upload input
            input_file.render()
            # render image preview of the input
            input_preview.render()
        with gr.Column():
            # render image output preview
            output_preview_image.render()
            # render video output preview
            output_preview_video.render()
            # render output download link
            output_download.render()

    # define function to process and display input and output
    def process_and_display(input_media):
        if input_media is None:
            # handle case when no file is uploaded or cleared
            return None, gr.update(visible=False), gr.update(visible=False), None

        input_path, output_path = pothole_detector(
            input_media
        )  # call pothole_detector to get paths

        # check if the output is a video or image and display accordingly
        if output_path.endswith((".mp4", ".avi", ".mov")):
            # if output is a video
            return (
                input_path,
                gr.update(value=None, visible=False),  # hide image
                gr.update(value=output_path, visible=True),  # show video
                output_path,
            )
        else:
            # if output is an image
            return (
                input_path,
                gr.update(value=output_path, visible=True),  # show image
                gr.update(value=None, visible=False),  # hide video
                output_path,
            )

    # define the action when the input file is changed
    input_file.change(
        fn=process_and_display,  # function to call when input file changes
        inputs=input_file,  # the input component
        outputs=[
            input_preview,  # input preview image
            output_preview_image,  # output image update
            output_preview_video,  # output video update
            output_download,  # downloadable output path
        ],
    )


if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0")  # launch the gradio interface
