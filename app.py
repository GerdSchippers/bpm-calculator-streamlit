import streamlit as st
import datetime
from fpdf import FPDF

# Donkere modus inschakelen
st.set_page_config(page_title="BPM Calculator", layout="wide")

# CSS om de webapp er als Autotelex uit te laten zien
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

# BPM Tarief en methodes
bruto_bpm = 1788  # Bruto BPM uit Autotelex

# Invoerpanelen
st.title("BPM Calculator 🚗💨")
st.write("Voer de gegevens van uw voertuig in:")

col1, col2 = st.columns(2)
with col1:
    datum_toelating = st.date_input("Datum eerste toelating")
    co2_wltp = st.number_input("CO2-uitstoot (WLTP, g/km)", min_value=0, value=100)
    brandstof = st.selectbox("Brandstofsoort", ["Benzine", "Diesel", "Elektriciteit", "LPG", "CNG"])
with col2:
    waarde_onbeschadigd = st.number_input("Handelsinkoopwaarde onbeschadigd (€)", min_value=0, value=10000)
    waarde_beschadigd = st.number_input("Handelsinkoopwaarde huidige staat (€)", min_value=0, value=5000)

afschrijfmethode = st.radio("Afschrijvingsmethode:", ["Forfaitair", "Koerslijst", "Taxatierapport"])

# Afschrijving berekenen
if afschrijfmethode == "Forfaitair":
    afschrijvingspercent = 39  # Afschrijving volgens Autotelex-tabel
elif afschrijfmethode == "Koerslijst":
    afschrijvingspercent = 25.69  # Autotelex koerslijst afschrijving
elif afschrijfmethode == "Taxatierapport":
    afschrijvingspercent = 71.48  # Autotelex taxatierapport afschrijving

# Netto BPM berekenen
netto_bpm = bruto_bpm * (100 - afschrijvingspercent) / 100
st.success(f"**Te betalen BPM: € {netto_bpm:,.2f}**")

# PDF Download functie
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Gebruik een lettertype dat UTF-8 ondersteunt
    pdf.add_font('Arial', '', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', uni=True)
    pdf.set_font("Arial", style='', size=12)

    pdf.cell(200, 10, "BPM Berekening Resultaat", ln=True, align='C')
    pdf.cell(200, 10, f"Datum eerste toelating: {datum_toelating}", ln=True)
    pdf.cell(200, 10, f"CO2-uitstoot WLTP: {co2_wltp} g/km", ln=True)
    pdf.cell(200, 10, f"Bruto BPM: € {bruto_bpm:,.2f}", ln=True)
    pdf.cell(200, 10, f"Afschrijvingsmethode: {afschrijfmethode}", ln=True)
    pdf.cell(200, 10, f"Afschrijvingspercentage: {afschrijvingspercent:.2f}%", ln=True)
    pdf.cell(200, 10, f"Te betalen BPM: € {netto_bpm:,.2f}", ln=True)

    return pdf.output(dest='S').encode('utf-8')


st.download_button("Download berekening als PDF", data=generate_pdf(), file_name="BPM_Berekening.pdf", mime="application/pdf")
