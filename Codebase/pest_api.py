def get_pest_risk(crop="wheat"):
    levels = {"wheat": "🟠 Medium", "rice": "🔴 High", "maize": "🟢 Low", "sugarcane": "🟠 Medium"}
    risk = levels.get(crop.lower(), "❓ Unknown")
    recs = [
        "🔍 Monitor fields weekly for early signs of infestation",
        "🪰 Use pheromone traps if risk is High",
    ]
    return {"crop": crop, "risk_level": risk, "recommendations": recs}
