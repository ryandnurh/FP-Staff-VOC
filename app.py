import streamlit as st
from datetime import datetime, timedelta

def validate_time(time):
    if time.hour < 10 or time.hour > 21:
        return True
    return False

# Confirm reservation
def validation(name, time, table_selected):
    if not name:
        #check name is fill or not
        return False, st.warning("Harap masukkan nama Anda.")

    elif validate_time(time):
        #check if time correct or not
        return st.warning("Waktu yang dipilih tidak valid. Silakan pilih waktu antara jam 10:00 hingga jam 21:00")
    
    elif not table_selected:
        # check if the table are selected
        return st.warning("Silahkan Pilih Meja.")
    
    else:
        # Display the reservation details
        return True

# Set the page title and layout
st.set_page_config(page_title="Reservasi Online Restoran", layout="centered")

# Title of the app
st.title("Reservasi Online Restoran")

# Input for the user's name
name = st.text_input("Nama Anda")

# Date input for the reservation
date = st.date_input("Pilih Tanggal Reservasi", min_value=datetime.today())

# Time input for the reservation
time = st.time_input("Pilih Waktu Reservasi")



# Table selection
tables = ["Meja 1", "Meja 2", "Meja 3", "Meja 4", "Meja 5"]
table_selected = st.multiselect("Pilih Meja", tables)

# Number input for the number of guests
guests = st.number_input("Jumlah Tamu", min_value=1, step=1)

validation_check = validation(name, time, table_selected)

st.button(label = "Konfirmasi")
