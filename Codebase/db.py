import sqlite3
import pandas as pd

DB_FILE = "farm_database.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS farms (
            Farm_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Soil_pH REAL CHECK(Soil_pH BETWEEN 0 AND 14),
            Soil_Moisture REAL CHECK(Soil_Moisture BETWEEN 0 AND 100),
            Temperature REAL,
            Rainfall REAL,
            Crop_Type TEXT,
            Fertilizer_Usage REAL,
            Crop_Yield_ton REAL,
            Sustainability_Score REAL CHECK(Sustainability_Score BETWEEN 0 AND 100),
            Carbon_Footprint REAL
        )
        """
    )
    cursor.execute("PRAGMA table_info(farms)")
    cols = [col[1] for col in cursor.fetchall()]
    if "Carbon_Footprint" not in cols:
        cursor.execute("ALTER TABLE farms ADD COLUMN Carbon_Footprint REAL")
    conn.commit()
    conn.close()

def insert_farm(
    Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type,
    Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score, Carbon_Footprint,
):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO farms (Soil_pH, Soil_Moisture, Temperature, Rainfall,
                          Crop_Type, Fertilizer_Usage, Crop_Yield_ton,
                          Sustainability_Score, Carbon_Footprint)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            Soil_pH, Soil_Moisture, Temperature, Rainfall, Crop_Type,
            Fertilizer_Usage, Crop_Yield_ton, Sustainability_Score, Carbon_Footprint,
        ),
    )
    conn.commit()
    conn.close()

def fetch_all_farms():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farms ORDER BY Farm_ID ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    return pd.DataFrame(rows, columns=cols)

def update_farms(df):
    conn = connect_db()
    df.to_sql("temp_farms", conn, if_exists="replace", index=False)
    cur = conn.cursor()
    cur.executescript(
        """
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
            Sustainability_Score REAL CHECK(Sustainability_Score BETWEEN 0 AND 100),
            Carbon_Footprint REAL
        );
        INSERT INTO farms SELECT * FROM temp_farms;
        UPDATE sqlite_sequence SET seq = (SELECT MAX(Farm_ID) FROM farms) WHERE name = 'farms';
        DROP TABLE temp_farms;
        """
    )
    conn.commit()
    conn.close()

def delete_farm_by_id(farm_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM farms WHERE Farm_ID = ?", (farm_id,))
    conn.commit()
    conn.execute("VACUUM")
    conn.close()
