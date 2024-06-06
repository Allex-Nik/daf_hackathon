import base64
import requests 
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from sklearn.cluster import KMeans
from sklearn.covariance import EllipticEnvelope
from sklearn.decomposition import PCA
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')


def get_truck_info(vin="XLRTEF5300G450805", start_date="2024-03-25", end_date="2024-06-03"):

    auth_URL = 'https://api.connect.daf.com/rfms/token'
    base_URL = 'https://api.connect.daf.com'

    username= "Hackathon_4@daftrucks.com"
    password = "Team4Hackathon!"
    creds = username +':' + password
    creds_bytes = creds.encode('ascii')
    base64_bytes = base64.b64encode(creds_bytes)
    base64_message = base64_bytes.decode('ascii')
    headers = {
    'Authorization': 'Basic ' + base64_message }

    r = requests.post(auth_URL, headers=headers, verify=False)
    jsondata = r.json()
    token = jsondata.get('access_token')

    datetype ='&datetype=received'
    triggerfilter = '&Triggerfilter=DRIVER_1_WORKING_STATE_CHANGED'

    header = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/vnd.fmsstandard.com.vehiclestatuses.v3.0+json; UTF-8'}

    data = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date:
        starttime = current_date.strftime("%Y-%m-%d") + "T23:59:59.999Z"
        stoptime = (current_date + timedelta(days=1)).strftime("%Y-%m-%d") + "T23:59:59.999Z"

        myurl = base_URL+'/rfms/vehiclestatuses?vin=' + vin +'&starttime=' + starttime

        req = requests.get(myurl, headers=header, verify=False)
        # print(jsondata)
        jsondata=req.json()
#       # print(jsondata)



        for i in jsondata['vehicleStatusResponse']['vehicleStatuses']:
            dat=[]
            dat.append(i['vin'])
            dat.append(i['triggerType']['triggerType'])
            dat.append(i['triggerType']['context'])
            dat.append(i['createdDateTime'])
            dat.append(i['receivedDateTime'])
            try:
                dat.append(i['hrTotalVehicleDistance'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['totalEngineHours'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['grossCombinationVehicleWeight'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['snapshotData']['gnssPosition']['latitude'])
            except Exception:
                dat.append(-9999)

            try:
                dat.append(i['snapshotData']['gnssPosition']['longitude'])
            except Exception:
                dat.append(-9999)

            try:
                dat.append(i['snapshotData']['gnssPosition']['heading'])
            except Exception:
                dat.append(-9999)

            try:
                dat.append(i['snapshotData']['gnssPosition']['speed'])
            except Exception:
                dat.append(-9999)

            try:
                dat.append(i['snapshotData']['gnssPosition']['positionDateTime'])
            except Exception:
                dat.append(None)

            try:
                dat.append(i['snapshotData']['wheelBasedSpeed'])
            except Exception:
                dat.append(0)

            dat.append(i['snapshotData']['fuelType'])

            try:
                dat.append(i['snapshotData']['fuelLevel1'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['snapshotData']['catalystFuelLevel'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['snapshotData']['driver1WorkingState'])
            except Exception:
                dat.append(None)

            try:
                dat.append(i['snapshotData']['driver2WorkingState'])
            except Exception:
                dat.append(None)

            try:
                dat.append(i['snapshotData']['ambientAirTemperature'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['uptimeData']['engineCoolantTemperature'])
            except Exception:
                dat.append(0)
            try:
                dat.append(i['uptimeData']['serviceBrakeAirPressureCircuit1'])
            except Exception:
                dat.append(0)

            try:
                dat.append(i['uptimeData']['serviceBrakeAirPressureCircuit2'])
            except Exception:
                dat.append(0)

            data.append(dat)

        current_date += timedelta(days=1)

    df = pd.DataFrame(data, columns=['vin', 'triggerType_triggerType',
                                        'triggerType_context','createdDateTime',"receivedDateTime",
                                        "hrTotalVehicleDistance","totalEngineHours","grossCombinationVehicleWeight",
                                        'snapshotData_gnssPosition_latitude','snapshotData_gnssPosition_longitude',
                                        "snapshotData_gnssPosition_heading","snapshotData_gnssPosition_speed",
                                        "snapshotData_gnssPosition_positionDateTime",
                                        'snapshotData_wheelBasedSpeed','snapshotData_fuelType',
                                        'snapshotData_fuelLevel1','snapshotData_catalystFuelLevel',
                                        'snapshotData_driver1WorkingState','snapshotData_driver2WorkingState',
                                        'snapshotData_ambientAirTemperature','uptimeData_engineCoolantTemperature',
                                        'uptimeData_serviceBrakeAirPressureCircuit1','uptimeData_serviceBrakeAirPressureCircuit2'])

    df.drop_duplicates(inplace=True)
    
    return df


def get_dates_online():
    
    # Get today's date
    today = datetime.today().date()

    # Calculate the date 70 days before today
    days_before = today - timedelta(days=70)

    # Format the dates as YYYY-MM-DD
    today_str = today.strftime('%Y-%m-%d')
    days_before_str = days_before.strftime('%Y-%m-%d')

    # Create the tuple
    return today_str, days_before_str

# get the dates
end_date, start_date = get_dates_online()

df_truck = get_truck_info(start_date=start_date, end_date=end_date)