import pandas as pd
import random
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- Generate Mock Alerts ---------------- #
def generate_mock_alerts(n=10):
    """Simulate random detections of poachers/animals."""
    threat_types = ["Poacher", "Animal", "Vehicle", "Ranger"]
    locations = ["Zone A", "Zone B", "Zone C", "Zone D"]

    data = []
    for _ in range(n):
        t_type = random.choice(threat_types)
        conf = random.randint(60, 99)
        lat = round(random.uniform(1.0, 2.5), 4)
        lon = round(random.uniform(31.0, 33.0), 4)
        loc = random.choice(locations)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append([t_type, conf, lat, lon, loc, timestamp])

    df = pd.DataFrame(data, columns=["type", "confidence", "lat", "lon", "location", "timestamp"])
    return df


# ---------------- Export to CSV ---------------- #
def export_to_csv(df, filename="detections.csv"):
    df.to_csv(filename, index=False)


# ---------------- Export to PDF ---------------- #
def export_to_pdf(df, filename="detections.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Wildlife Poacher Detection Report", styles["Heading1"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))

    # Convert DF to Table
    table_data = [list(df.columns)] + df.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.green),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 10),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
