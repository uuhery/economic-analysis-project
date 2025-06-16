# Economic Analysis and Decision Tool for Software Projects

This project is a web-based application for simulating cost estimation, investment analysis, risk modeling, and resource optimization in software engineering projects.

## 🔧 Structure

```

economic-analysis-project/
├── backend/   # Fastapi + MySQL backend
├── frontend/  # Vue 2 frontend
├── doc/  # Final Report
├── slides/  # PPT

````

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
````

### Frontend

```bash
cd frontend
npm install
npm run serve
```
📦 Recommended Node version: 16.15.0  

## 🧠 Modules

* COCOMO Estimation
* NPV/ROI/IRR Analysis
* Risk Simulation (MCS, Decision Tree)
* Resource Optimization
