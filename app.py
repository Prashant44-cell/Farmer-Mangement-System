import streamlit as st
import sqlite3
import pandas as pd
import requests
import ollama

# --- DATABASE SETUP & FUNCTIONS ---
DB_FILE = 'farm_database.db'

def connect_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farms (
            Farm_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Soil_pH REAL CHECK(Soil_pH BETWEEN 0 AND 14),
            Soil_Moisture REAL CHECK(Soil_Moisture BETWEEN 0 AND 100),
            Temperature REAL,
            Rainfall REAL,
            Crop_Type TEXT,
            Fertilizer_Usage REAL,
            Crop_Yield_ton REAL,
            Sustainability_Score REAL CHECK(Sustainability_Score BETWEEN 0 AND 100)
        )
    ''')
    conn.commit()
    conn.close()

def insert_farm(Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type, Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO farms (Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type, Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type, Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score))
    conn.commit()
    conn.close()

def fetch_all_farms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farms ORDER BY Farm_ID ASC")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=columns)

def update_farms(dataframe):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create temporary table with new data
    dataframe.to_sql('temp_farms', conn, if_exists='replace', index=False)
    
    # Rebuild main table with correct schema
    cursor.executescript('''
        DROP TABLE IF EXISTS farms;
        CREATE TABLE farms (
            Farm_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Soil_pH REAL CHECK(Soil_pH BETWEEN 0 AND 14),
            Soil_Moisture REAL CHECK(Soil_Moisture BETWEEN 0 AND 100),
            Temperature REAL,
            Rainfall REAL,
            Crop_Type TEXT,
            Fertilizer_Usage REAL,
            Crop_Yield_ton REAL,
            Sustainability_Score REAL CHECK(Sustainability_Score BETWEEN 0 AND 100)
        );
        
        INSERT INTO farms SELECT * FROM temp_farms;
        UPDATE sqlite_sequence SET seq = (SELECT MAX(Farm_ID) FROM farms) WHERE name = 'farms';
        DROP TABLE temp_farms;
    ''')
    conn.commit()
    conn.close()

def delete_farm_by_id(farm_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM farms WHERE Farm_ID = ?", (farm_id,))
    conn.commit()
    cursor.execute("VACUUM")
    conn.close()

# --- AI SUGGESTION FUNCTION ---
def generate_ai_suggestion(farm_data):
    prompt = f"""As an agricultural AI expert, analyze this farm data:
    - Soil pH: {farm_data['Soil_pH']}
    - Soil Moisture: {farm_data['Soil_Moisture']}%
    - Temperature: {farm_data['Temperature']}°C
    - Rainfall: {farm_data['Rainfall']}mm
    - Crop Type: {farm_data['Crop_Type']}
    - Fertilizer Usage: {farm_data['Fertilizer_Usage']}kg
    - Crop Yield: {farm_data['Crop_Yield_ton']} tons
    - Sustainability Score: {farm_data['Sustainability_Score']}/100

    Provide 2-3 concise, practical suggestions to improve sustainability and crop yield. 
    Focus on specific, actionable steps with brief explanations. Use bullet points."""
    
    try:
        response = ollama.generate(
            model='phi3',
            prompt=prompt,
            stream=True,
            options={'temperature': 0.7, 'max_tokens': 300}
        )
        return response
    except Exception as e:
        return f"AI Suggestion unavailable: {str(e)}"

# --- WEATHER FUNCTION ---
def get_weather(city="Delhi"):
    API_KEY = "ccfceca6ac6c6f170a961f260287ab24"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return {
                "City": city,
                "Temperature": data['main']['temp'],
                "Weather": data['weather'][0]['description'],
                "Humidity": data['main']['humidity'],
                "Wind Speed": data['wind']['speed'],
                "Pressure": data['main']['pressure'],
                "Visibility": data.get('visibility', 'N/A')
            }
        else:
            return {"Error": data.get("message", "Unable to fetch data.")}
    except Exception as e:
        return {"Error": str(e)}

# --- STREAMLIT CONFIG & STYLING ---
st.set_page_config(page_title="Farm Management System", page_icon="🌾", layout="wide")
init_db()

# Custom CSS styles with hover effects
st.markdown("""
    <style>
    .stApp {
        background: url('https://c4.wallpaperflare.com/wallpaper/674/65/161/children-farmers-farm-field-wallpaper-preview.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: -1;
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    .weather-card:hover {
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .developer-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .developer-section:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.15);
    }
    /* Data editor hover effects */
    .stDataEditor .table-row:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    .stDataEditor th:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    /* Button hover effects */
    .stButton>button {
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    /* Tooltip styling */
    .stTooltip {
        background: rgba(0, 0, 0, 0.8) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP PAGES ---
def home_page():
    st.title("🌦️ Smart Farm Weather Dashboard")
    city = st.text_input("Enter City", "Delhi")
    
    if st.button("Get Weather Analysis"):
        result = get_weather(city)
        if "Error" in result:
            st.error(result["Error"])
        else:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
                    <div class='weather-card'>
                        <h2>{result['City']}</h2>
                        <div style='font-size: 40px;'>🌡️</div>
                        <h3>{result['Temperature']}°C</h3>
                        <p>{result['Weather'].capitalize()}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                cols = st.columns(3)
                metrics = [
                    ("💧", "Humidity", f"{result['Humidity']}%"),
                    ("💨", "Wind Speed", f"{result['Wind Speed']} m/s"),
                    ("📊", "Pressure", f"{result['Pressure']} hPa")
                ]
                
                for idx, (icon, title, value) in enumerate(metrics):
                    with cols[idx]:
                        st.markdown(f"""
                            <div class='weather-card'>
                                <div style='font-size: 30px;'>{icon}</div>
                                <h4>{title}</h4>
                                <p>{value}</p>
                            </div>
                        """, unsafe_allow_html=True)

def register_page():
    st.title("📝 Entry")
    with st.form("farm_form"):
        col1, col2 = st.columns(2)
        with col1:
            Soil_pH = st.slider("Soil pH", 0.0, 14.0, 6.8, 0.1,
                               help="Optimal pH range for most crops: 5.5-7.0")
            Soil_Moisture = st.slider("Soil Moisture (%)", 0.0, 100.0, 60.0,
                                      help="Ideal range: 50-80% for most crops")
            Temperature = st.number_input("Temperature (°C)", -30.0, 60.0, 25.0,
                                         help="Average daily temperature")
            Rainfall = st.number_input("Rainfall (mm)", 0.0, 1000.0, 100.0,
                                      help="Annual rainfall measurement")
        with col2:
            Crop_Type = st.selectbox("Crop Type", ["Wheat", "Maize", "Potato", "Rice", "Sugarcane", "Mustard"],
                                    help="Select the primary crop type")
            Fertilizer_Usage = st.number_input("Fertilizer Usage (kg)", 0.0, 1000.0, 250.0,
                                              help="Total fertilizer used per hectare")
            Crop_Yield_ton = st.number_input("Crop Yield (tons)", 0.0, 100.0, 5.0,
                                            help="Total yield per hectare")
            Sustainability_Score = st.slider("Sustainability Score", 0, 100, 85,
                                           help="Composite score considering environmental impact")

        if st.form_submit_button("Save Record"):
            try:
                insert_farm(Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type, Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score)
                st.success("✅ Farm record saved successfully!")
                farm_data = {
                    'Soil_pH': Soil_pH,
                    'Soil_Moisture': Soil_Moisture,
                    'Temperature': Temperature,
                    'Rainfall': Rainfall,
                    'Crop_Type': Crop_Type,
                    'Fertilizer_Usage': Fertilizer_Usage,
                    'Crop_Yield_ton': Crop_Yield_ton,
                    'Sustainability_Score': Sustainability_Score
                }
                st.subheader("🤖 AI Suggestions")
                with st.spinner("Analyzing farm data..."):
                    response = generate_ai_suggestion(farm_data)
                    if isinstance(response, str):
                        st.error(response)
                    else:
                        st.write_stream(chunk['response'] for chunk in response)
            except Exception as e:
                st.error(f"Database error: {e}")

def database_page():
    st.title("📊 Farm Data History")
    df = fetch_all_farms()
    
    if df.empty:
        st.info("No farm records found.")
    else:
        st.subheader("Edit Existing Records")
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            column_config={
                "Farm_ID": st.column_config.NumberColumn(
                    "Farm ID",
                    disabled=True,
                    help="Unique farm identifier"
                ),
                "Soil_pH": {
                    "help": "Soil acidity/alkalinity (0-14 scale)",
                    "format": "%.1f"
                },
                "Soil_Moisture": {
                    "help": "Water content in soil (%)",
                    "format": "%.1f%%"
                },
                "Temperature": {
                    "help": "Average temperature (°C)",
                    "format": "%.1f°C"
                },
                "Rainfall": {
                    "help": "Annual precipitation (mm)",
                    "format": "%.1f mm"
                },
                "Crop_Type": {
                    "help": "Type of cultivated crop"
                },
                "Fertilizer_Usage": {
                    "help": "Fertilizer applied per hectare (kg)",
                    "format": "%.1f kg"
                },
                "Crop_Yield_ton": {
                    "help": "Yield per hectare (metric tons)",
                    "format": "%.1f t"
                },
                "Sustainability_Score": {
                    "help": "Environmental impact score (0-100)",
                    "format": "%d/100"
                }
            }
        )
        
        if st.button("💾 Save All Changes"):
            try:
                update_farms(edited_df)
                st.success("✅ Changes saved successfully!")
            except Exception as e:
                st.error(f"Error saving changes: {e}")

        st.subheader("Delete Records")
        col1, col2 = st.columns(2)
        with col1:
            delete_id = st.number_input("Enter Farm ID to delete", min_value=1, step=1,
                                       help="Enter the Farm ID to permanently delete")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Selected Record"):
                try:
                    delete_farm_by_id(delete_id)
                    st.success(f"Farm ID {delete_id} deleted successfully.")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error deleting record: {e}")

def bulk_csv_upload_page():
    st.title("🗂️ Load Your Data")
    uploaded_files = st.file_uploader("Drag and drop CSV files here or click to browse", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_csv(file)
                st.subheader(f"📄 {file.name}")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Could not read {file.name}: {e}")

def developer_info_page():
    st.title("👨💻 Developer Hub")
    
    with st.expander("📌 Developer Information", expanded=True):
        st.markdown("""
            <div class='developer-section'>
                <h3>Developed by -Prashant Gupta</h3>
                <p>📧 Gmail: prashantvyahut@gmail.com<br>
                LinkedIn-Prashant Gupta<br>
                📞 Contact: +91 8986430667</p>
            </div>
        """, unsafe_allow_html=True)
        
    
    feedback = st.text_area("💬 Your valuable feedback")
    
    if st.button("📤 Submit Feedback"):
        if feedback:
            st.success("🙏 Thank you for your feedback! We'll use it to improve the system.")
        else:
            st.warning("Please write some feedback before submitting.")

# --- MAIN APP ROUTING ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Home", "Register Farm", "History", "CSV Upload", "Developer Hub"])

    if page == "Developer Hub":
        developer_info_page()
    elif page == "Home":
        home_page()
    elif page == "Register Farm":
        register_page()
    elif page == "History":
        database_page()
    elif page == "CSV Upload":
        bulk_csv_upload_page()

if __name__ == "__main__":
    main()
