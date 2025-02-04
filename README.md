# Eye Blink Health Tracker 🚀👀

This Python project detects **eye blinks in real-time** using **OpenCV & MediaPipe** and provides **live feedback on blink health**. It alerts users with **beep sounds** and **voice summaries**, helping to prevent **eye strain & dryness**.

![Blink Detection](https://via.placeholder.com/800x400)  

---

## 🔹 Features

✅ **Real-Time Eye Blink Detection** using OpenCV & MediaPipe  
✅ **Eye Health Analysis:** Tracks blinks over a session  
✅ **Beep Sound Alert** if you forget to blink for **15 seconds**  
✅ **Voice Summary (TTS)** every **15 minutes**  
✅ **Live Session Timer** displays total elapsed time  
✅ **Optimized for Low-End Devices** (No heavy ML models required)  

---

## 🔹 Limitations

While this tool is effective for real-time blink detection and eye health tracking, it has some limitations:

**⚡ Windows-Only Compatibility:**

The beep sound alert (winsound.Beep) works only on Windows.
On Linux/macOS, alternative sound libraries like playsound or pydub may be needed.

**👤 Designed for One-Person Tracking:**

The tool is optimized for tracking a single person at a time.
If multiple faces are detected, only the first face will be processed.

**🎥 Camera & Lighting Conditions Affect Accuracy:**

Low-light conditions might reduce landmark detection accuracy, despite the contrast enhancement applied.
Works best with good lighting and a front-facing camera.

**🔁 Few False Negatives, But Not Perfect:**

The tool minimizes false negatives (missed blinks) by using an accurate EAR threshold.
However, false positives (accidental blinks) may occur if the person tilts their head or moves too fast.

**🖥️ System Performance Considerations:**

Optimized for low-end devices, but high-resolution cameras or heavy multitasking may impact real-time performance.
Frame rate may drop on older systems.

**📏 Requires Manual EAR Threshold Adjustment:**

Different people have different eye sizes and blink speeds.
The default EAR threshold (0.2) may need fine-tuning for different users.

---

## 🔹 Installation & Setup

### **📌 Installation & Setup Guide for README.md**  
Here’s a complete **Installation & Setup** section for your GitHub **README.md** file.

---

## **📥 Installation & Setup**  

### **1️⃣ Prerequisites**  
Before running the **Eye Blink Health Tracker**, ensure you have:

- ✅ **Windows OS** (Recommended)  
  - Works best on **Windows** (Beep sound won’t work on Linux/macOS)  
- ✅ **Python 3.7 or later**  
  - Check if Python is installed:

    ```sh
    python --version
    ```

- ✅ **A Webcam** (Built-in or External)  
  - The tool **requires a webcam** to detect eye blinks.  

---

### **2️⃣ Clone or Download the Project**  

#### **(a) Clone using Git**  
If you have Git installed, run:

```sh
git clone https://github.com/SudheerNaraharisetty/eye-blink-health-tracker.git
cd eye-blink-health-tracker
```

#### **(b) Download Manually**  
1. Go to [GitHub Repository](https://github.com/SudheerNaraharisetty/eye-blink-health-tracker)  
2. Click **Code → Download ZIP**  
3. Extract the ZIP and open the project folder.

---

### **3️⃣ Install Dependencies**  
To install all required libraries, **run this command:**

```sh
pip install -r requirements.txt
```

📌 **If `requirements.txt` is missing, install manually:**
```sh
pip install opencv-python mediapipe pyttsx3
```

---

### **4️⃣ Run the Eye Blink Tracker**  
Once installed, run the script:

```sh
python blink_detectionp.py
```

---

### **5️⃣ Expected Output**  
- **Detects eye blinks in real-time using your webcam** 🎥  
- **Alerts if you don’t blink for 15 seconds (beep sound)** 🔔  
- **Tracks session duration & blinks per minute** ⏱  
- **Gives voice summary every 15 minutes** 🔊  

---

## **🎯 You're All Set!**  
Your **Eye Blink Health Tracker** is now ready to use! 🚀  

Let me know if you need any changes before adding this to your **README.md**. 😊
