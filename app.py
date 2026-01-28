# app.py - Professional Wildlife Poacher Detection
import time
import random
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from sklearn.metrics import roc_curve, auc, confusion_matrix

# ---------------------------------------------------------------------
# App config
# ---------------------------------------------------------------------
st.set_page_config(page_title="Wildlife Poacher Detection", page_icon="🐘", layout="wide")

# ---------------------------------------------------------------------
# Demo users
# ---------------------------------------------------------------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "ranger": {"password": "ranger123", "role": "Ranger"},
    "analyst": {"password": "analyst123", "role": "Analyst"},
    "researcher": {"password": "researcher123", "role": "Researcher"},
}

# ---------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------
if "auth" not in st.session_state: st.session_state.auth=False
if "user" not in st.session_state: st.session_state.user=None
if "role" not in st.session_state: st.session_state.role=None
if "alerts" not in st.session_state:
    st.session_state.alerts=pd.DataFrame(columns=["id","type","confidence","lat","lon","location","timestamp"])

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def generate_mock_alerts(n=10):
    types = ["Poacher","Vehicle","Animal","Ranger"]
    return pd.DataFrame({
        "id":[f"A{int(time.time()*1000)+i}" for i in range(n)],
        "type":np.random.choice(types,n),
        "confidence":np.random.randint(55,100,n),
        "lat":np.random.uniform(-1.5,1.5,n)+0.5,
        "lon":np.random.uniform(36.0,38.0,n),
        "location":np.random.choice(["Zone A","Zone B","Zone C"],n),
        "timestamp":[datetime.now().isoformat() for _ in range(n)]
    })

def append_new_alerts(k=5):
    new_df=generate_mock_alerts(k)
    st.session_state.alerts=pd.concat([new_df,st.session_state.alerts],ignore_index=True).drop_duplicates("id")

def auto_seed_data():
    if st.session_state.alerts.empty:
        append_new_alerts(20)

def kpi_counts(df):
    total=len(df)
    threats=len(df[df["type"].isin(["Poacher","Vehicle"])])
    animals=len(df[df["type"]=="Animal"])
    avg_conf=round(df["confidence"].mean(),1) if total else 0
    return total,threats,animals,avg_conf

def simulate_model_eval(df,n=200):
    if df.empty:
        y_true=np.random.binomial(1,0.2,size=n)
        y_score=np.random.rand(n)
        return y_true,y_score
    y_true=(df["type"]=="Poacher").astype(int).sample(min(n,len(df)),replace=True).to_numpy()
    y_score=df["confidence"].astype(float).sample(min(n,len(df)),replace=True).to_numpy()/100
    return y_true,y_score

# ---------------------------------------------------------------------
# Login Page
# ---------------------------------------------------------------------
def do_login():
    st.markdown("""
    <style>
    .login-card { max-width:420px; margin:10% auto; padding:30px; border-radius:12px;
                  background:rgba(255,255,255,0.05); backdrop-filter:blur(8px);
                  box-shadow:0 8px 30px rgba(0,0,0,0.5); text-align:center; }
    .login-title { font-size:32px; margin-bottom:8px; }
    .login-sub { font-size:16px; color:#ccc; margin-bottom:20px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🐘 Wildlife Poacher Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">AI-driven protection system. Please log in.</div>', unsafe_allow_html=True)

    user=st.text_input("Username")
    pwd=st.text_input("Password",type="password")
    if st.button("Login", use_container_width=True):
        if user in USERS and USERS[user]["password"]==pwd:
            st.session_state.auth=True
            st.session_state.user=user
            st.session_state.role=USERS[user]["role"]
            st.success(f"Welcome {user} ({st.session_state.role})")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Try admin/admin123 (demo)")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    do_login(); st.stop()

# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
auto_seed_data()
alerts_df=st.session_state.alerts.copy()
with st.sidebar:
    st.subheader(f"👋 {st.session_state.user} ({st.session_state.role})")
    page=st.radio("Navigate",["Dashboard","Live Map","Detections","Analytics","Reports","Admin","About"])
    if st.button("Add Mock Alerts"): append_new_alerts(5)
    if st.button("Logout"):
        st.session_state.auth=False; st.rerun()

# ---------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------
if page=="Dashboard":
    st.header("📊 Dashboard Overview")
    total,threats,animals,avg_conf=kpi_counts(alerts_df)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Alerts",total)
    c2.metric("Threats",threats)
    c3.metric("Animals",animals)
    c4.metric("Avg Confidence",f"{avg_conf}%")

    if not alerts_df.empty:
        fig=px.pie(alerts_df,names="type",title="Detection Distribution")
        st.plotly_chart(fig,use_container_width=True)

elif page=="Live Map":
    st.header("🌍 Live Map")
    center=[alerts_df["lat"].mean(),alerts_df["lon"].mean()]
    fmap=folium.Map(location=center,zoom_start=6,control_scale=True)

    folium.TileLayer("OpenStreetMap",name="Street Map").add_to(fmap)
    folium.TileLayer("Esri.WorldImagery",name="Satellite").add_to(fmap)

    HeatMap(alerts_df[["lat","lon"]].values.tolist(),radius=18).add_to(fmap)

    for _,row in alerts_df.iterrows():
        folium.Marker([row.lat,row.lon],
                      popup=f"{row.type} ({row.confidence}%) - {row.location}",
                      icon=folium.Icon(color="red" if row.type=="Poacher" else "blue")).add_to(fmap)

    folium.LayerControl().add_to(fmap)
    st_folium(fmap,width=1200,height=600)

elif page=="Detections":
    st.header("📑 Detection Records")
    st.dataframe(alerts_df,use_container_width=True)

elif page=="Analytics":
    st.header("📈 Analytics & Model Evaluation")
    total,threats,animals,avg_conf=kpi_counts(alerts_df)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total",total); c2.metric("Threats",threats)
    c3.metric("Animals",animals); c4.metric("Avg Conf",f"{avg_conf}%")

    alerts_df["ts"]=pd.to_datetime(alerts_df["timestamp"])
    over_time=alerts_df.groupby(alerts_df["ts"].dt.floor("H")).size().reset_index(name="count")
    if not over_time.empty:
        st.plotly_chart(px.line(over_time,x="ts",y="count",markers=True,title="Detections Over Time"),use_container_width=True)

    pivot=pd.crosstab(alerts_df["location"],alerts_df["type"])
    if not pivot.empty:
        st.plotly_chart(px.imshow(pivot,text_auto=True,aspect="auto",color_continuous_scale="YlOrRd",title="Heatmap"),use_container_width=True)

    y_true,y_score=simulate_model_eval(alerts_df,200)
    if len(np.unique(y_true))>1:
        fpr,tpr,_=roc_curve(y_true,y_score)
        roc_auc=auc(fpr,tpr)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=fpr,y=tpr,mode="lines",name="ROC",line=dict(color="blue")))
        fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Random",line=dict(dash="dash")))
        fig.update_layout(title=f"ROC Curve (AUC={roc_auc:.2f})",xaxis_title="FPR",yaxis_title="TPR")
        st.plotly_chart(fig,use_container_width=True)
        y_pred=(y_score>0.5).astype(int)
        cm=confusion_matrix(y_true,y_pred)
        st.plotly_chart(px.imshow(cm,text_auto=True,aspect="auto",color_continuous_scale="Blues",title="Confusion Matrix"),use_container_width=True)

elif page=="Reports":
    st.header("📂 Reports")
    total,threats,animals,avg_conf=kpi_counts(alerts_df)
    st.subheader("📊 Summary")
    st.write(f"**Total Alerts:** {total}, **Threats:** {threats}, **Animals:** {animals}, **Avg Confidence:** {avg_conf}%")

    st.subheader("📈 Detection Distribution")
    if not alerts_df.empty:
        st.plotly_chart(px.pie(alerts_df,names="type",title="Detection Summary"),use_container_width=True)

    st.subheader("📥 Export")
    st.download_button("Download CSV",alerts_df.to_csv(index=False).encode("utf-8"),"alerts.csv","text/csv")
    # (PDF export can be added with reportlab if needed)

elif page=="Admin":
    st.header("🛡️ Admin Console")
    if st.session_state.role!="Admin":
        st.warning("Admin only.")
    else:
        new_user=st.text_input("New Ranger Username")
        new_pass=st.text_input("New Ranger Password",type="password")
        admin_pass=st.text_input("Re-enter Admin Password",type="password")
        if st.button("Add Ranger"):
            if not new_user or not new_pass:
                st.error("Enter credentials")
            elif admin_pass==USERS["admin"]["password"]:
                if new_user in USERS: st.warning("User exists")
                else:
                    USERS[new_user]={"password":new_pass,"role":"Ranger"}
                    st.success(f"✅ Ranger {new_user} added")
            else: st.error("Invalid admin password")

elif page=="About":
    st.header("ℹ️ About Wildlife Poacher Detection System")
    st.write("""
    ### Overview  
    This project leverages **AI and data visualization** to detect and track potential wildlife poaching activities.  

    ### Features  
    - 📊 Real-time Dashboard with KPIs  
    - 🌍 Interactive Live Map (Street + Satellite)  
    - 🔥 Heatmaps and Analytics  
    - 📈 ROC Curves and Confusion Matrix for evaluation  
    - 🛡️ Admin Ranger Management  
    - 📂 Reports with Export  

    ### Technologies  
    - **Streamlit** for web app  
    - **Folium** for mapping  
    - **Plotly** for interactive charts  
    - **scikit-learn** for model simulation  

    ### Future Enhancements  
    - Integration with drone / IoT camera feeds  
    - Real-time anomaly detection using YOLOv8  
    - Automated ranger alerts via SMS/Email  

    ---  
    🔒 *Demo version – login with admin/admin123*  
    """)
