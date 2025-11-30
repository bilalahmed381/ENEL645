import cv2

from main.model import load_model
from main.utilities import get_severity_with_position, is_video_file

# load the pre-trained model
model = load_model()


def draw_boxes_and_severity(frame, boxes):
    # iterate over the detected boxes and draw them with severity labels
    for x1, y1, x2, y2 in boxes:
        area = (x2 - x1) * (y2 - y1)
        y_center = (y1 + y2) / 2
        frame_height = frame.shape[0]
        severity = get_severity_with_position(area, y_center, frame_height)
        # draw a rectangle around the detected pothole
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        # add severity text near the top-left corner of the box
        cv2.putText(
            frame,
            severity,
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )

    return frame  # return the frame with the drawn boxes and severity labels


def pothole_detector(input_media):
    if input_media is None:  # check if input media is provided
        return None, None  # return None if no input media is passed

    if is_video_file(input_media):  # check if the input is a video file
        cap = cv2.VideoCapture(input_media)  # open the video file
        if not cap.isOpened():  # check if the video was successfully opened
            raise ValueError(
                f"Error opening video file: {input_media}"
            )  # raise an error if video is not opened

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # get width of the video
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # get height of the video
        fps = cap.get(cv2.CAP_PROP_FPS)  # get frames per second of the video

        output_video_path = (
            "output_detected.mp4"  # set the output path for the detected video
        )
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # set codec for video output
        out = cv2.VideoWriter(
            output_video_path, fourcc, fps, (width, height)
        )  # initialize VideoWriter

        frame_idx = 0  # initialize frame index for processing
        while cap.isOpened():  # loop through video frames
            ret, frame = cap.read()  # read a new frame
            if (
                not ret or frame is None or frame_idx > fps * 10
            ):  # break after 10 seconds or if no frame is read
                break

            # make predictions on the frame and draw bounding boxes
            results = model.predict(frame, conf=0.4, classes=[0], verbose=False)
            boxes = (
                results[0].boxes.xyxy.cpu().numpy()
                if results and results[0].boxes
                else []
            )  # extract bounding boxes
            frame = draw_boxes_and_severity(
                frame, boxes
            )  # draw the bounding boxes and severity on the frame

            out.write(frame)  # write the processed frame to the output video
            frame_idx += 1  # increment frame index

        cap.release()  # release video capture
        out.release()  # release video writer

        return input_media, output_video_path  # return input and output video paths

    else:  # if the input is an image
        img = cv2.imread(input_media)  # read the image
        if img is None:  # check if image was read successfully
            return None, None  # return None if image is invalid

        # make predictions on the image and draw bounding boxes
        results = model.predict(img, conf=0.4, classes=[0], verbose=False)
        boxes = (
            results[0].boxes.xyxy.cpu().numpy() if results and results[0].boxes else []
        )  # extract bounding boxes
        img = draw_boxes_and_severity(
            img, boxes
        )  # draw the bounding boxes and severity on the image

        output_image_path = (
            "output_detected.jpg"  # set the output path for the detected image
        )
        cv2.imwrite(output_image_path, img)  # save the processed image

        return input_media, output_image_path  # return input and output image paths
