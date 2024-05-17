import streamlit as st
import datetime
import requests

'''
# TaxiFareModel front
'''
st.image('taxi.jpg')

st.markdown('''## Taxi fare estimator''')

date_time = st.date_input(
    "Select a date for booking a taxi:",
    datetime.date(2024, 5, 17))

time = st.time_input('Select a time for booking a taxi:', datetime.time(8, 45))

st.write(f"The selected date and time for booking a tax are {date_time} - {time}")


pickup_lon = st.number_input('Specify pickup LOGITUDE?')
pickup_lat =st.number_input('Specify pickup LATITUDE?')
dropoff_lon= st.number_input('Specify dropoff LONGITUTE?')
dropoff_lat=st.number_input('Specify dropoff LATITUDE?')
passenger_count=st.number_input('How many passengers are travelling?')


# Once we have these, let's call our API in order to retrieve a prediction

#See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

#🤔 How could we call our API ? Off course... The `requests` package 💡


url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')



#2. Let's build a dictionary containing the parameters for our API...
parameters = {
              'pickup_datetime' : f'{date_time} {time}',
              'pickup_longitude' : pickup_lon,
              'pickup_latitude' : pickup_lat,
              'dropoff_longitude' : dropoff_lon,
              'dropoff_latitude' : dropoff_lat,
              'passenger_count': int(passenger_count)
              }

#3. Let's call our API using the `requests` package...
response = requests.get(url, params=parameters).json()

#4. Let's retrieve the prediction from the **JSON** returned by the API...
st.write('Your estimated fare is :$',round(response['fare'],2))

#4. Let's implement the map

@st.cache
def get_map_data():
    return pd.DataFrame(
            np.array([[pickup_lat, pickup_lon], [dropoff_lat, dropoff_lon]]),
            columns=['lat', 'lon']
        )
df = get_map_data()
st.map(df)

#5. Add the pickup and dropof marks on the map

p_address = st.text_input('Pick-up address', 'rump Tower')
d_address = st.text_input('Drop-off address', 'Empire State Building')
url_address = 'https://nominatim.openstreetmap.org/search'
p_response = requests.get(url_address, params={'q': p_address, 'format': 'json'}).json()
p_lat = float(p_response[0]['lat'])
p_lon = float(p_response[0]['lon'])
d_response = requests.get(url_address, params={'q': d_address, 'format': 'json'}).json()
d_lat = float(d_response[0]['lat'])
d_lon = float(d_response[0]['lon'])
