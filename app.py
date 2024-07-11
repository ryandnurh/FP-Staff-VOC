import streamlit as st
from PIL import Image
from datetime import datetime


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
    jumlah_meja = 20
    jumlah_kolom = 5
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

    tables_selected = []

    for i in range(jumlah_meja):
        if st.session_state[f"meja_{i+1}_clicked"]:
            tables_selected.append(f"Meja {i + 1}")

    total_meja = sum(1 for i in range(jumlah_meja) if st.session_state[f"meja_{i+1}_clicked"])
    total_harga = total_meja * 25000
    st.write(f"Meja yang Dipilih: {', '.join(tables_selected)}")
    st.write(f"Total Meja yang Dipilih: {total_meja}")
    st.write(f"Total Harga: Rp {total_harga:,}")

    st.session_state.total_harga = total_harga
    st.session_state.tables_selected = tables_selected
    st.session_state.total_meja = total_meja




def check_cash_payments(dp, amount):
    change = dp-amount
    if dp < amount:
        st.warning(f"Uang anda masih kurang {change:,.0f}")
        return False
    
    elif dp>amount:
        st.session_state.greeting = f"Kembalian anda Rp {change:,.0f}. Terimakasih telah memesan, Berikut Detail Pemesanan anda."
        return True
    
    else:
        st.session_state.greeting = f"Terimakasih telah memesan, Berikut Detail Pemesanan anda."
        return True



def handle_payment_method_selection(amount):
        comma_amount = amount.replace(",", "")
        total_amount = int(comma_amount)
        payment_methods = ["Cash", "E-Wallet", "Transfer Bank"]
        transfer_methods = ["BCA","SEA BANK"]
        payment_method = st.selectbox("Pilih Metode Pembayaran", options=payment_methods)

        if payment_method == "Transfer Bank":

            transfer_method =st.selectbox("Pilih Bank", options=transfer_methods)

            if transfer_method == "BCA":
                st.info(f"Silahkan transfer ke BCA 4561034901 DAVA MOHAMMAD RIZKY sejumlah Rp {amount}")
            
            elif transfer_method =="SEA BANK":
                st.info(f"Silahkan transfer ke SEA BANK 901255803955 FEBRYAND NUR HIDAYAT sejumlah Rp {amount}")

            uploaded_file = st.file_uploader("Upload bukti", type=['png','jpg'])

            if uploaded_file is not None:
                st.image(uploaded_file)

            if st.button("Konfirmasi"):
                if uploaded_file is not None:
                    img = Image.open(uploaded_file)
                    img.save(f"uploaded-file/{uploaded_file.name}")

                    st.session_state.greeting = f"Berhasil mengupload ({uploaded_file.name}). Terimakasih telah memesan, Berikut Detail Pemesanan anda."
                    st.session_state.page = 'result'
                    st.experimental_rerun()

                else:
                    st.error("Silahkan Upload File terlebih dahulu")
        
        elif payment_method == "E-Wallet":
            st.error("Mohon Maaf, Pembayaran ini belum bisa digunakan")
        
        elif payment_method == "Cash":
            dp = st.number_input("Input DP", min_value=0.0, step=100.0, format="%.0f")
            note = st.text_area("Tulis Catatan (opsional)", placeholder="catatan anda...")
            
            st.session_state.note = f"{note}"

            if st.button("Konfirmasi Pembayaran"):
                if (check_cash_payments(dp,total_amount)):
                    st.session_state.page = 'result'
                    st.experimental_rerun()


def main():
    home_page()
    tables()
    pax = st.number_input("Jumlah Pax", min_value=1, value=1, step=1, format="%d")
    st.session_state.pax = pax  # Simpan nilai pax ke dalam session state

    name = st.session_state.reservation_details['name']
    phone = st.session_state.reservation_details['phone']
    time = st.session_state.reservation_details['time']
    total_meja = st.session_state.total_meja

    st.session_state.details = f"""
    - **Nama Pemesan :** {st.session_state.reservation_details['name']}
    - **Nomor WhatsApp :** {st.session_state.reservation_details['phone']}
    - **Tanggal Reservasi :** {st.session_state.reservation_details['date']}
    - **Waktu Reservasi :** {st.session_state.reservation_details['time']}
    - **Meja yang Dipilih:** {', '.join(st.session_state.tables_selected)}
    - **Total Meja yang Dipilih:** { st.session_state.total_meja }
    - **Jumlah Pax :** { st.session_state.pax }
    - **Total Minimum DP :** Rp {st.session_state.total_harga:,}
    """
    
    if st.button("Konfirmasi & Bayar"):
        if (validation(name, phone, time, total_meja)):
            st.session_state.page = 'payment'
            st.experimental_rerun()




def payment():
    st.title("Halaman Pembayaran")
    st.session_state.details
    total = f"{st.session_state.total_harga:,}"

    handle_payment_method_selection(total)

   
def result():

    # Display the success message from the session state
    if "greeting" in st.session_state:
        st.success(st.session_state.greeting)

    st.title("Detail Reservasi")
    st.session_state.details

    #cek apabila ada catatan
    if st.session_state.note:
        st.write(f"Note : {st.session_state.note}")
        details = st.session_state.details + f"\n- **Note :** {st.session_state.note}" #menambahkan catatan ke download detail
        
    else:
        st.write("Note: Tidak ada catatan yang diberikan.")
        details = st.session_state.details

    col1, col2 = st.columns(2)

    if col1.download_button(
        label="Download Detail Reservasi",
        data= details,
        file_name="reservation_details.txt",
        mime="text/plain"
    ):
        st.success("Download Berhasil")

    if col2.button("Buat Pesanan Lain"):
        st.session_state.page = 'main'
        st.experimental_rerun()
        
    
   

if 'page' not in st.session_state:
    st.session_state.page = 'main'




def app_main():
    if st.session_state.page == 'main':
        main()
    elif st.session_state.page == 'payment':
        payment()
    elif st.session_state.page == 'result':
        result()



app_main()
