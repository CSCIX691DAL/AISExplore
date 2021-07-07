###  Running Guide for File Listener

Requirements:
- Libais
- psycopg, 
- pymongo

Virtual Enviroment ?
    not necessary
    

Main Application
> This application utilizes TCP and writes data to a new file
every hour of the day. It also supports creating directories. 

App.py: `python app.py`

#### Decoder
Program works with both directories and single files

Directory: `python decode.py -dir 2019/07/08/`

Single File:`python decode.py -f  2019**.csv`