import pandas as pd
import streamlit as st

st.title('Pricing spread')

df = pd.read_excel('Карта рынка.xlsx', skiprows=1)
df['spread'] = (df['Спред, пп'] * 100)
df['Yield'] = ((100 - df['Цена, пп']) * 100) / df['Срок  до погашения / оферты, лет']
df['Cupon'] = df['spread'] / df['Цена, пп'] * 100 - df['spread']
df['Cspread'] = round(df['spread'] + df['Cupon'] + df['Yield'])

s_df = df[['ISIN','Тикер','Рейтинг','Цена, пп', 'Срок  до погашения / оферты, лет','Cspread']].copy()

# Фильтры для столбцов
tickers = s_df['Тикер'].unique()
selected_tickers = st.multiselect('Выберите тикер:', tickers)

# Фильтрация данных
f_df = s_df[(s_df['Тикер'].isin(selected_tickers) | (len(selected_tickers) == 0))]

# Отображение отфильтрованного DataFrame
st.dataframe(f_df)
