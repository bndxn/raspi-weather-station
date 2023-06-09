from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import plotly.express as px
import boto3
import numpy as np
from helpers import ddb_connection, graphers

application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')


@application.route('/temp_local')
def temp_local():
   
   df = ddb_connection.df_stored_locally()

   fig = graphers.overlapping_temperature_and_humidity(df)

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON,
            header='Local copy', description='Data stored locally (non-DDB)')


@application.route('/last_day')
def last_day():

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

   connection = ddb_connection.DynamoResource()

   df = ddb_connection.DynamoResource.query(connection, day_ago)

   fig = graphers.overlapping_temperature_and_humidity(df)

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON, 
            header='Last day', description='Temperature and humidity over the last day')


@application.route('/last_week')
def last_week():
   return render_template('index.html')


@application.route('/all_time')
def all_time():

   connection = ddb_connection.DynamoResource()

   df = ddb_connection.DynamoResource.query(connection)

   fig = px.scatter(df, x='timestamp', y='temperature')
   
   fig.update_yaxes(title_text='Temperature')
   fig.update_xaxes(title_text='Time')


   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON,
            header='Temperature only', description='Temperature only, since start of measurements.')


if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

