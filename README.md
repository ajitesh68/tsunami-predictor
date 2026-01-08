# 🌊 Tsunami Prediction 

A Machine Learning application that predicts the risk of a tsunami following an earthquake. 
Built with **Python**, **Streamlit**, and **Scikit-Learn**.

## 🚀 Live Demo
[Click here to view the App]https://ajitesh68-tsunami-predictor-app-mv7dfm.streamlit.app/


## 🧠 How It Works
This model analyzes real-time earthquake parameters to classify tsunami risk:
* **Magnitude & Depth:** The core physics of tsunami generation.
* **Geospatial Data:** Checks if the quake is in the "Ring of Fire".
* **Intensity Metrics:** CDI, MMI, and Significance.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Model:** Random Forest Classifier (Scikit-Learn)
* **Data Processing:** Pandas & NumPy

## 📂 Project Structure
* `app.py`: The main application logic.
* `tsunami_model.pkl`: The pre-trained ML model.
* `tsunami-prediction.ipynb`: The research notebook used to train the model.

## 📦 How to Run Locally
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/tsunami-predictor.git](https://github.com/YOUR_USERNAME/tsunami-predictor.git)

   pip install -r requirements.txt

   streamlit run app.py
