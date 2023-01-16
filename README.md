# Framework DoRoute: Python-based programming to implement finding the shortest path algorithm with the REST API web service

DoRoute is a framework for the shortest path algorithm. it builds based on REST-API which makes it easier to do data exchange. Moreover, DoRoute has more than one shortest path algorithms implementation including Greedy, Best First Search, Dijkstra, A*, and Floyd-Warshall. DoRoute is a flexible framework because it has a route database that can be easily modified according to a particular case. Furthermore, DoRoute uses an open-source python framework that is easy to install and deploy. However, DoRoute only provides 5 algorithms for this current version. However, researchers and practitioners can easily develop their algorithm using DoRoute Framework



## Installation

Requirements :
1. Command Prompt or any terminal
2. Postman
3. Mysql (Database)
4. Flask (Web App)


## Usage example

The current version of DoRoute only provides five shortest path algorithms, you can choose the algorithm by sending the parameters on the HTTP request.

1. Execute the python file (change the directory according where you put the DoRoute.py file)

```sh
D:\FrameworkDoRoute>python DoRoute.py
```
after running the python script, the flask web App will automatically run, now we just need to create an HTTP request with the GET method, in this process you can use postman

2. Open Postman and gives the following parameters on body
URL:localhost:8080/findRoute

the parameters that will be given to the body are origin, destination, and the algorithm to be used, the data type must use the JSON format. 

Example parameter:
```sh
{
    "algorithm":"Astar",
    "origin":"Jakarta",
    "destination":"Jayapura"
}
```
After the HTTP response status code show 200, which means the HTTP request was successful, you will receive an output in the form of JSON data containing route suggestions and the overall cost.

This DoRoute framework can also perform CRUD with databases via REST-API, It has four CRUD function: add node, delete node, add route, and delete route. Add node is used to add a new node, delete node is used to delete node, add route is used to add a new path, and delete route is used to delete a path. Here are some samples:

ADD NODES
URL : localhost:8080/addNodes
Three HTTP request parameters are required for the add node function: city name, latitude, and longitude

Example parameters:
```sh
{
    "city":"Kalimantan",
    "lat":"100",
    "long":"100"
}
```

If the HTTP response status code [15] show 200, the response will provide output in the form of text “updated success”, if it fails, the response will give an output in the form of text “Failed!, Data has been registered”.

DELETE NODES
URL : localhost:8080/deleteNodes.
For the delete node function, one HTTP request parameters is required: nodeId

Example parameters:
```sh
{
    "nodeId":"24"
}
```
If the HTTP response status code show 200, the response will provide output in the form of text “record(s) affected”, if it fails, the response will give an output in the form of text “Failed!, No record found”.

ADD ROUTES
URL : localhost:8080/addRoutes
For the add route function, six HTTP request parameters is required: origin, destination, distance, price, rate, duration

example parameters:
```sh
{
    "origin":"Sabah",
    "destination":"Jayapura",
    "distance":"800",
    "price":"20000",
    "rate":"4",
    "duration":"4"
}
```
If the HTTP response status code [15] show 200, the response will provide output in the form of text “record(s) affected”, if it fails, the response will give an output in the form of text “Node hasn’t registered”.

DELETE NODES
URL : localhost:8080/deleteRoutes
For the delete route function, one HTTP request [12] parameters is required: routeId

Example parameters:
```sh
{
    "routeId":"36"
}
```
If the HTTP response status code [15]  show 200, the response will provide output in the form of text “record(s) affected”, if it fails, the response will give an output in the form of text “No record found”.


_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Requirements Python Libraries:
1. MySQL-connector-python
2. numpy
3. pandas
4. scikit-learn
5. Flask

Installation
```sh
pip install MySQL-connector-python
pip install numpy
pip install pandas
pip install scikit-learn
pip install Flask
```

## Meta

AUTHOR
1. Dedy Rahman Wijaya
2. Patrick Adolf Telnoni
3. Wahyu Yulianto
4. Khalid Umar Saifullah

CURRENT VERSION of DoRoute

v1.0

LEGAL CODE LICENSE

[license][license]


## Contributing

1. Fork it (<https://github.com/JstKhalid/DoRoute>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[license]: https://github.com/JstKhalid/DoRoute/blob/main/LICENSE
