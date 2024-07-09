import streamlit as st
from datetime import datetime, timedelta

def validate_time(time):
    if time.hour < 10 or time.hour > 21:
        return True
    return False

# Display the number of guests for each table
def display_guests(table_guests):
    guest=[]
    for table, guests in table_guests.items():
        guest.append(f" {table} : {guests} Tamu")
    return guest


# Confirm reservation
def validation(name, time, table_selected):
    if not name:
        #check name is fill or not
        st.warning("Harap masukkan nama Anda.")
        return False

    elif validate_time(time):
        #check if time correct or not
        st.warning("Waktu yang dipilih tidak valid. Silakan pilih waktu antara jam 10:00 hingga jam 21:00")
        return False
    
    elif not table_selected:
        # check if the table are selected
        st.warning("Silahkan Pilih Meja.")
        return False
    
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

# Create a dictionary to store the table selection and number of guests
table_guests = {}

for table in table_selected:
    table_guests[table] = st.number_input(f"Jumlah Tamu untuk {table}", min_value=1, step=1)



validation_check = validation(name, time, table_selected)

check = False

if (validation_check):

    
    if st.button("Konfirmasi"):
        check = True
    

if (check):
    
    reservation_details = f"""
    ### Detail Reservasi Anda:
    - **Nama:** {name}
    - **Tanggal:** {date.strftime('%Y-%m-%d')}
    - **Waktu:** {time.strftime('%H:%M')}
    - **Meja:** {', '.join(table_selected)}
    - **Jumlah Tamu:** { display_guests(table_guests) }
    """


    st.success("Reservasi berhasil dikonfirmasi!")
    st.markdown(reservation_details)

    # Payment confirmation step
    dp_amount = 25000 * len(table_selected)
    st.write(f"Total DP yang harus dibayar: Rp. {dp_amount:,}")

    st.write("Silakan bayar DP di kasir restoran.")
    st.write("Silakan masukkan jumlah DP yang dibayar:")
    dp_paid = st.number_input("Jumlah DP yang dibayar")
    if dp_paid >= dp_amount:
        st.success("DP berhasil dibayar!")
    else:
        st.error("Jumlah DP yang dibayar tidak sesuai. Silakan cek kembali.")


    st.button("Bayar") 

