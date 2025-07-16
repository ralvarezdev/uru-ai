import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar import pyzbar

# Define your validation function
def is_valid_qr(data):
    # Check if the QR code data is a valid URL
    return data.startswith("https")

# Scan QR from webcam
def scan_qr():
    cap = cv2.VideoCapture(0)
    valid_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objs = pyzbar.decode(frame)
        for obj in decoded_objs:
            qr_data = obj.data.decode("utf-8")
            valid_data = qr_data
            cap.release()
            cv2.destroyAllWindows()
            show_result(qr_data)
            return

        cv2.imshow("Scan QR Code - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Display result in GUI
def show_result(qr_data):
    if is_valid_qr(qr_data):
        messagebox.showinfo("QR Code Result", f"✅ Valid QR Code:\n{qr_data}")
    else:
        messagebox.showerror("QR Code Result", f"❌ Invalid QR Code:\n{qr_data}")

# Tkinter GUI setup
root = tk.Tk()
root.title("QR Code Scanner")

canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

scan_button = tk.Button(root, text="Scan QR Code", command=scan_qr)
canvas.create_window(150, 100, window=scan_button)

root.mainloop()