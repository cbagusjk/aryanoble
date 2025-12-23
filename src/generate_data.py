import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_erha_dummy_data(num_rows=5000):
    # --- 1. Setup Data Master (Lookup Tables) ---
    
    # Lokasi Cabang (Channel)
    branches = [
        {'code': 'CH001', 'name': 'Erha Derma Center Kemanggisan', 'city': 'Jakarta Barat'},
        {'code': 'CH002', 'name': 'Erha Apothecary PIK', 'city': 'Jakarta Utara'},
        {'code': 'CH003', 'name': 'Erha Clinic Bandung', 'city': 'Bandung'},
        {'code': 'CH004', 'name': 'Erha Clinic Surabaya', 'city': 'Surabaya'},
        {'code': 'CH005', 'name': 'Erha Apothecary Senayan City', 'city': 'Jakarta Pusat'},
    ]

    # Produk & Treatment (Beserta kisaran harga)
    products = [
        {'code': 'TRT001', 'name': 'Acne Peeling', 'type': 'Treatment', 'base_price': 450000},
        {'code': 'TRT002', 'name': 'Laser Rejuvenation', 'type': 'Treatment', 'base_price': 1500000},
        {'code': 'TRT003', 'name': 'Hair Growth Therapy', 'type': 'Treatment', 'base_price': 750000},
        {'code': 'PRD001', 'name': 'Acne Sunblock SPF30', 'type': 'Product', 'base_price': 120000},
        {'code': 'PRD002', 'name': 'Brightening Night Cream', 'type': 'Product', 'base_price': 185000},
        {'code': 'PRD003', 'name': 'Collagen Supplement', 'type': 'Product', 'base_price': 300000},
    ]

    # Tenaga Medis
    doctors = [
        {'id': 'DR001', 'name': 'dr. Amanda Sp.KK', 'job': 'Doctor'},
        {'id': 'DR002', 'name': 'dr. Budi Santoso', 'job': 'Doctor'},
        {'id': 'DR003', 'name': 'dr. Citra Lestari', 'job': 'Doctor'},
        {'id': 'NS001', 'name': 'Ns. Diana', 'job': 'Nurse'}, # Nurse untuk treatment ringan
        {'id': 'NS002', 'name': 'Ns. Eko', 'job': 'Nurse'},
    ]

    # Metode Pembayaran
    payments = [
        {'type': 'Cash', 'name': 'Cash'},
        {'type': 'Card', 'name': 'Credit Card BCA'},
        {'type': 'Card', 'name': 'Debit Mandiri'},
        {'type': 'E-Wallet', 'name': 'GoPay'},
        {'type': 'E-Wallet', 'name': 'OVO'},
        {'type': 'Insurance', 'name': 'Admedika'},
    ]

    # --- 2. Fungsi Helper ---

    def random_date(start_date, end_date):
        delta = end_date - start_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start_date + timedelta(seconds=random_second)

    # --- 3. Generate Data Rows ---
    
    data = []
    
    # Periode Transaksi: 1 Tahun (Jan 2023 - Des 2023)
    start_period = datetime(2023, 1, 1)
    end_period = datetime(2023, 12, 31)

    for _ in range(num_rows):
        # Pilih Cabang
        branch = random.choice(branches)
        
        # Pilih Produk
        prod = random.choice(products)
        
        # Tentukan Sales (Harga base + variasi sedikit/random quantity 1-2)
        qty = random.choice([1, 1, 1, 2]) # Lebih sering beli 1
        sales = prod['base_price'] * qty
        
        # Pilih Dokter/Medis
        # Logika: Jika treatment mahal, biasanya dokter. Jika produk, bisa siapa saja/random.
        if prod['type'] == 'Treatment' and prod['base_price'] > 500000:
            doc = random.choice([d for d in doctors if d['job'] == 'Doctor'])
        else:
            doc = random.choice(doctors)
            
        # Pilih Metode Bayar
        pay = random.choice(payments)
        
        # Generate Data Customer
        cust_id = f"CUST{random.randint(1000, 9999)}"
        gender = random.choice(['F', 'F', 'F', 'M']) # Skincare biasanya dominan Female
        age = int(np.random.normal(30, 8)) # Rata-rata umur 30, std dev 8
        age = max(15, min(70, age)) # Limit umur 15-70
        
        # Tanggal Transaksi
        trx_date = random_date(start_period, end_period)
        
        # Tanggal Registrasi (TglReg)
        # 30% User Baru (TglReg dekat dengan TrxDate), 70% User Lama
        is_new_user = random.random() < 0.3
        if is_new_user:
            reg_date = trx_date - timedelta(days=random.randint(0, 30))
        else:
            reg_date = trx_date - timedelta(days=random.randint(60, 1000))
            
        row = {
            'TransactionDate': trx_date.date(), # Kolom Tambahan Krusial
            'ChannelCode': branch['code'],
            'ChannelStoreName': branch['name'],
            'CustomerID': cust_id,
            'Gender': gender,
            'Age': age,
            'City': branch['city'], # Asumsi customer tinggal di kota sama dengan klinik
            'TglReg': reg_date.date(),
            'ProductCode': prod['code'],
            'ProductName': prod['name'],
            'TotalSales': sales,
            'PaymentMethodType': pay['type'],
            'PaymentMethodName': pay['name'],
            'DoctorID': doc['id'],
            'DoctorName': doc['name'],
            'MedicalJobdesk': doc['job']
        }
        data.append(row)

    # --- 4. Create DataFrame ---
    df = pd.DataFrame(data)
    
    # Sorting berdasarkan tanggal transaksi agar rapi
    df = df.sort_values(by='TransactionDate').reset_index(drop=True)
    
    return df

# Generate Data
df_dummy = generate_erha_dummy_data(5000)

# Preview Data
print("Info Dataset:")
print(df_dummy.info())
print("\nContoh 5 Data Teratas:")
print(df_dummy.head())

# Opsional: Simpan ke CSV
df_dummy.to_csv('dummy_erha_sales.csv', index=False)