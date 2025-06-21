# Driver-Alert

This project is a real-time Driver Alert System built using Python and OpenCV, designed to monitor driver fatigue by tracking Eye Aspect Ratio (EAR). If the system detects signs of drowsiness for a sustained period, it triggers an alert both visually and through a terminal-based buzzer simulation.

🧠 Overview
Driver fatigue is a leading cause of road accidents. This system simulates a non-intrusive safety feature that alerts the driver when signs of drowsiness are detected by monitoring eye movements using a webcam.

🛠️ Technologies Used
Python 3.x

OpenCV

NumPy

Threading & Time

Winsound (for buzzer simulation on Windows)

⚙️ How It Works
Eye Aspect Ratio (EAR) is calculated by detecting contours of both eyes.

If EAR falls below a specified threshold for a number of consecutive frames, the system assumes the driver is drowsy.

The frame is overlaid with a "SLEEP ALERT!" warning.

Terminal logs and simulated beeping (printed as 🔔) are activated to grab attention.

📸 Features
🔁 Real-time video processing from webcam

📐 Eye Aspect Ratio-based drowsiness detection

🔔 Terminal-based beep alert (can be modified for actual audio)

🎯 Contour detection and eye hull visualization

✅ State-aware logging to avoid repeated prints
