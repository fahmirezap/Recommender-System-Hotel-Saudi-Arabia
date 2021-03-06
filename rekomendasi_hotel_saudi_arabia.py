# -*- coding: utf-8 -*-
"""Rekomendasi Hotel Saudi Arabia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sXjh1oTc1Aj1jrVmRtceBYk96Mm1NZot
"""

#Import Library
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import re
#Read Dataset CSV
df = pd.read_csv("Hotel Saudi Arabia.csv")
df.head()

#Analisa Dataset
df.describe()
df.info()

#Fungsi Untuk Menampilkan Deskripsi hotel, Nama, Alamat
def print_description(index):
    example = df[df.index == index][['description', 'hotel_name', 'city']].values[0]
    if len(example) > 0:
        print(example[0])
        print('Nama:', example[1])
        print('Kota:', example[2])

#Cek
print_description(1)

#Cek
print_description(50)

#Preprocessing
import nltk
nltk.download('stopwords')
clean_spcl = re.compile('[/(){}\[\]\|@,;]')
clean_symbol = re.compile('[^0-9a-z #+_]')
stopworda = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower() # mengubah jadi huruf kecil
    text = clean_spcl.sub(' ', text)
    text = clean_symbol.sub('', text)
    text = ' '.join(word for word in text.split() if word not in stopworda) # hapus stopword dari kolom deskripsi
    return text

# Buat kolom tambahan untuk data description yang telah dibersihkan   
df['desc_clean'] = df['description'].apply(clean_text)

# Fungsi Deskripsi kedua (Setelah preprocessing)
def print_description_clean(index):
    example = df[df.index == index][['desc_clean', 'hotel_name', 'city']].values[0]
    if len(example) > 0:
        print(example[0])
        print('Nama:', example[1])
        print('Kota:', example[2])

#Menggunakan TF-IDF dan Cosine Similarity Untuk Mengubah Data menjadi angka matriks
df.set_index('hotel_name', inplace=True)
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['desc_clean'])
cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
cos_sim

# Set index utama di kolom 'name' untuk melakukan rekomendasi hotel
indices = pd.Series(df.index)
indices[:50]

#Modelling Untuk 10 Data Hasil Rekomendasi
def recommendations(name, cos_sim = cos_sim):
    
    recommended_hotel = []
    
    # Mengambil nama hotel berdasarkan variabel indicies
    idx = indices[indices == name].index[0]

    # Membuat series berdasarkan skor kesamaan
    score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

    # mengambil index dan dibuat 10 baris rekomendasi terbaik
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    for i in top_10_indexes:
        recommended_hotel.append(list(df.index)[i])
        
    return recommended_hotel

#Modelling Untuk 5 Data Hasil Rekomendasi
def recommendations1(name, cos_sim = cos_sim):
    
    recommended_hotel1 = []
    
    # Mengambil nama hotel berdasarkan variabel indicies
    idx = indices[indices == name].index[0]

    # Membuat series berdasarkan skor kesamaan
    score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

    # mengambil index dan dibuat 5 baris rekomendasi terbaik
    top_5_indexes = list(score_series.iloc[1:6].index)
    
    for i in top_5_indexes:
        recommended_hotel1.append(list(df.index)[i])
        
    return recommended_hotel1

#Modelling Untuk 3 Data Hasil Rekomendasi
def recommendations2(name, cos_sim = cos_sim):
    
    recommended_hotel1 = []
    
    # Mengambil nama hotel berdasarkan variabel indicies
    idx = indices[indices == name].index[0]

    # Membuat series berdasarkan skor kesamaan
    score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

    # mengambil index dan dibuat 5 baris rekomendasi terbaik
    top_3_indexes = list(score_series.iloc[1:4].index)
    
    for i in top_3_indexes:
        recommended_hotel1.append(list(df.index)[i])
        
    return recommended_hotel1

#Cek rekomendasi dengan hasil 10 hotel
recommendations('Hilton Riyadh Hotel & Residences')

#Cek rekomendasi dengan hasil 5 hotel
recommendations1('Hilton Riyadh Hotel & Residences')

#Cek rekomendasi dengan hasil 3 hotel
recommendations2('Hilton Riyadh Hotel & Residences')