# audio = 'https://s3-ap-southeast-1.amazonaws.com/rekognition-hirepro-test/proctored_data/159/3842990/3895480/media/63db05b9-9595-4b55-9bb4-87bff65bf3a9_TestUser_3764884_198832.opus?AWSAccessKeyId=AKIAIPKT65FIXSXQGDOQ&Signature=kTXKP8EEiFHoVn%2Fy3nQx9%2FUPoRg%3D&Expires=1733483800'

# video = 'https://s3-ap-southeast-1.amazonaws.com/rekognition-hirepro-test/proctored_data/159/3842990/3895480/media/63db05b9-9595-4b55-9bb4-87bff65bf3a9_TestUser_3764884_198832.webm?AWSAccessKeyId=AKIAIPKT65FIXSXQGDOQ&Signature=WSyCmFGqcB0qSxLCWMkfABRhzQg%3D&Expires=1733483800'

import cv2

# file_path = r'C:\Users\Dell\Desktop\automation - proc\63db05b9-9595-4b55-9bb4-87bff65bf3a9_TestUser_3764884_198832.webm'


# def check_video(file_path):
#     # Try to open the video file using OpenCV
#     cap = cv2.VideoCapture(file_path)
#
#     if cap.isOpened():
#         frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         fps = cap.get(cv2.CAP_PROP_FPS)
#
#         if frame_count > 0 and fps > 0:
#             print(f"Video is valid. Frame count: {frame_count}, FPS: {fps}")
#             return True
#         else:
#             print("Video is invalid (no frames).")
#             return False
#     else:
#         print("Failed to open video file.")
#         return False
#
# import cv2
# import numpy as np
#
# # Video properties
# width, height = 1920, 1080
# fps = 30
# duration = 60  # in seconds
#
# # Create a black frame
# black_frame = np.zeros((height, width, 3), dtype=np.uint8)
#
# # Define video writer object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('black_screen.avi', fourcc, fps, (width, height))
#
# # Write black frames to video
# for _ in range(fps * duration):
#     out.write(black_frame)
#
# # Release video writer
# out.release()
# cv2.destroyAllWindows()

# Example usage
video_file_path = r"C:\Users\Dell\Desktop\automation - proc\black_screen.avi"  # Change to your video file path
# check_video(video_file_path)
#
# import cv2
# import pyvirtualcam
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
#
# # Path to your video file
# video_path = r"C:\Users\Dell\Desktop\automation - proc\black_screen.avi"
#
# # Open video using OpenCV
# cap = cv2.VideoCapture(video_path)
#
# # Set up Chrome WebDriver (or another browser driver)
# chrome_options = Options()
# chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow media stream in browser
# driver = webdriver.Chrome(executable_path='F:\ASSESSMENT\chromedriver.exe', options=chrome_options)
#
# # Navigate to the page where webcam input is needed
# driver.get('https://webcamtests.com/')
#
# # Wait for the page to load and the webcam prompt to appear
# time.sleep(5)  # Adjust as necessary
#
# # Start the virtual webcam using pyvirtualcam
# with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Convert the frame to the correct color format for pyvirtualcam
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # Feed the frame to the virtual webcam
#         cam.send(frame)
#         cam.sleep_until_next_frame()
#
#         # You can add more logic here to control the video playback
#
#     # Close the video capture when done
#     cap.release()
#
# # Optionally, close the browser after a delay
# time.sleep(5)  # Adjust to let the video play in the browser
# driver.quit()


import time
import cv2
import numpy as np
import pyvirtualcam
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Define the path to your video file
video_path = r"C:\Users\Dell\Desktop\automation - proc\black_screen.avi"  # Change this to your recorded video file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties (e.g., width, height, fps)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Initialize the virtual camera
with pyvirtualcam.Camera(width=frame_width, height=frame_height, fps=fps) as cam:
    print(f"Virtual camera started: {cam.device}")

    # Open a browser session with Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='F:\ASSESSMENT\chromedriver.exe', options=options)

    # Navigate to a webpage that requires webcam input (like a video chat app)
    driver.get(
        "https://amsin.hirepro.in/assessment/#/assess/login/eyJ1aWQiOiAiUVZReE16Z3pPREUxTVRZM01EST0iLCAicHN3ZCI6ICJWQ002WVhSV1ZrTT0iLCAiYWxpYXMiOiAiQVQiLCAiYXV0b2xvZ2luIjogImRISjFaUT09In0=")  # Replace with your actual URL

    # Give the page some time to load
    time.sleep(60)  # Adjust based on your page load time

    # Example: Automate any interaction (e.g., clicking a button to start video chat)
    # Replace with the appropriate interaction for your use case
    # Here we assume there's a button with id 'start-video-call'
    # start_button = driver.find_element(By.ID, "start-video-call")
    # start_button.click()

    # Wait for video input setup
    time.sleep(5)

    # Feed video to the virtual webcam while the browser session is open
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        # Convert frame to RGB (pyvirtualcam requires RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Send the frame to the virtual camera
        cam.send(frame_rgb)

        # Optionally, display the frame (for debugging purposes)
        cv2.imshow('Virtual Camera Feed', frame)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

    # Close the browser session
    driver.quit()
