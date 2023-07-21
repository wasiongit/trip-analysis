import pandas as pd
from datetime import datetime
import os
import math


def haversine(lat1, lon1, lat2, lon2)->float:
    """This functions returns distance in KM from latitude and longitude values.
    :param lat1: a numeric value
    :type lat1: float type
    :param lon1: a numeric value
    :type lon1: float type
    :param lat2: a numeric value
    :type lat2: float type
    :param lon2: a numeric value
    :type lon2: float type
    """
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


def main_query_f(input_time1,input_time2) ->bool:
    """This is the main query function, it saves the data in excel for the given range by user
    and if no data found in the given range then returns the no data found message.
    
    Returns a boolean value according to if Data found or not for the range 
    This function reads all the csv files from the EOL-dump folder and  
    :param input_time1: a numeric value
    :type input_time1: int type
    :param input_time2: a numeric value
    :type input_time2: int type

    1. It takes two arguments i.e. the start and end time between which we want the data.
    2. It takes all the CSV file one by one from the EOL-dump folder and read that file as a pandas data frame
    3. Now the function filters the data frame and takes data only within the limits of time.
    4. Now we are good to get some of the values from this filtered data frame like License plate number, Distance, Average Speed, Number of Speed Violations
    and if the data frame would be empty then we continue to check for other vehicles' data.
    5. Similarly now the function filters the Trip-Info.csv data frame within the limits given by the user and takes the values Number of Trips Completed and Transporter Name from the data frame
    6. Now to use the solution as an API I used Flask and the Flask can be run with the function app.py

    """

    time1 = datetime.fromtimestamp(input_time1)
    time2 = datetime.fromtimestamp(input_time2)
    trips_df=pd.read_csv('Trip-info.csv',index_col=0)
    trips_df['datetime_ns'] = pd.to_datetime(trips_df['date_time'], format='%Y%m%d%H%M%S')
    vehicles=os.listdir('EOL-dump')
    data=[] #to store output data
    print('Total no. of vehicles ',len(vehicles))
    i=1
    for vehicle in vehicles:
        print('Vehicle ',i)
        i+=1
        raw_df=pd.read_csv(f'EOL-dump/{vehicle}',index_col=0,dtype={'lat':float,'lname':str,'lon':float})
        filterd_df=raw_df.query(f'tis >{input_time1} and tis<{input_time2}')
        if filterd_df.count()[0]==0:
            continue # if No Data found
        license_plate_no=filterd_df['lic_plate_no'].to_list()[0]
        avg_speed=filterd_df['spd'].dropna().describe()['mean'] #droping null values
        n_over_speed=filterd_df.query('osf==True').count()[0]
        filterd_df=filterd_df.sort_values('tis',ignore_index=True) # sorting by time in asc order to calculate distance
        distances=[]
        lat1=filterd_df['lat'][0]
        lon1=filterd_df['lon'][0]
        for ind in filterd_df.index:
            lat2=filterd_df['lat'][ind]
            lon2=filterd_df['lon'][ind]
            distances.append(haversine(lat1,lon1,lat2,lon2))
            lat1=lat2 # updating the values
            lon1=lon2 # updating the values
        filterd_df['Distances']=distances
        total_distance=filterd_df['Distances'].sum()
        filtertrips_df=trips_df.query(f"vehicle_number=='{license_plate_no}'")
        filtertrips_df=filtertrips_df.query(f'datetime_ns >"{time1}" and datetime_ns<"{time2}"')
        if filtertrips_df.count()[0]==0:
            continue #if no data found within the limits
        no_of_trips=filtertrips_df.count()[0]
        transporter_name=filtertrips_df['transporter_name'].to_list()[0]
        row=(license_plate_no,total_distance,no_of_trips,avg_speed,transporter_name,n_over_speed)
        data.append(row)  
    if len(data)==0:
        return False
    output_df=pd.DataFrame(data)
    output_df.columns=['License plate number','Distance','Number of Trips Completed','Average Speed','Transporter Name','Number of Speed Violations']
    output_df.to_excel('static/output.xlsx',index=False)
    return True
