import pickle
from datetime import datetime
import streamlit as st
import numpy as np
from weather import get_weather
import path
import sys

starttime = datetime.now()
dir = path.Path(__file__).abspath()
# sys.append.path(dir.parent.parent)

# load model
print(dir)
pathToModel = '../model.h5'

with open(dir, 'rb') as file:
    model = pickle.load(file)


today = datetime.date.today()
Location = {'Adelaide': 0, 'Albany': 1, 'Albury': 2, 'AliceSprings': 3, 'BadgerysCreek': 4, 'Ballarat': 5, 'Bendigo': 6, 'Brisbane': 7, 'Cairns': 8, 'Canberra': 9, 'Cobar': 10, 'CoffsHarbour': 11, 'Dartmoor': 12, 'Darwin': 13, 'GoldCoast': 14, 'Hobart': 15, 'Katherine': 16, 'Launceston': 17, 'Melbourne': 18, 'MelbourneAirport': 19, 'Mildura': 20, 'Moree': 21, 'MountGambier': 22, 'MountGinini': 23, 'Newcastle': 24, 'Nhil': 25, 'NorahHead': 26, 'NorfolkIsland': 27, 'Nuriootpa': 28, 'PearceRAAF': 29, 'Penrith': 30, 'Perth': 31, 'PerthAirport': 32, 'Portland': 33, 'Richmond': 34, 'Sale': 35, 'SalmonGums': 36, 'Sydney': 37, 'SydneyAirport': 38, 'Townsville': 39, 'Tuggeranong': 40, 'Uluru': 41, 'WaggaWagga': 42, 'Walpole': 43, 'Watsonia': 44, 'Williamtown': 45, 'Witchcliffe': 46, 'Wollongong': 47, 'Woomera': 48}


def main():
    st.set_page_config(page_title="Czy jutro w Australii będzie padać?")
    overview = st.container()
    center = st.columns(1)
    prediction = st.container()
    predictButton = st.button("Sprawdź czy jutro pada")

    st.image("https://media1.popsugar-assets.com/files/thumbor/7CwCuGAKxT"
             "rQ4wPyOBpKjSsd1JI/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!"
             "-/2017/04/19/743/n/41542884/5429b59c8e78fbc4_MCDTITA_FE014_H_1_.JPG")
    with overview:
        st.title("Czy przeżyłbyś tytanica?")

    with center:
        miasto = st.radio("Miasto",list(Location.keys()), format_func=lambda x: Location[x])


    

    rain = model.predict(data)
    s_confidence = model.predict_proba(data)
    with predictButton:
        Week = today.strftime("%U")
        weather = get_weather(miasto)
        data = np.array([Week,miasto,weather[0],weather[1],weather[2],weather[3],weather[4],weather[5],weather[6],weather[7],weather[8],weather[9],weather[10]]).reshape(1, -1)
        with prediction:
            st.header("Czy będzie jutro padać w {miasto}, Australia?{0}".format("Tak" if rain[0] == 1 else "Nie"))
            st.subheader("Pewność predykcji {0:.2f} %".format(s_confidence[0][rain][0]*100))

if __name__  == "__main__":
    main()
