import requests
import pandas as pd
import numpy as np
import math
import json
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, jsonify, request

app = Flask(__name__)

df_city = pd.read_excel('venv//master_data//cities.xlsx', index_col=0)
df_airport = pd.read_excel('venv//master_data//airport.xlsx', index_col=0)
df_ground_cargo = pd.read_excel('venv//master_data//clean_ground_cargo.xlsx', index_col=0) 
df_air_cargo = pd.read_excel('venv//master_data//air_cargo.xlsx', index_col=0) 

def dijkstra(asal,tujuan,graph):
    openList = {}
    closeList = []
    parent = {}
    labels = 'No Path Found'
    openList[asal]=0
    INF = 999999
    #pembuatan openlist
    for node in graph.keys():
        for cNode in graph [node].keys():
            openList[cNode]=INF
            parent[cNode]=''
        openList[asal]=0
    print(openList)
    
    #Greedy process
    while openList != {}:
        if asal not in graph:
            closeList = labels
            break
        bestNode = min(openList,key=openList.get)
        print("Bestnode :",bestNode)
        closeList.append(bestNode)
        if bestNode == tujuan:
            break
        if bestNode in graph:
            suksesor = graph[bestNode]
            for node,value in suksesor.items():
                if node in openList:
                    #relaksasi cost
                    tempG = openList[bestNode]+graph[bestNode][node]
                    if tempG < openList[node]:
                        openList[node]=tempG
                        parent[node]=bestNode
        print(openList)
        del openList[bestNode]
    if openList == {}:
        closeList = labels
        
    
    hasilSearch = closeList,parent
    return hasilSearch
def reconstruction_path(asal,tujuan,graph,closeList,parent,bestNode):
    print("PARENT :",parent)
    jalur = [] #sesuaikan parameter kedua ekstrakJalur dengan nama ini
    bobotJalur = 0 #sesuaikan parameter ketiga ekstrakJalur dengan nama var ini
    hasil = closeList
    if hasil != 'No Path Found':
        while bestNode != asal:
            jalur.append(bestNode)
            print(graph[parent[bestNode]][bestNode],":",graph[parent[bestNode]][bestNode])
            bobotJalur += graph[parent[bestNode]][bestNode]
            bestNode = parent[bestNode]
        jalur.append(asal)
        jalur.reverse()
        hasil = jalur,bobotJalur
    return hasil

#Create Route + build machine learning
@app.route('/findRoute', methods=['GET','POST'])
def findRoute():
    #normalisasi Rute Darat
    data = df_ground_cargo[df_ground_cargo.columns[4:8]]
    scaler = MinMaxScaler(feature_range=(5, 10))
    scaler.fit(data)
    normed = scaler.transform(data)
    df_ground_cargo[df_ground_cargo.columns[4:8]] = normed
    df_ground_cargo
    
    #normalisasi Rute Udara
    data = df_air_cargo[df_air_cargo.columns[4:8]]
    scaler = MinMaxScaler(feature_range=(5, 10))
    scaler.fit(data)
    normed = scaler.transform(data)
    df_air_cargo[df_air_cargo.columns[4:8]] = normed
    df_air_cargo
     
    #Graph Darat
    ground_graph = {}
    w1,w2,w3,w4 = (1,1,1,1)
    for row in df_ground_cargo.values:
        ground_origin = row[0]
        ground_destination = row[2]
        ground_distance = int(row[4])
        ground_price = int(row[5])
        ground_duration = int(row[6])
        ground_rate = int(row[7])
        
        if ground_destination in df_airport['airport_city_id'].values:
            cost = ((ground_distance*1/w1) + (ground_price*1/w2) + (ground_duration*1/w3) + (-ground_rate*1/w4))/2
        else:
            cost = (ground_distance*1/w1) + (ground_price*1/w2) + (ground_duration*1/w3) + (-ground_rate*1/w4)
        
        if ground_origin in ground_graph:
            ground_graph[ground_origin][ground_destination] = cost
        else:
            ground_graph[ground_origin]={}
            ground_graph[ground_origin][ground_destination] = cost
    ground_graph
    
    #Graph Udara
    air_graph = {}
    w1,w2,w3,w4 = (1,1,1,1)
    for row in df_air_cargo.values:
        air_origin = row[0]
        air_destination = row[2]
        air_distance = int(row[4])
        air_price = int(row[5])
        air_duration = int(row[6])
        air_rate = int(row[7])
        
        cost = (air_distance*1/w1) + (air_price*1/w2) + (air_duration*1/w3) + (-air_rate*1/w4)
        
        if air_origin in air_graph:
            air_graph[air_origin][air_destination] = cost
        else:
            air_graph[air_origin]={}
            air_graph[air_origin][air_destination] = cost

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
     origin = request.get_json()['org']

     destination = request.get_json()['des']
     print(origin,'-',destination)

     prov_origin = int(df_city.loc[df_city['city_id']==origin]['province_id'])
     prov_destination = int(df_city.loc[df_city['city_id']==destination]['province_id'])
     if prov_origin == prov_destination:
         result = dijkstra(21,10,air_graph)
     else:
         airport_origin = int(df_airport.loc[df_airport['province_id']==prov_origin]['airport_city_id'])
         airport_destination = int(df_airport.loc[df_airport['province_id']==prov_destination]['airport_city_id'])
         print(airport_origin,"-",airport_destination)
         
         list_result = []
         #langkah 1 asal ke airport asal
         result = dijkstra(origin,airport_origin,ground_graph)
         print(result)
         list_result.append(reconstruction_path(origin,
                                             airport_origin,
                                             ground_graph,
                                             (result[0]),
                                             (result[1]),
                                             (result[0][-1])))
         print('langkah 1 :',list_result)
     #     if 'No Path Found' not in list_result:
         #langkah 2 airport asal ke airport tujuan
         result = dijkstra(airport_origin,airport_destination,air_graph)
         print(result)
         list_result.append(reconstruction_path(airport_origin,
                                             airport_destination,
                                             air_graph,
                                             (result[0]),
                                             (result[1]),
                                             (result[0][-1])))

         print('langkah 2 :',list_result)

             
     #     if 'No Path Found' not in list_result:
         #langkah 3 airport tujuan ke tujuan
         result = dijkstra(airport_destination,destination,ground_graph)
         list_result.append(reconstruction_path(airport_destination,
                                             destination,
                                             ground_graph,
                                             (result[0]),
                                             (result[1]),
                                             (result[0][-1])))

         print('langkah 3 :',list_result)
         
         #rekonstruksi Full
         full_path = []
         nilai = 0
         if 'No Path Found' not in list_result:
             for row in list_result:
                 nilai += row[1]
                 for x in row[0]:
                     node = F"{df_city.loc[df_city['city_id']==x]['type'].values[0]} {df_city.loc[df_city['city_id']==x]['city_name'].values[0]}"
                     full_path.append(node)
             print("Path :",full_path,"Cost :",nilai)
         else:
             full_path = 'No Path Found'
             print("Path :",full_path,"Cost :",nilai)
         
         response = {
             'status':{
                 "responseCode": "200",
                 "responseDesc": "Success",
                 "responseMessage": "Sucsess operating algorithm"
             },
             'result':{
                 'fullPath':full_path,
                 'cost':nilai
             }
         }
         return jsonify(response)
    else:
     response = {
             'status':{
                 "responseCode": "400",
                 "responseDesc": "failed",
                 "responseMessage": "No Input"
             }
         }
     return jsonify(response)

# driver function
if __name__ == '__main__':
    #website_url = '10.251.251.169:8080'
    website_url = 'localhost:8080'
    app.config['SERVER_NAME'] = website_url
    app.run()   