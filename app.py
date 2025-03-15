import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF

# Donkere modus inschakelen
st.set_page_config(page_title="BPM Calculator", layout="wide")
st.markdown(
    """
    <style>
    body { color: white; background-color: #0E1117; }
    .stTextInput, .stNumberInput, .stSelectbox, .stDateInput {
        background-color: #262730; color: white;
    }
    .stButton>button { background-color: #4CAF50; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# BPM Tarieven 2025
tarief_2025 = [
    {"min": 0,   "max": 78,  "basis": 667,   "pergram": 2},
    {"min": 79,  "max": 100, "basis": 825,   "pergram": 79},
    {"min": 101, "max": 140, "basis": 2563,  "pergram": 173},
    {"min": 141, "max": 156, "basis": 9483,  "pergram": 284},
    {"min": 157, "max": None, "basis": 14027, "pergram": 568}
]

def bereken_bruto_bpm(co2, tarief):
    """Berekent de bruto BPM op basis van CO2-uitstoot"""
    for schijf in tarief:
        if schijf["max"] is None or schijf["min"] <= co2 <= schijf["max"]:
            return schijf["basis"] + (co2 - schijf["min"]) * schijf["pergram"]
    return 0

# Invoerpanelen
st.title("BPM Calculator 🚗💨")
st.write("Voer de gegevens van uw voertuig in:")

col1, col2 = st.columns(2)
with col1:
    datum_toelating = st.date_input("Datum eerste toelating")
    co2_nedc = st.number_input("CO2-uitstoot (NEDC, g/km)", min_value=0, value=0)
    co2_wltp = st.number_input("CO2-uitstoot (WLTP, g/km)", min_value=0, value=0)
with col2:
    brandstof = st.selectbox("Brandstofsoort", ["Benzine", "Diesel", "Elektriciteit", "LPG", "CNG"])
    waarde_onbeschadigd = st.number_input("Handelsinkoopwaarde onbeschadigd (€)", min_value=0, value=0)
    waarde_beschadigd = st.number_input("Handelsinkoopwaarde huidige staat (€)", min_value=0, value=0)

afschrijfmethode = st.radio("Afschrijvingsmethode:", ["Forfaitair", "Koerslijst", "Taxatierapport"])

# BPM berekening
co2_waarde = min(co2_nedc, co2_wltp) if co2_nedc and co2_wltp else (co2_nedc if co2_nedc > 0 else co2_wltp)
bruto_bpm = bereken_bruto_bpm(co2_waarde, tarief_2025)

# Afschrijving bepalen
if afschrijfmethode == "Forfaitair":
    voertuig_leeftijd = (datetime.date.today() - datum_toelating).days // 30
    afschrijvingspercent = max(0, min(90, voertuig_leeftijd * 1.5))  # Simpele afschrijving van 1.5% per maand tot max 90%
elif afschrijfmethode == "Koerslijst":
    afschrijvingspercent = (1 - waarde_onbeschadigd / 30000) * 100 if waarde_onbeschadigd > 0 else 50
elif afschrijfmethode == "Taxatierapport":
    afschrijvingspercent = (1 - waarde_beschadigd / waarde_onbeschadigd) * 100 if waarde_onbeschadigd > 0 else 50

afschrijvingspercent = min(max(afschrijvingspercent, 0), 100)
netto_bpm = bruto_bpm * (100 - afschrijvingspercent) / 100

st.success(f"**Te betalen BPM: € {netto_bpm:,.2f}**")

# PDF Download functie
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='', size=12)
    pdf.cell(200, 10, "BPM Berekening Resultaat", ln=True, align='C')

    pdf.cell(200, 10, f"Datum eerste toelating: {datum_toelating}", ln=True)
    pdf.cell(200, 10, f"CO2-uitstoot gebruikt: {co2_waarde} g/km", ln=True)
    pdf.cell(200, 10, f"Bruto BPM: € {bruto_bpm:,.2f}", ln=True)
    pdf.cell(200, 10, f"Afschrijvingsmethode: {afschrijfmethode}", ln=True)
    pdf.cell(200, 10, f"Afschrijvingspercentage: {afschrijvingspercent:.2f}%", ln=True)
    pdf.cell(200, 10, f"Te betalen BPM: € {netto_bpm:,.2f}", ln=True)

    return pdf.output(dest='S').encode('latin-1')

st.download_button("Download berekening als PDF", data=generate_pdf(), file_name="BPM_Berekening.pdf", mime="application/pdf")
