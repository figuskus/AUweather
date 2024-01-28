import pickle
from datetime import datetime
import streamlit as st
import numpy as np
from weather import get_weather
import path
import datetime as dt
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

starttime = datetime.now()
dir = path.Path(__file__).abspath()
# sys.append.path(dir.parent.parent)

# load model
pathToModel = './model.h5'

with open(pathToModel, 'rb') as file:
    model = pickle.load(file)


today = dt.date.today()
Location = {'Adelaide': 0, 'Albany': 1, 'Albury': 2, 'AliceSprings': 3, 'BadgerysCreek': 4, 'Ballarat': 5, 'Bendigo': 6, 'Brisbane': 7, 'Cairns': 8, 'Canberra': 9, 'Cobar': 10, 'CoffsHarbour': 11, 'Dartmoor': 12, 'Darwin': 13, 'GoldCoast': 14, 'Hobart': 15, 'Katherine': 16, 'Launceston': 17, 'Melbourne': 18, 'MelbourneAirport': 19, 'Mildura': 20, 'Moree': 21, 'MountGambier': 22, 'MountGinini': 23, 'Newcastle': 24, 'Nhil': 25, 'NorahHead': 26, 'NorfolkIsland': 27, 'Nuriootpa': 28, 'PearceRAAF': 29, 'Penrith': 30, 'Perth': 31, 'PerthAirport': 32, 'Portland': 33, 'Richmond': 34, 'Sale': 35, 'SalmonGums': 36, 'Sydney': 37, 'SydneyAirport': 38, 'Townsville': 39, 'Tuggeranong': 40, 'Uluru': 41, 'WaggaWagga': 42, 'Walpole': 43, 'Watsonia': 44, 'Williamtown': 45, 'Witchcliffe': 46, 'Wollongong': 47, 'Woomera': 48}

def main():
    st.set_page_config(page_title="Czy jutro w Australii będzie padać?")
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()

    st.image("https://content.api.news/v3/images/bin/6a48333d1aa571be691beb66566c7524")

    with overview:
        st.title("Czy jutro w Australii będzie padać?")

    with left:
        miasto = st.selectbox("Wybierz miasto",Location.keys())

    predictButton = st.button("Sprawdź czy jutro pada")


    

    if predictButton:
        Week = today.strftime("%U")
        weather = get_weather(miasto)
        data = np.array([int(Week),miasto,weather[0],weather[1],weather[2],weather[3],weather[4],weather[5],weather[6],weather[7],weather[8],weather[9],weather[10]]).reshape(1, -1)
        headers = ['Numer tygodnia','Lokalizacja','Minimalna temperatura', 'Maksymalna temperatura', 'Opady deszczu', 'Kierunek porywu wiatru', 'Prędkość porywu wiatru', 'Kierunek wiatru o 9 rano', 'Kierunek wiatru o 3 po południu', 'Średnia prędkość wiatru', 'Średnia wilgotność', 'Średnie ciśnienie', 'Czy padało dzisiaj']
        values = [int(Week),Location[miasto],weather[0],weather[1],weather[2],weather[3],weather[4],weather[5],weather[6],weather[7],weather[8],weather[9],weather[10]]
        df = pd.DataFrame(values_transposed, columns=headers)
        st.write(df)
        
        st.write()
        rain = model.predict(data)
        s_confidence = model.predict_proba(data)
        pewnosc = str(s_confidence[0][0]*100)
        # st.write(s_confidence)
        st.header("Czy będzie jutro padać w "+miasto+", Australia? {0}".format("Tak" if rain[0] == 1 else "Nie"))
        # st.subheader("Pewność predykcji {0:.2f} %".format(s_confidence[0][rain][0]*100))
        st.subheader("Pewność predykcji "+pewnosc+" %")


if __name__  == "__main__":
    main()
