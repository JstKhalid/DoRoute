import mysql.connector # pip install mysql-connector-python
from heapq import merge
from mysql.connector import Error
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json


connection = mysql.connector.connect(host='localhost',
                                         database='bobt',
                                         user='root',
                                         password='')

query = "SELECT * FROM hitung_bobot"

cursor = connection.cursor()
cursor.execute(query)
record = cursor.fetchall()
w1,w2,w3,w4 = (1,1,1,1)

asal = ""
nested = {}
map = {}
print("Total Lane : ",len(record))
dblen = len(record)
i=0

for row in record:
   id_rute = row[0]
   asaldb = row[1]
   tujuan = row[2]
   harga = row[3]
   distance = row[4]
   rating = row[5]
   durasi = row[6]
   agensi = row[7]
   
   rumus = (harga*1/w1) + (distance*1/w2) + (-rating*1/w3) + (durasi*1/w4)
   
   i=i+1
   if asaldb == asal:
    newnested = {tujuan : rumus}
    nested.update(newnested)
    # print(nested)
    # print("sama")
   elif asal == "":
    newnested = {tujuan : rumus}
    nested.update(newnested)
    # print(nested)
    asal = asaldb
    # print("kosong")
   else: 

    # print("beda")
    mapnew = {asal:nested}
    map.update(mapnew)
    
    nested = {}
    newnested = {tujuan : rumus}
    nested.update(newnested)
    # print(nested)
    asal = asaldb
   
   if i == dblen:
    mapnew = {asal:nested}
    map.update(mapnew)


   


for r in record:
    print(r)
print(map)
# print(map['jakarta'])
# print(map['surabaya'])
# print(map['bogor'])
# print(asaldb)
 
 



   
