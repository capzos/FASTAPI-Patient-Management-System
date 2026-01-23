# 🏥 Patient Management System – FastAPI

A fully functional **FastAPI-based REST API** for managing patient records, including BMI calculation and health verdicts.

---

## 🚀 Features

- Create, view, update, delete patients
- Automatic BMI calculation
- Health verdict based on BMI
- Sorting patients by height, weight, or BMI
- Data persistence using JSON file
- Input validation using Pydantic

---

## 🛠️ Tech Stack

- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **Python**

---


## API ENDPOINTS

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| GET    | `/`                            | Home               |
| GET    | `/viewpatients`                | View all patients  |
| GET    | `/viewpatient/{id}`            | View patient by ID |
| POST   | `/createpatient`               | Create new patient |
| PUT    | `/updatepatient/{id}`          | Update patient     |
| DELETE | `/deletepatient/{id}`          | Delete patient     |
| GET    | `/sort?sort_by=bmi&order=desc` | Sort patients      |


---


## 📊 BMI Verdict Logic

```
< 18.5 → Underweight

18.5 – 24.9 → Normal weight

25 – 29.9 → Overweight

>= 30 → Obesity
```


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/capzos/FASTAPI-Patient-Management-System
cd patient-management-fastapi
```

## 2️⃣ Create virtual environment (optional)

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

## 4️⃣ Run the server

```
uvicorn app.main:app --reload
```
