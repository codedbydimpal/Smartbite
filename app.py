import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
from PIL import Image
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from fpdf import FPDF
import tempfile
import io
import os
from datetime import datetime

# Load YOLO model
model = YOLO("best.pt")

# Nutritional info per 100g
nutrients = {
    "apple": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "sugar": 10, "fiber": 2.4, "vitamin_c": 4.6},
    "banana": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "sugar": 12, "fiber": 2.6, "vitamin_c": 8.7},
    "cucumber": {"calories": 16, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "sugar": 1.7, "fiber": 0.5, "vitamin_c": 2.8},
    "kiwi": {"calories": 41, "protein": 0.8, "fat": 0.4, "carbs": 10, "sugar": 9, "fiber": 2.1, "vitamin_c": 92.7},
    "orange": {"calories": 47, "protein": 0.9, "fat": 0.1, "carbs": 12, "sugar": 9, "fiber": 2.4, "vitamin_c": 53.2},
    "coconut": {"calories": 354, "protein": 3.3, "fat": 33.5, "carbs": 15.2, "sugar": 6.2, "fiber": 9, "vitamin_c": 3.3},
    "peach": {"calories": 39, "protein": 0.9, "fat": 0.3, "carbs": 10, "sugar": 8, "fiber": 1.5, "vitamin_c": 6.6},
    "cherry": {"calories": 50, "protein": 1.0, "fat": 0.3, "carbs": 12, "sugar": 8, "fiber": 1.6, "vitamin_c": 7},
    "pear": {"calories": 57, "protein": 0.4, "fat": 0.1, "carbs": 15, "sugar": 10, "fiber": 3.1, "vitamin_c": 4.3},
    "pomegranate": {"calories": 83, "protein": 1.7, "fat": 1.2, "carbs": 19, "sugar": 13, "fiber": 4, "vitamin_c": 10.2},
    "pineapple": {"calories": 50, "protein": 0.5, "fat": 0.1, "carbs": 13, "sugar": 10, "fiber": 1.4, "vitamin_c": 47.8},
    "watermelon": {"calories": 30, "protein": 0.6, "fat": 0.2, "carbs": 8, "sugar": 6, "fiber": 0.4, "vitamin_c": 8.1},
    "melon": {"calories": 34, "protein": 0.8, "fat": 0.2, "carbs": 9, "sugar": 8, "fiber": 0.9, "vitamin_c": 36.7},
    "grape": {"calories": 69, "protein": 0.6, "fat": 0.2, "carbs": 18, "sugar": 15, "fiber": 0.9, "vitamin_c": 3.2},
    "strawberry": {"calories": 32, "protein": 0.7, "fat": 0.3, "carbs": 8, "sugar": 4.9, "fiber": 2.0, "vitamin_c": 58.8}
}


# PDF class
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.temp_images = []

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Smartbite Report", ln=True, align="C")
        self.ln(5)

    def add_images_side_by_side(self, img1, img2, label1="Uploaded Image", label2="Detected Image with bounding boxes", pixel_width=240):
        # Resize both images
        aspect1 = img1.height / img1.width
        aspect2 = img2.height / img2.width

        height1 = int(pixel_width * aspect1)
        height2 = int(pixel_width * aspect2)

        resized1 = img1.resize((pixel_width, height1))
        resized2 = img2.resize((pixel_width, height2))

        # Save temp files
        temp1 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        resized1.save(temp1.name)
        resized2.save(temp2.name)
        self.temp_images.extend([temp1.name, temp2.name])
        temp1.close()
        temp2.close()

        # Draw images side by side
        current_y = self.get_y()
        self.image(temp1.name, x=20, y=current_y, w=60)
        self.image(temp2.name, x=110, y=current_y, w=60)

        # Add labels under images
        label_y = current_y + max(height1, height2) * 0.2645 + 2
        self.set_xy(20, label_y)
        self.set_font("Arial", "I", 10)
        self.cell(60, 8, label1, align="C")
        self.set_xy(110, label_y)
        self.cell(60, 8, label2, align="C")

        # Move cursor below labels with padding
        self.set_y(label_y + 12)

    def add_nutrient_table(self, all_data, serving_size):
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Nutritional Breakdown ({serving_size}g per fruit)", ln=True)
        self.ln(4)

        fruits = list(all_data.keys())
        nutrients = ["calories", "protein", "fat", "carbs", "sugar", "fiber", "vitamin_c"]
        col_width = 27
        row_height = 6

        # Header row: empty cell + fruits
        self.set_font("Arial", "B", 10)
        self.cell(col_width, row_height, "", border=1)
        for fruit in fruits:
            self.cell(col_width, row_height, fruit.title(), border=1)
        self.ln(row_height)

        # Nutrient rows
        self.set_font("Arial", "", 10)
        for nutrient in nutrients:
            self.cell(col_width, row_height, nutrient.replace("_", " ").title(), border=1)
            for fruit in fruits:
                val = all_data[fruit][nutrient]
                unit = "kcal" if nutrient == "calories" else "mg" if nutrient == "vitamin_c" else "g"
                self.cell(col_width, row_height, f"{val} {unit}", border=1)
            self.ln(row_height)

    def cleanup_temp_images(self):
        for path in self.temp_images:
            try:
                os.unlink(path)
            except Exception as e:
                print(f"Failed to delete temp file {path}: {e}")

# Streamlit UI
st.set_page_config(page_title="Fruit Detector + Nutrients", layout="wide")
st.title("🤖 Smartbite ")

uploaded_file = st.file_uploader("📤 Upload an image of fruits", type=["jpg", "jpeg", "png"])
serving_size = st.slider("🍽 Select serving size (grams)", 25, 200, 100, 25)
serving_factor = serving_size / 100

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    results = model.predict(image, conf=0.25)
    names = model.names
    fruit_counts = Counter(int(box.cls[0].item()) for box in results[0].boxes)

    # Resize for display
    resized_input = image.resize((300, int(image.height * 300 / image.width)))
    result_img = results[0].plot(pil=True)
    resized_result = result_img.resize((300, int(result_img.height * 300 / result_img.width)))

    left, right = st.columns(2)
    with left:
        st.image(resized_input, caption="Uploaded Image", use_container_width=False)
    with right:
        st.image(resized_result, caption="Detected Fruits", use_container_width=False)

    st.subheader("🧠 Detected Fruits and Nutritional Breakdown")
    total_fruits = sum(fruit_counts.values())
    st.markdown(f"### 🧮 Total Fruits Detected: **{total_fruits}**")

    all_data = {}
    for cls_id, count in fruit_counts.items():
        fruit = names[cls_id]
        st.markdown(f"---\n### 🤔 {fruit.title()} — Count: **{count}**")
        if fruit in nutrients:
            adjusted = {k: round(v * serving_factor, 2) for k, v in nutrients[fruit].items()}
            all_data[fruit] = adjusted

            display_data = {
                k: f"{v} kcal" if k == "calories" else f"{v}mg" if k == "vitamin_c" else f"{v}g"
                for k, v in adjusted.items()
            }
            df = pd.DataFrame(display_data, index=[f"{serving_size}g"])
            st.table(df.T)
        else:
            st.warning(f"No nutrient data for {fruit}")

    # Generate PDF
    pdf = PDF()
    pdf.add_page()
    pdf.add_images_side_by_side(image, result_img)
    pdf.add_nutrient_table(all_data, serving_size)

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join("reports", f"smartbite_report_{timestamp}.pdf")
    pdf.output(report_path)
    pdf.cleanup_temp_images()

    with open(report_path, "rb") as f:
        st.download_button("📥 Download Report as PDF", data=f.read(), file_name=f"smartbite_report_{timestamp}.pdf", mime="application/pdf")
