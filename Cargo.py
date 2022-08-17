import mysql.connector # pip install mysql-connector-python
from heapq import merge
from mysql.connector import Error
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def shortest(maps, asal, tujuan): # mencari jalur terpendek dari maps (graph yg dibangun)
    result = [] # node dengan jarak terpendek simpan ke dalam list
    result.append(asal) # inisialisasi node pertama dengan nilai asal

    while tujuan not in result: # telusuri graph sampai tujuan ditemukan
        current_node = result[-1] # -1 == list di index terakhir
        print ("Node Terakhir :",current_node)
        jarak_terpendek = min(maps[current_node].values()) # Cari local maximum (nilai/jarak terkecil dari node terakhir ke node selanjutnya)
#        print ("Node Dengan Jarak Terpendek Dari Node Terakhir :|", jarak_terpendek)
       
        for node, jarak in maps[current_node].items(): # iterasi mencari node selanjutnya
            print ("Node Selanjutnya :",node,"| Jarak :",jarak)
            if jarak == jarak_terpendek:
                 # ambil node dengan jarak terpendek dan tambahkan ke list result
                 # agar iterasi selanjutnya dimulai dari node sekarang.
                result.append(node)

    return result




connection = mysql.connector.connect(host='localhost',
                                         database='bobt',
                                         user='root',
                                         password='')

cursor = connection.cursor(dictionary=True)
sql = "SELECT * FROM hitung_bobot"
cursor.execute(sql)
rows = cursor.fetchall()

w1,w2,w3,w4 = (1,1,1,1)

maps = {}

for row in rows:
   asal= row['asal']
   tujuan= row['tujuan']
   id_rute = row['id_rute']
   harga = row['harga']
   distance = row['jarak']
   rating = row['rating']
   durasi = row['durasi']
   agensi = row['agensi']
   
   rumus = (harga*1/w1) + (distance*1/w2) + (-rating*1/w3) + (durasi*1/w4)

   maps_final= {
      asal:{tujuan : rumus}
   }

   maps.update(maps_final)

print(maps)


# query = "SELECT * FROM hitung_bobot"

# cursor = connection.cursor()
# cursor.execute(query)
# record = cursor.fetchall()

# print("Total Lane : ",len(record))


""" for row in record:
   id_rute = row[0]
   asal = row[1]
   tujuan = row[2]
   harga = row[3]
   distance = row[4]
   rating = row[5]
   durasi = row[6]
   agensi = row[7]
   

   rumus = (harga*1/w1) + (distance*1/w2) + (-rating*1/w3) + (durasi*1/w4)

   maps_final = {
      asal:{tujuan : rumus}
   }

   print(maps_final) """

   