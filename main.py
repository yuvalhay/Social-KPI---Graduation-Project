import streamlit as st

# from streamlit_option_menu import option_menu
# import streamlit.components.v1 as html
# from PIL import Image
# import cv2
# from st_aggrid import AgGrid
# import plotly.express as px
# import io

header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()
Loneliness_default_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]


def update_slider(kpi_name, value):
    del st.session_state[kpi_name]
    st.session_state[kpi_name] = value


def count_by_sign(sign):
    # count_non_zeros = count_zeros + count_negatives
    count_zeros = 0
    count_negatives = 0
    for val in st.session_state.values():
        if val < 0:
            count_negatives += 1
        if val == 0:
            count_zeros += 1
    if sign == 0:
        return count_zeros
    elif sign == -1: return count_negatives
    else: return count_zeros + count_negatives

with header:
    st.title("The visualization of our KPI's")
    st.text("1: Loneliness KPI")
    st.text("2: Health KPI")
    st.text("3: Economic Strength KPI")

with kpi_selection:
    st.header("KPI Selection")
    KPI_names = ["Loneliness", "Health", "Economic Strength"]
    KPI_page = st.radio("Choose", KPI_names)
    # firstKPI, secondKPI, thirdKPI, clear = st.columns([0.5, 0.4, 1, 1])
    # with firstKPI:
    #     loneliness_kpi_button = st.button("Loneliness")
    # with secondKPI:
    #     health_kpi_button = st.button("Health")
    # with thirdKPI:
    #     economic_strength_kpi_button = st.button("Economic Strength")
    # with clear:
    #     clear_button = st.button("Clear")

with kpi_weights:
    st.header("KPI weights")
    current_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
    Loneliness_kpi_dict = {"arnona_cat":0, "members_Water":0, "martial":0, "widow_grown":0, "widow_elderlies":0, "lonely_elderlies":0, "p85_plus":0, "accumulated_cases":0}

    current_ration = [3, 3, 3, 1, 2, 6, 1, 1]
    reset_kpi_weight_button = st.button("Reset")

    if KPI_page == "Loneliness":
        if reset_kpi_weight_button:
            index = 0
            for key in Loneliness_kpi_dict.keys():
                Loneliness_kpi_dict[key] = st.select_slider(
                'Explanation',
                options=['1', '2', '3', '4', '5', '6', '7'],
                value=(f'{current_ration[index]}'))
                index += 1
        else:
            index = 0
            for key in Loneliness_kpi_dict.keys():
                Loneliness_kpi_dict[key] = st.select_slider(
                    'Explanation',
                    options=['1', '2', '3', '4', '5', '6', '7'],
                    value=(f'{current_ration[index]}'))
                index += 1
            sum_of_weights = sum(Loneliness_kpi_dict.values())

    elif KPI_page == "Health":
        pass
    elif KPI_page == "Economic Strength":
        pass
