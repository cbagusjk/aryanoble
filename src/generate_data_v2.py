import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_erha_problematic_data():
    # --- 1. Setup Data Master ---
    
    branches = [
        {'code': 'CH001', 'name': 'Erha Derma Center Kemanggisan', 'city': 'Jakarta Barat'},
        {'code': 'CH002', 'name': 'Erha Apothecary PIK', 'city': 'Jakarta Utara'},
        {'code': 'CH003', 'name': 'Erha Clinic Bandung', 'city': 'Bandung'},
        {'code': 'CH004', 'name': 'Erha Clinic Surabaya', 'city': 'Surabaya'},
        {'code': 'CH005', 'name': 'Erha Apothecary Senayan City', 'city': 'Jakarta Pusat'},
    ]

    # Produk: Ada Treatment (High Value) & Product (Low Value)
    products = [
        {'code': 'TRT001', 'name': 'Acne Peeling', 'type': 'Treatment', 'price': 450000},
        {'code': 'TRT002', 'name': 'Laser Rejuvenation', 'type': 'Treatment', 'price': 1500000}, # High Value
        {'code': 'TRT003', 'name': 'Hair Growth Therapy', 'type': 'Treatment', 'price': 750000},
        {'code': 'PRD001', 'name': 'Acne Sunblock SPF30', 'type': 'Product', 'price': 120000},
        {'code': 'PRD002', 'name': 'Brightening Night Cream', 'type': 'Product', 'price': 185000},
        {'code': 'PRD003', 'name': 'Collagen Supplement', 'type': 'Product', 'price': 300000},
    ]

    doctors = [
        {'id': 'DR001', 'name': 'dr. Amanda Sp.KK', 'job': 'Doctor'}, # Top Performer
        {'id': 'DR002', 'name': 'dr. Budi Santoso', 'job': 'Doctor'},
        {'id': 'DR003', 'name': 'dr. Citra Lestari', 'job': 'Doctor'},
        {'id': 'NS001', 'name': 'Ns. Diana', 'job': 'Nurse'},
        {'id': 'NS002', 'name': 'Ns. Eko', 'job': 'Nurse'},
    ]

    payments = ['Cash', 'Credit Card BCA', 'Debit Mandiri', 'GoPay', 'OVO', 'Admedika']

    data = []
    
    # --- 2. Simulasi Harian (Jan - Des 2023) ---
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = timedelta(days=1)
    
    curr_date = start_date

    while curr_date <= end_date:
        month = curr_date.month
        
        # --- SKENARIO 1: Penurunan Global di Q4 (Okt-Des) ---
        if month >= 10: 
            # Volume transaksi harian rendah (10-15 trx/hari)
            daily_trx_volume = random.randint(10, 15)
        else:
            # Volume transaksi harian normal/tinggi (20-35 trx/hari)
            daily_trx_volume = random.randint(20, 35)
            
        # Generate transaksi untuk hari ini
        for _ in range(daily_trx_volume):
            
            # Pilih Cabang
            branch = random.choice(branches)
            
            # --- SKENARIO 2: Masalah Produk High Value ---
            # Mulai November, Laser Rejuvenation jarang dibeli (mungkin alat rusak?)
            current_products = products.copy()
            if month >= 11 and random.random() > 0.1: 
                # Hapus Laser dari list opsi, sisakan peluang kecil 10%
                current_products = [p for p in current_products if p['code'] != 'TRT002']
            
            prod = random.choice(current_products)
            
            # --- SKENARIO 3: Masalah Dokter di Kemanggisan ---
            # dr. Amanda (DR001) resign/cuti panjang dari Cabang Kemanggisan (CH001) mulai September
            current_doctors = doctors.copy()
            if branch['code'] == 'CH001' and month >= 9:
                 current_doctors = [d for d in current_doctors if d['id'] != 'DR001']
            
            # Logika pemilihan dokter vs nurse
            if prod['type'] == 'Treatment' and prod['price'] > 500000:
                # Treatment mahal harus dokter
                valid_docs = [d for d in current_doctors if d['job'] == 'Doctor']
                if not valid_docs: valid_docs = current_doctors # fallback
                doc = random.choice(valid_docs)
            else:
                doc = random.choice(current_doctors)

            # Generate Field Lainnya
            qty = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            sales = prod['price'] * qty
            
            # Customer Data
            cust_id = f"CUST{random.randint(1000, 3000)}" # Pool customer lebih kecil supaya ada repeat order
            is_new = random.random() < 0.2 # 20% customer baru hari ini
            if is_new:
                reg_date = curr_date
            else:
                reg_date = curr_date - timedelta(days=random.randint(30, 800))

            row = {
                'TransactionDate': curr_date.date(),
                'ChannelCode': branch['code'],
                'ChannelStoreName': branch['name'],
                'City': branch['city'],
                'CustomerID': cust_id,
                'Gender': random.choices(['F', 'M'], weights=[85, 15])[0],
                'Age': int(np.random.normal(32, 7)),
                'TglReg': reg_date.date(),
                'ProductCode': prod['code'],
                'ProductName': prod['name'],
                'TotalSales': sales,
                'PaymentMethodType': 'Cashless' if random.random() > 0.3 else 'Cash',
                'PaymentMethodName': random.choice(payments),
                'DoctorID': doc['id'],
                'DoctorName': doc['name'],
                'MedicalJobdesk': doc['job']
            }
            data.append(row)
        
        curr_date += delta

    # --- 3. Finalisasi DataFrame ---
    df = pd.DataFrame(data)
    return df

# Generate Data
df_case = generate_erha_problematic_data()

# Validasi Singkat (Untuk Anda mengecek pola)
print(f"Total Data: {len(df_case)} rows")
print("\n1. Cek Rata-rata Sales per Bulan (Harusnya drop di Okt-Des):")
df_case['Month'] = pd.to_datetime(df_case['TransactionDate']).dt.to_period('M')
print(df_case.groupby('Month')['TotalSales'].sum())

# Simpan
df_case.to_csv('../data/erha_sales_case_study.csv', index=False)