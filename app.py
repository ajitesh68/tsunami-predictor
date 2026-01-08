import streamlit as st
import joblib  
import numpy as np
import pandas as pd


try:
   
    with open('tsunami_model.pkl', 'rb') as f:
        model = joblib.load(f)
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

st.set_page_config(page_title="Tsunami Prediction AI", page_icon="🌊")
st.title("🌊 Tsunami Prediction System")

with st.expander("Event Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        magnitude = st.number_input("Magnitude", 0.0, 10.0, 7.5, format="%.2f")
        depth = st.number_input("Depth (km)", 0.0, 1000.0, 10.0, format="%.2f")
        latitude = st.number_input("Latitude", -90.0, 90.0, 0.0, format="%.4f")
        longitude = st.number_input("Longitude", -180.0, 180.0, 0.0, format="%.4f")
        nst = st.number_input("NST (Number of Stations)", 0, 1000, 20)
        gap = st.number_input("Gap", 0.0, 360.0, 50.0, format="%.2f")

    with col2:
        cdi = st.number_input("CDI Intensity", 0.0, 12.0, 5.0, format="%.2f")
        mmi = st.number_input("MMI Intensity", 0.0, 12.0, 5.0, format="%.2f")
        sig = st.number_input("Significance", 0.0, 3000.0, 500.0, format="%.2f")
        dmin = st.number_input("Dmin (Distance to Station)", 0.0, 100.0, 1.0, format="%.2f")
        date_input = st.date_input("Date of Event")

if st.button("Predict Tsunami Risk", type="primary"):
    data = {}
    
   
    data['magnitude'] = magnitude; data['cdi'] = cdi; data['mmi'] = mmi
    data['sig'] = sig; data['nst'] = nst; data['dmin'] = dmin
    data['gap'] = gap; data['depth'] = depth; data['latitude'] = latitude
    data['longitude'] = longitude
    data['Year'] = date_input.year
    data['Month'] = date_input.month

    

    data['magnitude_squared'] = magnitude ** 2
    data['magnitude_cubed'] = magnitude ** 3
    data['depth_squared'] = depth ** 2
    data['log_depth'] = np.log1p(depth)
    data['log_sig'] = np.log1p(sig)
    data['log_nst'] = np.log1p(nst)
    
  
    data['mag_depth_product'] = magnitude * depth
    data['mag_depth_ratio'] = magnitude / (depth + 1)
    data['mag_sig_ratio'] = magnitude / (sig + 1)
    data['cdi_mmi_ratio'] = cdi / (mmi + 0.1)
    data['intensity_product'] = cdi * mmi
    

    data['abs_latitude'] = abs(latitude)
    data['equator_distance'] = abs(latitude)
    data['northern_hemisphere'] = 1 if latitude > 0 else 0

    data['pacific_region'] = 1 if (longitude >= 120) or (longitude <= -60) else 0


    data['is_shallow'] = 1 if depth <= 70 else 0
    data['is_very_shallow'] = 1 if depth <= 35 else 0
    data['is_major_quake'] = 1 if magnitude >= 7.5 else 0
    data['is_great_quake'] = 1 if magnitude >= 8.0 else 0
    
    
    data['is_summer'] = 1 if data['Month'] in [6, 7, 8] else 0
    data['is_winter'] = 1 if data['Month'] in [12, 1, 2] else 0
    data['quarter'] = ((data['Month'] - 1) // 3) + 1

    
    data['network_coverage'] = nst / (gap + 1)
    
    
    data['detection_quality'] = 1 / (dmin + 0.01)
    
   
    depth_part = 100 - (depth / 7)
    if depth_part < 0: depth_part = 0
    
    data['risk_score'] = (
        (magnitude / 10) * 0.35 + 
        (depth_part) * 0.25 + 
        (sig / 1000) * 0.20 + 
        (mmi / 12) * 0.20
    )

   
    if magnitude < 6.5:
        data['magnitude_category'] = 0 
    elif magnitude < 7.0:
        data['magnitude_category'] = 0
    elif magnitude < 7.5:
        data['magnitude_category'] = 1 
    elif magnitude < 8.0:
        data['magnitude_category'] = 2 
    else:
        data['magnitude_category'] = 3 

    
    if depth <= 35:
        data['depth_risk_category'] = 3 
    elif depth <= 70:
        data['depth_risk_category'] = 2 
    elif depth <= 300:
        data['depth_risk_category'] = 1 
    else:
        data['depth_risk_category'] = 0 

   

   
    cols = ['magnitude', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude', 
            'Year', 'Month', 'magnitude_category', 'risk_score', 'mag_depth_ratio', 'mag_depth_product', 
            'is_shallow', 'is_very_shallow', 'depth_risk_category', 'is_major_quake', 'is_great_quake', 
            'abs_latitude', 'equator_distance', 'northern_hemisphere', 'pacific_region', 'cdi_mmi_ratio', 
            'intensity_product', 'mag_sig_ratio', 'network_coverage', 'detection_quality', 'is_summer', 
            'is_winter', 'quarter', 'magnitude_squared', 'depth_squared', 'magnitude_cubed', 'log_depth', 
            'log_sig', 'log_nst']
            
    df_input = pd.DataFrame([data], columns=cols)
    
   
    try:
        prediction = model.predict(df_input)
        
        st.markdown("---")
        if prediction[0] == 1:
            st.error("### ⚠️ HIGH TSUNAMI RISK DETECTED")
            st.write("This earthquake has a high probability of generating a tsunami.")
        else:
            st.success("### ✅ LOW TSUNAMI RISK")
            st.write("This earthquake is unlikely to generate a significant tsunami.")
            
    except Exception as e:
        st.error(f"Prediction Error: {e}")