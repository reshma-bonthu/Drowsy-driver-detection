import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import cv2
import dlib
from imutils import face_utils
import numpy as np
import winsound

# Initialize the camera and Dlib detectors
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Global variables for drowsiness detection
sleep = 0
drowsy = 0
active = 0
yawn = 0
status = ""
color = (0, 0, 0)
sound_thread_running = False

def play_alert_sound():
    global sound_thread_running
    if not sound_thread_running:
        sound_thread_running = True
        try:
            winsound.Beep(1000, 2000)
        finally:
            sound_thread_running = False

# Distance computation function
def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

# Blink detection function
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    if ratio > 0.25:
        return 2  # Open
    elif ratio > 0.21 and ratio <= 0.25:
        return 1  # Partial Blink
    else:
        return 0  # Sleeping

# Yawn detection function
def is_yawning(landmarks):
    top_lip = landmarks[51]
    bottom_lip = landmarks[57]
    left_corner = landmarks[48]
    right_corner = landmarks[54]
    vertical_dist = compute(top_lip, bottom_lip)
    horizontal_dist = compute(left_corner, right_corner)
    yawn_ratio = vertical_dist / horizontal_dist
    return yawn_ratio > 0.52

def run_detection():
    global sleep, drowsy, active, yawn, status, color
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        face_frame = frame.copy()
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if is_yawning(landmarks):
                yawn += 1
                if yawn > 5:
                    status = "Yawning !!!"
                    color = (255, 165, 0)
                    cv2.putText(frame, status, (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            else:
                yawn = 0

            if left_blink == 0 or right_blink == 0:
                sleep += 1
                drowsy = 0
                active = 0
                if sleep > 20:
                    status = "SLEEPING !!!"
                    color = (0, 0, 255)
                    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                    threading.Thread(target=play_alert_sound).start()
            elif left_blink == 1 or right_blink == 1:
                sleep = 0
                active = 0
                drowsy += 1
                if drowsy > 6:
                    status = "Drowsy !"
                    color = (255, 0, 0)
                    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            else:
                drowsy = 0
                sleep = 0
                active += 1
                if active > 6:
                    status = "Active :)"
                    color = (0, 255, 0)
                    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
                
        # Show the frames side by side
        combined_frame = np.hstack((frame, face_frame))
        cv2.imshow("Drowsiness Detection", combined_frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Frontend using tkinter
def create_frontend():
    root = tk.Tk()
    root.title("Drowsy Driver Detection")

    # Set fullscreen
    root.geometry("1950x1080")

    # Load and resize background image
    bg_image = Image.open(r"bg2.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Create a label for background
    bg_label = Label(root, image=bg_image_tk)
    bg_label.place(relwidth=1, relheight=1)

    # Title styling
    title_label = Label(root, text="Safety on Wheels", font=("Arial", 30, "bold"),bg="#000000", fg="white")
    title_label.place(relx=0.5, rely=0.1, anchor="center")
    def animate_title_opacity(label, opacity=0):
        opacity += 5
        if opacity <= 255:
            # Adjust the color based on opacity
            color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            label.config(fg=color)
            root.after(50, lambda: animate_title_opacity(label, opacity))

    animate_title_opacity(title_label)
    # Custom rounded button
    def on_enter(event):
        generate_button.config(bg="#005f73")

    def on_leave(event):
        generate_button.config(bg="#008CBA")
    # Generate button
    generate_button = Button(root, text="Start Detection", font=("Arial", 20, "bold"), bg="#008CBA", fg="white", padx=20, pady=10, command=lambda: threading.Thread(target=run_detection).start())
    generate_button.place(relx=0.5, rely=0.5, anchor="center")
    # Bind hover effects
    generate_button.bind("<Enter>", on_enter)
    generate_button.bind("<Leave>", on_leave)

    root.mainloop()

create_frontend()
