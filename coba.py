

reservation_details = f"""
### Detail Reservasi Anda:
- **Nama:** {name}
- **Tanggal:** {date.strftime('%Y-%m-%d')}
- **Waktu:** {time.strftime('%H:%M')}
- **Meja:** {', '.join(table_selected)}
- **Jumlah Tamu:** {guests}
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
