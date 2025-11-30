def get_severity_with_position(area, y_center, frame_height, alpha=0.6):
    # normalize vertical position (1 means bottom of frame, 0 means top)
    vertical_position_norm = y_center / frame_height

    # normalize area (you can tune this denominator based on typical bbox sizes)
    normalized_area = area / (frame_height * frame_height)

    # weighted severity score
    score = alpha * normalized_area + (1 - alpha) * vertical_position_norm

    if score < 0.2:
        return "Low"
    elif score < 0.4:
        return "Medium"
    else:
        return "High"
    
def is_video_file(path):
    # check if the file path is a valid video file
    return isinstance(path, str) and path.endswith(
        (".mp4", ".avi", ".mov")
    )  # check if the file has video extensions    