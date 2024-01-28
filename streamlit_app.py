import pickle
from datetime import datetime
import streamlit as st
import numpy as np
from weather import get_weather
import path
import datetime as dt

starttime = datetime.now()
dir = path.Path(__file__).abspath()
# sys.append.path(dir.parent.parent)

# load model
pathToModel = './model.h5'

with open(pathToModel, 'rb') as file:
    model = pickle.load(file)


today = dt.date.today()
Location = {0: 'Adelaide', 1: 'Albany', 2: 'Albury', 3: 'AliceSprings', 4: 'BadgerysCreek', 5: 'Ballarat', 6: 'Bendigo', 7: 'Brisbane', 8: 'Cairns', 9: 'Canberra', 10: 'Cobar', 11: 'CoffsHarbour', 12: 'Dartmoor', 13: 'Darwin', 14: 'GoldCoast', 15: 'Hobart', 16: 'Katherine', 17: 'Launceston', 18: 'Melbourne', 19: 'MelbourneAirport', 20: 'Mildura', 21: 'Moree', 22: 'MountGambier', 23: 'MountGinini', 24: 'Newcastle', 25: 'Nhil', 26: 'NorahHead', 27: 'NorfolkIsland', 28: 'Nuriootpa', 29: 'PearceRAAF', 30: 'Penrith', 31: 'Perth', 32: 'PerthAirport', 33: 'Portland', 34: 'Richmond', 35: 'Sale', 36: 'SalmonGums', 37: 'Sydney', 38: 'SydneyAirport', 39: 'Townsville', 40: 'Tuggeranong', 41: 'Uluru', 42: 'WaggaWagga', 43: 'Walpole', 44: 'Watsonia', 45: 'Williamtown', 46: 'Witchcliffe', 47: 'Wollongong', 48: 'Woomera'}


def main():
    st.set_page_config(page_title="Czy jutro w Australii będzie padać?")
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()

    st.image("https://content.api.news/v3/images/bin/6a48333d1aa571be691beb66566c7524")

    with overview:
        st.title("Czy przeżyłbyś tytanica?")

    with left:
        miasto = st.selectbox("Wybierz miasto",Location.keys())

    predictButton = st.button("Sprawdź czy jutro pada")


    

    if predictButton:
        Week = today.strftime("%U")
        weather = get_weather(miasto)
        data = np.array([int(Week),Location[x],weather[0],weather[1],weather[2],weather[3],weather[4],weather[5],weather[6],weather[7],weather[8],weather[9],weather[10]]).reshape(1, -1)
        st.write(data)
        rain = model.predict(data)
        s_confidence = model.predict_proba(data)
        with prediction:
            st.header("Czy będzie jutro padać w {miasto}, Australia?{0}".format("Tak" if rain[0] == 1 else "Nie"))
            st.subheader("Pewność predykcji {0:.2f} %".format(s_confidence[0][rain][0]*100))

if __name__  == "__main__":
    main()
