from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import numpy as np
import mysql.connector as sql
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import math

# creating a Flask app
app = Flask(__name__)

#Create Route + build machine learning
@app.route('/findRoute', methods=['GET','POST'])
def findRoute():

    #Database Connection
    connection = mysql.connector.connect(host='localhost',
                                            database='mapscargo', # masukan nama database di kiri
                                            user='root',
                                            password='')

    querryRoute = "SELECT sample.sample_id AS 'ID', origin AS'ORIGIN ID', destination AS 'DESTINATION ID', a.city_name AS 'ORIGIN', b.city_name AS 'DESTINATION', sample.distance AS 'DISTANCE', sample.price AS 'PRICE', sample.rate AS 'RATE', sample.duration AS 'DURATION' FROM sample JOIN city a ON sample.origin = a.city_id JOIN city b ON sample.destination = b.city_id;"
    querryNodes = "SELECT city_id AS 'NODE ID', city_name AS 'NODE', lat, city.long FROM city"

    routeCursor = connection.cursor()
    routeCursor.execute(querryRoute)
    routeResult = routeCursor.fetchall()

    nodesCursor = connection.cursor()
    nodesCursor.execute(querryNodes)
    nodesResult = nodesCursor.fetchall()

    print(nodesResult)
    route = pd.DataFrame(routeResult,columns=['ID','ORIGIN ID','DESTINATION ID','ORIGIN','DESTINATION','DISTANCE','PRICE','RATE','DURATION'])
    nodes = pd.DataFrame(nodesResult,columns=['NODE ID','NODE','lat','long'])

    def routeNormalization(route,minParam):
        paramRoute = pd.concat([route,minParam]).reset_index(drop=True)
        data = paramRoute[paramRoute.columns[5:9]]
        scaler = MinMaxScaler(feature_range=(5, 10))
        scaler.fit(data)
        normedData =scaler.transform(data)
        route[route.columns[5:9]] = normedData[:len(route)]

    def createGraph(route):
        graph = {}
        w1,w2,w3,w4 = (1,1,1,1)
        for row in route.values:
            origin_db = row[3]
            destination_db = row[4]
            distance_db = row[5]
            price_db = row[6]
            rate_db = row[7]
            duration_db = row[8]

            W = (distance_db*1/w1) + (price_db*1/w2) + (-rate_db*1/w3) + (duration_db*1/w4)

            if origin_db in graph:
                graph[origin_db][destination_db] = W
            else:
                graph[origin_db]={}
                graph[origin_db][destination_db] = W
        return graph
    
    def heuristicValues(nodes,destination: str):
        nodes["eDistance"] = np.nan
        p = nodes.loc[nodes.NODE == destination,'lat'].values
        q = nodes.loc[nodes.NODE == destination,'long'].values
        for node,lat,long in nodes[nodes.columns[1:4]].values:
            if node == destination:
                nodes.loc[nodes.NODE == destination,'eDistance'] = 0.0
            else:
                eDistance = math.sqrt((p-lat)**2+(q-long)**2)
                nodes.loc[nodes.NODE == node,'eDistance'] = eDistance*110.574

    def heuristicNormalization(nodes,maxParam):
        paramNode = pd.concat([nodes,maxParam]).reset_index(drop=True)
        data = paramNode[paramNode.columns[2:5]]
        scaler = MinMaxScaler(feature_range=(5, 10))
        scaler.fit(data)
        normed=scaler.transform(data)
        paramNode[paramNode.columns[2:5]]=normed
        nodes[nodes.columns[4]] = paramNode[paramNode.columns[4]].iloc[:len(nodes)]
    
    def heursiticGraph(nodes):
        hDict={}
        w1 = 1
        for row in nodes.values:
            node = row[1]
            e_distance = row[4]

            h_value = (e_distance*1/w1)
            hDict[node]=h_value
        return hDict

    def greedy(origin: str,destination: str,graph):
        openList = {}
        closeList = []
        parent = {}
        labels = 'No Path Found'
        openList[origin]=0
        while destination not in closeList:
            bestNode = min(openList,key=openList.get)
            print("Bestnode :",bestNode)
            closeList.append(bestNode)
            if bestNode not in graph:
                closeList = labels
                break
            successor = graph[bestNode]
            for node,value in successor.items():
                if node not in closeList:
                    if node in openList:
                        if value<openList[node]:
                            openList[node]=value
                            parent[node]=bestNode
                    elif node not in openList:
                        openList[node]=value
                        parent[node]=bestNode
            print(openList)
            del openList[bestNode]
            if destination in openList:
                bestNode = destination
                closeList.append(destination)
                break
        searchResult = closeList,parent
        return searchResult

    def bestfirstSearch(origin: str,destination: str,graph):
        openList = {}
        closeList = []
        parent = {}
        labels = 'No Path Found'
        openList[origin]=0

        while openList != {}:
            if openList == {}:
                closeList = labels
            bestNode = min(openList,key=openList.get)
            print("Bestnode :",bestNode)
            closeList.append(bestNode)
            del openList[bestNode]
            if bestNode == destination:
                break
            if bestNode in graph:
                successor = graph[bestNode]
                for node,value in successor.items():
                    if node not in closeList:
                        if node in openList:
                            if value<openList[node]:
                                openList[node]=value
                                parent[node]=bestNode
                        elif node not in openList:
                            openList[node]=value
                            parent[node]=bestNode         
                print(openList)
        searchResult = closeList,parent
        return searchResult

    def dijkstra(origin: str,destination: str,graph):
        openList = {}
        closeList = []
        parent = {}
        labels = 'No Path Found'
        openList[origin]=0
        INF = 999999

        for node in graph.keys():
            for cNode in graph [node].keys():
                openList[cNode]=INF
                parent[cNode]=''
            openList[origin]=0
        print(openList)
        while openList != {}:
            if openList == {}:
                closeList = labels
                break
            bestNode = min(openList,key=openList.get)
            print("Bestnode :",bestNode)
            closeList.append(bestNode)
            if bestNode == destination:
                break
            if bestNode in graph:
                successor = graph[bestNode]
                for node,value in successor.items():
                    if node in openList:
                        tempG = openList[bestNode]+graph[bestNode][node]
                        if tempG < openList[node]:
                            openList[node]=tempG
                            parent[node]=bestNode
            print(openList)
            del openList[bestNode]
        searchResult = closeList,parent
        return searchResult
    
    def aStar(origin: str,destination: str,graph,hList):
        gList = {}
        openList = {}
        closeList = []
        parent = {}
        labels = 'No Path Found'
        openList[origin]=0

        pathList = {}
        closeListB = []
        parentB = {}
        gList[origin] = 0
        while openList !={}:
            print("OPEN LIST :",openList)
            bestNode = min(openList,key=openList.get)
            print("Bestnode :",bestNode)
            closeList.append(bestNode)
            if bestNode in graph:
                successor = graph[bestNode]
                for node,value in successor.items():
                    g = gList[bestNode] + graph[bestNode][node] #(g) baru  
                    if node == destination:
                        print("Path Found")
                        closeListB = closeList
                        parentB = parent
                        bestNodeB = destination
                        parentB[bestNodeB]=bestNode

                        fPath = 0
                        path = []
                        while bestNodeB != origin:
                            print(bestNodeB)
                            print(parentB)
                            path.append(bestNodeB)
                            fPath += graph[(parentB[bestNodeB])][bestNodeB] 
                            bestNodeB = parent[bestNodeB]
                        path.append(origin)
                        path.reverse()
                        print(path)
                        pathList[fPath]=path

                    if node in openList:
                        oldParent = parent[node]
                        oldG =  gList[node]
                        if oldG > g:
                            gList[node]=g
                            openList[node]=g+hList[node]
                            parent[node]=bestNode
                    elif node in closeList:
                        oldParent = parent[node]
                        oldG =  gList[node]
                        if oldG > g:
                            newF = g + hList[node]
                            parent[node]=bestNode
                            closeList[node]=newF
                            if node in graph:
                                nodeSuccessor = graph[node]
                                for GC in nodeSuccessor.keys: #grandChild
                                    gGC = g+nodeSuccessor[node]
                                    if GC in openList:
                                        gList = g+nodeSuccessor[node]
                                        openList[GC]=g+nodeSuccessor[node]+hList[GC]
                                        parent[GC]=node
                                    elif GC in nodeSuccessor:
                                        if gGC < g:
                                            gList = g+nodeSuccessor[node]
                                            openList[GC]=gGC+hList[GC]
                                            parent[GC]=node
                    else:
                        gList[node]=g
                        openList[node]=g+hList[node]
                        parent[node]=bestNode
            del openList[bestNode]
        print("Detected Routes :",pathList)
        searchResult = (pathList[min(pathList.keys())]),(min(pathList.keys()))
        return searchResult

    def FloydWarshall(origin: str,destination: str,route,nodes):
        u = int(nodes.loc[nodes['NODE'] == origin]['NODE ID']-1)
        v = int(nodes.loc[nodes['NODE'] == destination]['NODE ID']-1)
        nV = len(nodes[nodes.columns[0]])
        matrix = []
        parent = []
        for k in range (nV):
            row = []
            rowParent = []
            for i in range (nV):
                row.append(999)
                rowParent.append(-1)
                if i == k:
                    row[i] = 0
                    rowParent[i] = k

            matrix.append(row)
            parent.append(rowParent)
        print(graph)
        w1,w2,w3,w4 = (1,1,1,1)
        for row in route.values:
            origin_db = row[1]
            destination_db = row[2]
            distance_db = row[5]
            price_db = row[6]
            rate_db = row[7]
            duration_db = row[8]
            W = (distance_db*1/w1) + (price_db*1/w2) + (-rate_db*1/w3) + (duration_db*1/w4)
            matrix[origin_db-1][destination_db-1]=W
            parent[origin_db-1][destination_db-1]=destination_db-1
            
        for k in range (nV):
            for i in range (nV):
                for j in range (nV):
                    if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]
                        parent[i][j] = parent[i][k]

        if parent[u][v]==-1:
            result = "No Path"
            return result
        else:
            result = [u]
        
            while u != v:
                
                u = parent[u][v]
                result.append(u)

        path = []
        for nodeId in result:
            node = nodes.loc[nodes['NODE ID'] == (nodeId+1)]['NODE'].values[0]
            path.append(node)
        pathG = 0
        for row in range(len(path)):
            if row != 0:
                parent = row -1
                pathG += (graph[path[parent]][path[row]])
        searchResult = (path,pathG)
        return searchResult

    def pathReconstruction(closeList,parent,bestNode: str,origin: str):
        print("PARENT :",parent)
        path = [] #sesuaikan parameter kedua ekstrakJalur dengan nama ini
        pathG = 0 #sesuaikan parameter ketiga ekstrakJalur dengan nama var ini
        result = closeList
        if result != 'No Path Found':
            while bestNode != origin:
                path.append(bestNode)
                print(graph[parent[bestNode]][bestNode],":",graph[parent[bestNode]][bestNode])
                pathG += graph[parent[bestNode]][bestNode]
                bestNode = parent[bestNode]
            path.append(origin)
            path.reverse()
            result = path,pathG
        return result

    route = pd.read_sql(querryRoute,connection)
    nodes = pd.read_sql(querryNodes,connection)
    minParam = pd.DataFrame({'ID': len(route)+1,'ORIGIN ID':0,'DESTINATION ID':0 , 'ORIGIN': 'Min Param', 'DESTINATION':'Min Param', 'DISTANCE': 0, 'PRICE':0, 'RATE':0, 'DURATION':0},index=[0])
    maxParam = pd.DataFrame({'NODE ID': len(nodes)+1, 'NODE': 'max_param', 'lat': 999, 'long':999, 'eDistance':max(route[route.columns[5]])},index=[0])
    routeNormalization(route,minParam) 
    graph = createGraph(route)
    origin = None
    destination = None
    algorithm = None

    request_data = request.get_json()
    if request_data:
        if 'origin' in request_data:
            origin = request_data['origin']
        if 'destination' in request_data:
            destination = request_data['destination']
        if 'algorithm' in request_data:
            algorithm = request_data['algorithm']

    if algorithm == 'Greedy':
        result = pathReconstruction(greedy(origin,destination,graph)[0],greedy(origin,destination,graph)[1],(greedy(origin,destination,graph)[0])[-1],origin)
    if algorithm == 'BFS':
        result = pathReconstruction(bestfirstSearch(origin,destination,graph)[0],bestfirstSearch(origin,destination,graph)[1],(bestfirstSearch(origin,destination,graph)[0])[-1],origin)
    if algorithm == 'Dijkstra':
        result = pathReconstruction(dijkstra(origin,destination,graph)[0],dijkstra(origin,destination,graph)[1],(dijkstra(origin,destination,graph)[0])[-1],origin)
    if algorithm == 'Astar':
        heuristicValues(nodes,destination)
        heuristicNormalization(nodes,maxParam)
        hList = heursiticGraph(nodes)
        result = aStar(origin,destination,graph,hList)
    if algorithm == 'FloydWarshall':
        result=FloydWarshall(origin,destination,route,nodes)
    


    return jsonify({
        'result': result
    })
     

@app.route('/addNodes', methods=['GET','POST'])
    #Database Connection
def addNodes():
    connection = mysql.connector.connect(host='localhost',
                                            database='mapscargo', # masukan nama database di kiri
                                            user='root',
                                            password='')

    querryRoute = "SELECT sample.sample_id AS 'ID', origin AS'ORIGIN ID', destination AS 'DESTINATION ID', a.city_name AS 'ORIGIN', b.city_name AS 'DESTINATION', sample.distance AS 'DISTANCE', sample.price AS 'PRICE', sample.rate AS 'RATE', sample.duration AS 'DURATION' FROM sample JOIN city a ON sample.origin = a.city_id JOIN city b ON sample.destination = b.city_id;"
    querryNodes = "SELECT city_id AS 'NODE ID', city_name AS 'NODE', lat, city.long FROM city"

    routeCursor = connection.cursor()
    routeCursor.execute(querryRoute)
    routeResult = routeCursor.fetchall()

    nodesCursor = connection.cursor()
    nodesCursor.execute(querryNodes)
    nodesResult = nodesCursor.fetchall()

    print(nodesResult)
    route = pd.DataFrame(routeResult,columns=['ID','ORIGIN ID','DESTINATION ID','ORIGIN','DESTINATION','DISTANCE','PRICE','RATE','DURATION'])
    nodes = pd.DataFrame(nodesResult,columns=['NODE ID','NODE','lat','long'])


    request_data = request.get_json()
    if request_data:
        if 'city' in request_data:
            city = request_data['city']
        if 'lat' in request_data:
            lat = int(request_data['lat'])
        if 'long' in request_data:
            long = int(request_data['long'])
    

    def addNode(city: str,lat: int,long: int,conn):

        myCursor = conn.cursor()
        sql = f"INSERT INTO `city` (`city_id`, `city_name`, `lat`, `long`) VALUES (NULL, '{city}', '{lat}', '{long}')"

        sqlCheck = f"SELECT * FROM `city` WHERE city_name = '{city}'"
        myCursor.execute(sqlCheck)
        myresult = myCursor.fetchall()

        result = "" 

        if myresult != []:
            result = "Failed!, Data has been registered"
            return result
        else :
            myCursor.execute(sql)
            conn.commit()
            result = "Update Success"
            return result
    
    result = addNode(city,lat,long,connection)
    return result

@app.route('/deleteNodes', methods=['GET','POST'])
    #Database Connection
def deleteNodes():
    #Database Connection
    connection = mysql.connector.connect(host='localhost',
                                            database='mapscargo', # masukan nama database di kiri
                                            user='root',
                                            password='')

    querryRoute = "SELECT sample.sample_id AS 'ID', origin AS'ORIGIN ID', destination AS 'DESTINATION ID', a.city_name AS 'ORIGIN', b.city_name AS 'DESTINATION', sample.distance AS 'DISTANCE', sample.price AS 'PRICE', sample.rate AS 'RATE', sample.duration AS 'DURATION' FROM sample JOIN city a ON sample.origin = a.city_id JOIN city b ON sample.destination = b.city_id;"
    querryNodes = "SELECT city_id AS 'NODE ID', city_name AS 'NODE', lat, city.long FROM city"

    routeCursor = connection.cursor()
    routeCursor.execute(querryRoute)
    routeResult = routeCursor.fetchall()

    nodesCursor = connection.cursor()
    nodesCursor.execute(querryNodes)
    nodesResult = nodesCursor.fetchall()

    print(nodesResult)
    route = pd.DataFrame(routeResult,columns=['ID','ORIGIN ID','DESTINATION ID','ORIGIN','DESTINATION','DISTANCE','PRICE','RATE','DURATION'])
    nodes = pd.DataFrame(nodesResult,columns=['NODE ID','NODE','lat','long'])

    request_data = request.get_json()
    if request_data:
        if 'nodeID' in request_data:
            nodeId = int(request_data['nodeID'])

    def deleteNode(nodeId: int,conn):

        myCursor= conn.cursor()
        sql = f"DELETE FROM `city` WHERE `city`.`city_id` = {nodeId}"
        
        myCursor.execute(sql)
        conn.commit()
        result = "" 
        if myCursor.rowcount == 0:
            result = "Failed!, No record found" 
            return result
        else:
            result = "record(s) affected"
            return result
    
    result = deleteNode(nodeId,connection)
    return result

@app.route('/addRoutes', methods=['GET','POST'])
    #Database Connection
def addRoutes():
    #Database Connection
    connection = mysql.connector.connect(host='localhost',
                                            database='mapscargo', # masukan nama database di kiri
                                            user='root',
                                            password='')

    querryRoute = "SELECT sample.sample_id AS 'ID', origin AS'ORIGIN ID', destination AS 'DESTINATION ID', a.city_name AS 'ORIGIN', b.city_name AS 'DESTINATION', sample.distance AS 'DISTANCE', sample.price AS 'PRICE', sample.rate AS 'RATE', sample.duration AS 'DURATION' FROM sample JOIN city a ON sample.origin = a.city_id JOIN city b ON sample.destination = b.city_id;"
    querryNodes = "SELECT city_id AS 'NODE ID', city_name AS 'NODE', lat, city.long FROM city"

    routeCursor = connection.cursor()
    routeCursor.execute(querryRoute)
    routeResult = routeCursor.fetchall()

    nodesCursor = connection.cursor()
    nodesCursor.execute(querryNodes)
    nodesResult = nodesCursor.fetchall()

    print(nodesResult)
    route = pd.DataFrame(routeResult,columns=['ID','ORIGIN ID','DESTINATION ID','ORIGIN','DESTINATION','DISTANCE','PRICE','RATE','DURATION'])
    nodes = pd.DataFrame(nodesResult,columns=['NODE ID','NODE','lat','long'])


    request_data = request.get_json()
    if request_data:
        if 'origin' in request_data:
            origin = request_data['origin']
        if 'destination' in request_data:
            destination = request_data['destination']
        if 'distance' in request_data:
            distance = float(request_data['distance'])
        if 'price' in request_data:
            price = float(request_data['price'])
        if 'rate' in request_data:
            rate = float(request_data['rate'])
        if 'duration' in request_data:
            duration = float(request_data['duration'])
    
    def addRoute(nodesResult,origin: str,destination: str,distance: float,price: float,rate: float,duration: float,conn):
        
        myCursor= conn.cursor()
        originId = ''
        destinationId = ''
        result = ""
        for row in nodesResult:
            if row[1]==origin:
                originId=row[0]
            elif row[1]==destination:
                destinationId=row[0]
        if originId == '' or destinationId == '':
            result = "Node hasn't registered"
            return result
        else:
            sql = f"INSERT INTO `sample` (`sample_id`, `origin`, `destination`, `distance`, `price`, `rate`, `duration`, `airline`) VALUES (NULL, '{originId}', '{destinationId}', '{distance}', '{price}', '{rate}', '{duration}', '')"
            myCursor.execute(sql)
            conn.commit()
            result =  "record(s) affected"
            return result

    result = addRoute(nodesResult,origin,destination,distance,price,rate,duration,connection)
    return result

@app.route('/deleteRoutes', methods=['GET','POST'])
    #Database Connection
def deleteRoutes():
    #Database Connection
    connection = mysql.connector.connect(host='localhost',
                                            database='mapscargo', # masukan nama database di kiri
                                            user='root',
                                            password='')

    querryRoute = "SELECT sample.sample_id AS 'ID', origin AS'ORIGIN ID', destination AS 'DESTINATION ID', a.city_name AS 'ORIGIN', b.city_name AS 'DESTINATION', sample.distance AS 'DISTANCE', sample.price AS 'PRICE', sample.rate AS 'RATE', sample.duration AS 'DURATION' FROM sample JOIN city a ON sample.origin = a.city_id JOIN city b ON sample.destination = b.city_id;"
    querryNodes = "SELECT city_id AS 'NODE ID', city_name AS 'NODE', lat, city.long FROM city"

    routeCursor = connection.cursor()
    routeCursor.execute(querryRoute)
    routeResult = routeCursor.fetchall()

    nodesCursor = connection.cursor()
    nodesCursor.execute(querryNodes)
    nodesResult = nodesCursor.fetchall()

    print(nodesResult)
    route = pd.DataFrame(routeResult,columns=['ID','ORIGIN ID','DESTINATION ID','ORIGIN','DESTINATION','DISTANCE','PRICE','RATE','DURATION'])
    nodes = pd.DataFrame(nodesResult,columns=['NODE ID','NODE','lat','long'])


    request_data = request.get_json()
    if request_data:
        if 'routeID' in request_data:
            routeID = int(request_data['routeID'])
       
    def deleteRoute(routeId,conn):
        result = ""
        myCursor= conn.cursor()
        sql = f"DELETE FROM `sample` WHERE `sample`.`sample_id` = {routeId}"
        
        myCursor.execute(sql)
        conn.commit()
        if myCursor.rowcount == 0:
            result = "No record found"
            return result
        else:
            result = "record(s) affected"
            return result
    
    result = deleteRoute(routeID,connection)
    return result

# driver function
if __name__ == '__main__':
    #website_url = '10.251.251.169:8080'
    website_url = 'localhost:8080'
    app.config['SERVER_NAME'] = website_url
    app.run()