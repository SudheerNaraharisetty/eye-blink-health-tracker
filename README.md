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

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/SudheerNaraharisetty/eye-blink-health-tracker.git
cd eye-blink-health-tracker
