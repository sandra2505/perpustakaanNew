
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistem Perpustakaan", layout="wide")
st.title(" Sistem Perpustakaan Sekolah")

# Inisialisasi data
if "books" not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=["ID", "Judul", "Penulis", "Kategori", "Stok"])

if "members" not in st.session_state:
    st.session_state.members = pd.DataFrame(columns=["ID", "Nama", "Kelas/Alamat"])

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Nama", "Judul Buku", "Tanggal Pinjam", "Tanggal Kembali", "Status"])

tab1, tab2, tab3, tab4 = st.tabs(["📘 Buku", "👥 Anggota", "🔁 Peminjaman", "📊 Riwayat"])

with tab1:
    st.header("📘 Data Buku")
    with st.form("add_book"):
        col1, col2, col3 = st.columns(3)
        with col1:
            judul = st.text_input("Judul Buku")
        with col2:
            penulis = st.text_input("Penulis")
        with col3:
            kategori = st.text_input("Kategori")
        stok = st.number_input("Stok", 1, 100)
        submitted = st.form_submit_button("Tambah Buku")
        if submitted:
            new_book = {
                "ID": len(st.session_state.books) + 1,
                "Judul": judul,
                "Penulis": penulis,
                "Kategori": kategori,
                "Stok": stok
            }
            st.session_state.books = pd.concat([st.session_state.books, pd.DataFrame([new_book])], ignore_index=True)
            st.success("✅ Buku berhasil ditambahkan.")

    st.dataframe(st.session_state.books)

with tab2:
    st.header("👥 Data Anggota")
    with st.form("add_member"):
        nama = st.text_input("Nama")
        alamat = st.text_input("Kelas / Alamat")
        submit_member = st.form_submit_button("Tambah Anggota")
        if submit_member:
            new_member = {"ID": len(st.session_state.members)+1, "Nama": nama, "Kelas/Alamat": alamat}
            st.session_state.members = pd.concat([st.session_state.members, pd.DataFrame([new_member])], ignore_index=True)
            st.success("✅ Anggota berhasil ditambahkan.")

    st.dataframe(st.session_state.members)

with tab3:
    st.header("🔁 Peminjaman / Pengembalian")
    nama = st.selectbox("Pilih Nama", st.session_state.members["Nama"] if not st.session_state.members.empty else [])
    buku = st.selectbox("Pilih Buku", st.session_state.books["Judul"] if not st.session_state.books.empty else [])
    tanggal_pinjam = st.date_input("Tanggal Pinjam", datetime.today())
    tanggal_kembali = st.date_input("Tanggal Kembali", datetime.today())
    status = st.selectbox("Status", ["Dipinjam", "Dikembalikan"])
    if st.button("Simpan Transaksi"):
        transaksi = {
            "Nama": nama,
            "Judul Buku": buku,
            "Tanggal Pinjam": tanggal_pinjam,
            "Tanggal Kembali": tanggal_kembali,
            "Status": status
        }
        st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([transaksi])], ignore_index=True)
        st.success("✅ Transaksi disimpan!")

with tab4:
    st.header("📊 Riwayat Peminjaman")
    st.dataframe(st.session_state.transactions)

    if st.download_button("📥 Download CSV", st.session_state.transactions.to_csv(index=False), file_name="riwayat_peminjaman.csv"):
        st.success("File CSV berhasil diunduh.")
