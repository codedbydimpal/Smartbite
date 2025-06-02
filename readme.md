# 🧠 Smartbite: AI-powered Fruit Detection & Nutritional Estimation

Smartbite is an AI-based application built using YOLO (You Only Look Once) that identifies fruits from an uploaded image and provides an accurate nutritional breakdown per fruit based on a selected serving size. It also offers the option to download the analysis as a professional PDF report.

---

## 🚀 Features

- 🍎 **Automatic Fruit Detection** using a YOLOv8 model.
- 📊 **Nutritional Analysis** based on the detected fruit and user-selected serving size.
- 🧾 **PDF Report Generation** with detected images and a nutrient table.
- 🖼️ Streamlit-based GUI for easy interaction and usability.
- 📥 Downloadable, professional-style reports for diet tracking or educational use.

---

## 🔍 Why This Project Is Useful

### 🎯 Health & Wellness Tracking
Helps users better understand the nutritional value of fruits they consume regularly, promoting healthier dietary habits.

### 👨‍🏫 Educational Tool
Can be used in classrooms and training environments to teach about computer vision, healthy eating, or both.

### 🍽️ Diet Planning
Assists fitness coaches and nutritionists in creating accurate, fruit-based meal plans.

### 📷 Computer Vision Application
Demonstrates the use of real-time object detection and classification in a practical, user-centric application.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Model:** YOLOv8
- **Backend:** Python, PIL, FPDF
- **Visualization:** Matplotlib, Pandas

---

## 🧪 Model Training Results

The YOLOv8 model was trained to detect multiple fruit categories. Below are the performance metrics over 50 epochs:

### 📉 Training & Validation Loss
| Metric        | Trend (↓)        |
|---------------|------------------|
| `train/box_loss` | Decreasing steadily |
| `val/box_loss`   | Decreasing with some noise |
| `train/cls_loss` | Sharp decline in early epochs |
| `val/cls_loss`   | Follows training trend |
| `train/dfl_loss` | Gradual decline |
| `val/dfl_loss`   | Slightly noisier decline |

### 📈 Precision, Recall, and mAP
| Metric            | Value (Final Epoch) |
|-------------------|---------------------|
| `precision(B)`     | ~0.96               |
| `recall(B)`        | ~0.97               |
| `mAP@0.5`          | ~0.95               |
| `mAP@0.5:0.95`     | ~0.85               |

![Training Results](Project-Images/Results.png)

These metrics indicate the model is both highly accurate and robust in detecting fruit categories.

---

## 🖥️ GUI Snapshot

The interface allows easy image upload, serving size selection, and download of results:

![Smartbite GUI](Project-Images/Smartbite%20GUI.png)

---

## 🤔 Results with Identified Fruit image and Nutrient summary

![Nutrition Results](Project-Images/Nutrition%20Results.png)


## 📄 PDF Report Example

A sample output report includes:
- The uploaded image.
- The detection result with bounding boxes.
- A nutrient breakdown per fruit based on serving size.

![Report Sample](Project-Images/Report%20in%20PDF%20form.png)

---

## ▶️ How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Launch the app:
    ```bash
    streamlit run app.py
    ```

3. Upload a fruit image and receive nutritional insights instantly!

---

## 🧠 Future Enhancements

- 🔄 Real-time webcam-based detection
- 📦 Upload support for multiple images
- 🥗 Integration with broader meal tracking systems

---
