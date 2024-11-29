import pandas as pd
import streamlit as st

st.title('Pricing spread')

df = pd.read_excel('Карта рынка.xlsx', skiprows=1)
df['spread'] = (df['Спред, пп'] * 100)
df['Yield'] = ((100 - df['Цена, пп']) * 100) / df['Срок  до погашения / оферты, лет']
df['Cupon'] = df['spread'] / df['Цена, пп'] * 100 - df['spread']
df['Cspread'] = round(df['spread'] + df['Cupon'] + df['Yield'])


s_df = df[['ISIN','Тикер','Рейтинг','Цена, пп', 'Срок  до погашения / оферты, лет','spread','Cspread']].copy()

# Фильтры для столбцов
tickers = s_df['Тикер'].unique()
selected_tickers = st.multiselect('Выберите тикер:', tickers)

# Фильтрация данных
f_df = s_df[(s_df['Тикер'].isin(selected_tickers) | (len(selected_tickers) == 0))]

# Отображение отфильтрованного DataFrame
st.dataframe(f_df)

if not f_df.empty:
    # Выбор облигации
    selected_bond = st.selectbox('Выберите облигацию:', f_df['Тикер'].unique())
    bond_data = f_df[f_df['Тикер'] == selected_bond].iloc[0]

    # Ввод цены или спреда
    input_type = st.radio("Выберите, что хотите ввести:", ("Цена", "Спред"))

    if input_type == "Цена":
        price_input = st.number_input("Введите цену облигации:", min_value=0.0, step=0.01)
        if st.button("Рассчитать спред"):
            # Расчет спреда на основе введенной цены
            spread_calculated = round(bond_data['spread'] + (bond_data['spread'] / price_input * 100 - bond_data['spread']) + (((100 - price_input) * 100) / bond_data['Срок  до погашения / оферты, лет']))
            st.success(f"Расчитанный спред: {spread_calculated:.2f}")
    
    elif input_type == "Спред":
        spread_input = st.number_input("Введите спред:", min_value=0.0, step=0.01)
        if st.button("Рассчитать цену"):
            # Расчет цены на основе введенного спреда
            
            price_calculated = ((100-spread_input*bond_data['Срок  до погашения / оферты, лет']/100)+((100-spread_input*bond_data['Срок  до погашения / оферты, лет']/100)**2+4*bond_data['Срок  до погашения / оферты, лет']*bond_data['spread'])**0.5)/2

            
            st.success(f"Расчитанная цена: {price_calculated:.2f}")
