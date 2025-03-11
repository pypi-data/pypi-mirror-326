import os
import requests
import cv2
from ultralytics import YOLO
import pytesseract
import easyocr

# مسیر مدل و لینک دانلود
MODEL_PATH = r'C:\ProgramFiles\license_plate_detector.pt'
MODEL_URL = 'https://raw.githubusercontent.com/mahdihuseine/object.detector/main/object/detector/models/license_plate_detector.pt'

# در صورت نیاز مسیر اجرایی Tesseract را مشخص کنید (برای ویندوز)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class PlateRecognition:
    def __init__(self):
        self._ensure_model_exists()
        self.license_plate_detector = YOLO(MODEL_PATH)
        self.reader = easyocr.Reader(['en'])

    def _ensure_model_exists(self):
        """دانلود مدل در صورت عدم وجود"""
        if not os.path.exists(MODEL_PATH):
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            response = requests.get(MODEL_URL)
            if response.status_code == 200:
                with open(MODEL_PATH, 'wb') as f:
                    f.write(response.content)
            else:
                raise Exception("خطا در دانلود مدل!")

    def detect_plate(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("تصویر مورد نظر یافت نشد!")
        plates_dir = 'plates'
        if not os.path.exists(plates_dir):
            os.makedirs(plates_dir)
        
        results = self.license_plate_detector(image)
        detections = results[0].boxes.data.tolist()
        
        if len(detections) == 0:
            raise ValueError("هیچ پلاکی شناسایی نشد!")
        
        detections = sorted(detections, key=lambda d: d[4], reverse=True)
        best_detection = detections[0]
        x1, y1, x2, y2, score, class_id = best_detection
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        
        plate_img = image[y1:y2, x1:x2]
        plate_path = os.path.join(plates_dir, 'plate.jpg')
        cv2.imwrite(plate_path, plate_img)

        plate_info_path = os.path.join(plates_dir, 'plate_info.txt')
        with open(plate_info_path, 'w', encoding='utf-8') as f:
            f.write(f"x1 = {x1}\n")
            f.write(f"y1 = {y1}\n")
            f.write(f"x2 = {x2}\n")
            f.write(f"y2 = {y2}\n")
        
        plate_info = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "plate_path": plate_path
        }
        
        return plate_img, plate_info

    def extract_text(self, plate_img):
        config_tesseract = '--psm 7'
        tesseract_text = pytesseract.image_to_string(plate_img, config=config_tesseract).strip()
        easyocr_result = self.reader.readtext(plate_img, detail=0)
        easyocr_text = " ".join(easyocr_result)
        return {
            "tesseract": tesseract_text,
            "easyocr": easyocr_text
        }
