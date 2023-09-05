import cv2
import os
import random
import string

frame_dir = "frames"
replacement_dir = "replacements"
frames = [os.path.join(frame_dir, f) for f in os.listdir(frame_dir)]
replacements = [os.path.join(replacement_dir, f) for f in os.listdir(replacement_dir)]
random.shuffle(frames)
random.shuffle(replacements)
top_left = None
bottom_right = None
replacement_image = None
mockup_image = None


def choose_images():
    global mockup_image, replacement_image
    frame = frames.pop()
    replacement = replacements.pop()
    mockup_image = cv2.imread(frame)
    mockup_image = cv2.resize(mockup_image, (1280, 960))
    replacement_image = cv2.imread(replacement)


def mouse_callback(event, x, y, flags, param):
    global top_left, bottom_right
    if event == cv2.EVENT_LBUTTONDOWN:
        top_left = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        bottom_right = (x, y)

        cv2.rectangle(mockup_image, top_left, bottom_right, (0, 0, 0, 0), -1)
        replace_roi()
        cv2.destroyAllWindows()


def replace_roi():
    global mockup_image, top_left, bottom_right, replacement_image
    roi = mockup_image[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]

    replacement_image_resized = cv2.resize(
        replacement_image, (roi.shape[1], roi.shape[0]), interpolation=cv2.INTER_CUBIC
    )
    mockup_image[
        top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]
    ] = replacement_image_resized


def save_image():
    letters = string.ascii_lowercase
    filename = "".join(random.choice(letters) for i in range(10)) + ".jpg"
    cv2.imwrite(filename, mockup_image)
    print("Image saved as", filename)


def run_script():
    global frames, replacements
    while True:
        if not frames or not replacements:
            print("No more images to process")
            return
        choose_images()
        cv2.namedWindow("Mockup")
        cv2.setMouseCallback("Mockup", mouse_callback)
        while True:
            cv2.imshow("Mockup", mockup_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                return
            elif key == ord("s"):
                save_image()
                break
            elif key == ord("r"):
                frames.append(frames.pop(0))
                replacements.append(replacements.pop(0))
                break
        cv2.destroyAllWindows()


run_script()
