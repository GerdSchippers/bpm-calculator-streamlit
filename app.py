import streamlit as st

st.title("BPM Calculator")
st.write("Voer de gegevens van uw voertuig in:")

# Invoervelden
datum_toelating = st.date_input("Datum eerste toelating")
co2_nedc = st.number_input("CO2-uitstoot (NEDC, g/km)", min_value=0)
co2_wltp = st.number_input("CO2-uitstoot (WLTP, g/km)", min_value=0)
brandstof = st.selectbox("Brandstofsoort", ["Benzine", "Diesel", "Elektriciteit", "LPG", "CNG"])

# Eenvoudige testberekening
if co2_nedc > 0 or co2_wltp > 0:
    st.success(f"Je BPM wordt berekend op basis van CO2-uitstoot ({min(co2_nedc, co2_wltp)} g/km).")
