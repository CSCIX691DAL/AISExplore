# AISExplore
The automatic identification system (AIS) is an automatic tracking system that uses transponders on ships and is used by vessel traffic services (VTS). [Wikipedia](https://en.wikipedia.org/wiki/Automatic_identification_system)

The AISExplore project collects and allows for the display of these messages.


## Running the software

Running this software will require Nodejs, Python3 (with certain dependencies) and MongoDB

You can run the software by running the following commands on a linux system when all software dependencies listed in the Software dependencies section below are installed,
Then opening a web browser to http://localhost:8000

### Running the nodejs listener

You can run the nodejs listener by running the following command in the SocketListener Directory 
 
> nodejs DataForwarder.js

### Running the Django Server

You can run the Django server by running the following commands in the WebApp Directory 
 
> python3 manage.py migrate

> python3 manage.py runserver


### Usage

You can visit the running server at localhost:8000
 
The map will load all ships within the current view from the server
 
### Developer Api

Developers can access the raw database output without updating the map by accessing the following urls which return JSON
Arrays with the specified data.

> localhost:8000/raw/latest

Will return the latest entries for all ships in the database in the format {"results": {database entrys}},
With all database entries in the form of key pair values of the mmsi and the latest entry for that ship

> localhost:8000/raw/region/{geometry}

Will return the entries for all ships in the database in whose coordinate points lie within the coordinates supplied in json format
after region/, the geometry must be valid json and each point must be specified in a list, any amount of coordinates can be provided 
but take care as point order matters, you may end up asking for an hourglass rather than a square also you don't need to close the geometry
it will be take care of for you.
(Ex. {"nw":[40.32, -60.21], "ne":[39.50, -60.21], "se":[39.50, -61.20], "sw":[40.32, -61.20] })

> localhost:8000/raw/search/[criteria]

Allows you to search the database depending on the provided criteria, criteria can reference and search specific ais message fields by typing the name of the field then equals and the value you wish to search for these can be comma delimited. 

(Ex. name=ALPHA) 


## Software dependencies

### Installation on ubuntu ###
The following packages will needed to be installed to run this software instructions provided are for ubuntu/debian based systems,
you can install these packages by running the following command substituting the package name for the underscores.
> sudo apt update

> sudo apt install ______
- git
- apache2
- python3-pip
- libpq-dev
- python3-dev
- python3-wheel
- g++
- mongodb
- nodejs

### python dependancies ###

The following will needed to be installed to run this software they can be installed after installing python3
by opening your command line and entering the following command at the root of the project.
> pip3 install setuptools

> pip3 install wheel

> pip3 install -r requirements.txt 
