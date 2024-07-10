import streamlit as st
from datetime import datetime, timedelta

def validate_time(time):
    if time.hour < 10 or time.hour > 21:
        return True
    return False

def validation(name, phone, time, table_selected):
    if not name:
        #check name is fill or not
        st.warning("Harap masukkan nama Anda.")
        return False

    elif not phone:
        #check no.wa is fill or not
        st.warning("Harap masukkan nomor WhatsApp Anda.")
        return False
    
    elif not phone.isnumeric():
        #check nomor wa adalah angka dan bukan alfabet
        st.warning("Harap masukkan nomor WhatsApp Anda dengan benar.")
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


def reservation_id():
    name = st.text_input("Nama Pemesan", placeholder="Masukkan Nama Anda")
    phone = st.text_input("Nomor Whatsapp", placeholder="Masukkan Nomor WhatsApp Anda")
    date = st.date_input("Pilih Tanggal Reservasi", min_value=datetime.today())
    time = st.time_input("Pilih Waktu Reservasi")
    
    return name, phone, date, time


def home_page():
    st.title("Reservasi Online Restoran")
    name, phone, date, time = reservation_id()
    st.session_state.reservation_details = {
        'name': name,
        'phone': phone,
        'date': date,
        'time' : time
    }

    return name, phone, date, time



def get_button_style(clicked):
    if clicked:
        return """
            background-color: red; 
            color: white; 
            border: none; 
            padding: 15px 32px; 
            text-align: center; 
            text-decoration: none; 
            display: inline-block; 
            font-size: 16px; 
            margin: 4px 2px; 
            cursor: pointer; 
            border-radius: 4px;
        """
    else:
        return """
            background-color: blue; 
            color: white; 
            border: none; 
            padding: 15px 32px; 
            text-align: center; 
            text-decoration: none; 
            display: inline-block; 
            font-size: 16px; 
            margin: 4px 2px; 
            cursor: pointer; 
            border-radius: 4px;
            """




def tables():
    jumlah_meja = 9
    jumlah_kolom = 3
    cols = st.columns(jumlah_kolom)

    st.write("Pilih Meja")
    for i in range(jumlah_meja):
        if f"meja_{i+1}_clicked" not in st.session_state:
            st.session_state[f"meja_{i+1}_clicked"] = False

    for i in range(jumlah_meja):
        with cols[i % jumlah_kolom]:
            button_label = f"Meja {i + 1}"
            clicked_key = f"meja_{i+1}_clicked"
            button_style = get_button_style(st.session_state[clicked_key])
            button_html = f"""
            <button style="{button_style}" onclick="document.getElementById('{button_label}').click()">{button_label}</button>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            if st.button(button_label, key=button_label):
                st.session_state[clicked_key] = not st.session_state[clicked_key]
                st.experimental_rerun()

    total_meja = sum(1 for i in range(jumlah_meja) if st.session_state[f"meja_{i+1}_clicked"])
    total_harga = total_meja * 25000
    st.write(f"Total Meja yang Dipilih: {total_meja}")
    st.write(f"Total Harga: Rp {total_harga:,}")

    st.session_state.total_harga = total_harga

    return total_meja



def main():
    name, phone, date, time = home_page()
    total_meja = tables()
    pax = st.number_input("Jumlah Pax", min_value=1, value=1, step=1, format="%d")
    st.session_state.pax = pax  # Simpan nilai pax ke dalam session state

    
    if st.button("Konfirmasi & Bayar"):
        if (validation(name, phone, time, total_meja)):
            st.session_state.page = 'payment'
            st.experimental_rerun()




def payment():
    st.title("Halaman Pembayaran")

    reservation_details = f"""
    - **Nama Pemesan :** {st.session_state.reservation_details['name']}
    - **Nomor WhatsApp :** {st.session_state.reservation_details['phone']}
    - **Tanggal Reservasi :** {st.session_state.reservation_details['date']}
    - **Waktu Reservasi :** {st.session_state.reservation_details['time']}
    - **Meja :** { "" }
    - **Jumlah Pax :** { st.session_state.pax }
    - **Total Minimum DP :** Rp {st.session_state.total_harga:,}
    """

    st.markdown(reservation_details)
        
    dp = st.number_input("Input DP", min_value=0.0, value=0.0, step=0.1, format="%.2f")
    note = st.text_area("Tulis Catatan")
    if st.button("Konfirmasi Pembayaran"):
        st.write("Pembayaran dikonfirmasi.")
        st.write(f"Jumlah DP: {dp}")
        st.write(f"Catatan: {note}")
        st.session_state.page = 'main'

if 'page' not in st.session_state:
    st.session_state.page = 'main'




def app_main():
    if st.session_state.page == 'main':
        main()
    elif st.session_state.page == 'payment':
        payment()



app_main()
