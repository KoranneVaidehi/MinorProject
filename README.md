# Deepfake Detection System (NAV-SMFS)

A web-based Deepfake Detection System that identifies manipulated facial content using Deep Learning techniques. The system analyzes facial features, detects inconsistencies, and classifies media as real or fake.

---

## Features

* Face Detection using MTCNN
* Facial Landmark Extraction
* Deep Learning-based Classification (CNN)
* Heatmap Visualization for fake regions
* Probability Score Output
* Web-based Interface (Django)

---

## Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Django (Python)
* **Database:** MongoDB Atlas
* **Machine Learning:** TensorFlow / PyTorch
* **Libraries:** OpenCV, NumPy, MTCNN

---

## System Workflow

1. Upload Image/Video
2. Face Detection using MTCNN
3. Extract Facial Landmarks
4. Feature Processing
5. Deepfake Classification
6. Heatmap Generation
7. Display Result (Real/Fake with score)

---

## Project Structure

```
NAV-SMFS/
│── backend/
│   │── models/
│   │── views.py
│   │── urls.py
│   │── utils/
│
│── frontend/
│   │── templates/
│   │── static/
│
│── dataset/
│── trained_model/
│── manage.py
│── requirements.txt
```

---

## How to Run

### 1. Clone Repository

```bash
git clone https://github.com/KoranneVaidehi/MinorProject
cd NAV-SMFS
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Server

```bash
python manage.py runserver
```

---

## Output

* Displays whether the media is **Real or Fake**
* Shows **confidence score**
* Visualizes manipulated regions using **heatmap**

---

## Use Cases

* Social Media Content Verification
* Fake News Detection
* Digital Media Forensics
* Identity Fraud Prevention

---

## Future Enhancements

* Real-time video detection
* Mobile application integration
* Improved model accuracy with larger datasets
* API integration for third-party use

---

## Contributors

* Vaidehi Koranne
* Yeswanth Yadav
* Shivani Barot
* Jaykumar Panchal

---

## License

This project is for academic and research purposes only.
