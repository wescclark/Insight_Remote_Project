from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
from a_Model import ModelIt
import requests

#user = 'postgres' #add your username here (same as previous postgreSQL)
#password = 'ragnarok'                      
host = 'localhost'
#dbname = 'birth_db'
#engine = create_engine('postgres://postgres:ragnarok@localhost/birth_db')
#db = create_engine('postgres://%s:%s@%s/%s'%(user,password,host,dbname))
#con = None
#con = psycopg2.connect(database = dbname, user = user, password = password)
def is_url_ok(url):
	full_url = 'https://www.youtube.com/watch?v='+vid
	return(200 == requests.head(url).status_code)
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Bananaphone' },
       )


	


@app.route('/input')
def input():
    return render_template("input.html")


@app.route('/output')
def output():
  
	vid = request.args.get('video_id')
	if not vid:
		vid = 'dQw4w9WgXcQ'
  
	
	if is_url_ok == False:
		vid = 'dQw4w9WgXcQ'
	
	
  
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
  #query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
  #print(query)
  #query_results=pd.read_sql_query(query,con)
  #print(query_results)
  #births = []
  #for i in range(0,query_results.shape[0]):
      #births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
	the_result, plot_url, country_demo = ModelIt(vid)
	return render_template("output.html", embed_id = 'https://www.youtube.com/embed/' + vid, video_id = vid, plot_url = plot_url, the_result = the_result, country_demo = country_demo)
