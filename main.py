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
    st.session_state[f"{kpi_name}"] = value



# st.sidebar.slider("My slider", key="test_slider", min_value=-100, max_value=100)

# st.button("Update slider values", on_click=_update_slider, kwargs={"value": random.randint(-100, 100)})

# with st.sidebar:
#     # st.sidebar
#     # options_names = ["Prediction", "KPI"]
#     # choose_page = st.radio("Choose", options_names)
#
#     choose = option_menu("App Gallery", ["About", "Prediction", "Social KPI", "Contact"],
#                          icons=['person lines fill', 'pc display horizontal', 'people', 'pencil square'],
#                          menu_icon="app-indicator", default_index=0,
#                          styles={
#                              "container": {"padding": "5!important", "background-color": "orange"},
#                              "icon": {"color": "black", "font-size": "25px"},
#                              "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
#                                           "--hover-color": "#eee"},
#                              "nav-link-selected": {"background-color": "#02ab21"},
#                          }
#                          )

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
    # Loneliness_sliders = [st.slider("arnona_cat", 0.0, 1.0, Loneliness_default_values[0]),
    #                       st.slider("members_Water", 0.0, 1.0, Loneliness_default_values[1]),
    #                       st.slider("martial", 0.0, 1.0, Loneliness_default_values[2]),
    #                       st.slider("widow_grown", 0.0, 1.0, Loneliness_default_values[3]),
    #                       st.slider("widow_elderlies", 0.0, 1.0, Loneliness_default_values[4]),
    #                       st.slider("lonely_elderlies", 0.0, 1.0, Loneliness_default_values[5]),
    #                       st.slider("p85_plus", 0.0, 1.0, Loneliness_default_values[6]),
    #                       st.slider("accumulated_cases", 0.0, 1.0, Loneliness_default_values[7])]
    if KPI_page == "Loneliness":
        Loneliness_kpi_names = ["arnona_cat", "members_Water", "martial", "widow_grown", "widow_elderlies", "lonely_elderlies", "p85_plus",
                       "accumulated_cases"]
        arnona_cat = st.slider("arnona_cat", 0.0, 1.0, key="arnona_cat")
        members_Water = st.slider("members_Water", 0.0, 1.0, key="members_Water")
        martial = st.slider("martial", 0.0, 1.0, key="martial")
        widow_grown = st.slider("widow_grown", 0.0, 1.0, key="widow_grown")
        widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, key="widow_elderlies")
        lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, key="lonely_elderlies")
        p85_plus = st.slider("p85_plus", 0.0, 1.0, key="p85_plus")
        accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, key="accumulated_cases")

        for kpi_name in Loneliness_kpi_names:
            if f"{kpi_name}" not in st.session_state:
                st.session_state[f"{kpi_name}"] = 0
        
        if arnona_cat != current_values[0]:
            diff_val = round(arnona_cat - current_values[0], 4)
            avg_diff = round(diff_val/7, 4) # בכמה לשנות כל משקל
            current_values[0] = arnona_cat
            st.write(diff_val, "--", avg_diff)

            if diff_val > 0:
                for i in range(8):
                    if i != 0:
                        current_values[i] = round(current_values[i] - avg_diff, 4)
                        update_slider(Loneliness_kpi_names[i], current_values[i])
                st.write(current_values)

                # arnona_cat = st.slider("arnona_cat", 0.0, 1.0, current_values[0])
                # members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1])
                # martial = st.slider("martial", 0.0, 1.0, current_values[2])
                # widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3])
                # widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4])
                # lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5])
                # p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6])
                # accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7])

            else:
                for i in range(8):
                    if i != 0:
                        current_values[i] = round(current_values[i] + avg_diff, 4)
                        update_slider(Loneliness_kpi_names[i], current_values[i])
                # arnona_cat = st.slider("arnona_cat", 0.0, 1.0, current_values[0])
                # members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1])
                # martial = st.slider("martial", 0.0, 1.0, current_values[2])
                # widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3])
                # widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4])
                # lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5])
                # p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6])
                # accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7])

        # temp_values = [arnona_cat, members_Water, martial, widow_grown, widow_elderlies, lonely_elderlies, p85_plus,
        #                accumulated_cases]
    # loneliness_weights = [["arnona_cat", 0.15], ["members_Water", 0.15], ["martial", 0.15], ["widow_grown", 0.04],
    #                       ["widow_elderlies", 0.1], ["lonely_elderlies", 0.3], ["p85_plus", 0.06],
    #                       ["accumulated_cases", 0.05]]
    elif KPI_page == "Health":
        pass
    elif KPI_page == "Economic Strength":
        pass
    # if loneliness_kpi_button:
    #     arnona_cat = st.slider("arnona_cat", 0.0, 1.0, 0.15)
    #     members_Water = st.slider("members_Water", 0.0, 1.0, 0.15)
    #     martial = st.slider("martial", 0.0, 1.0, 0.15)
    #     widow_grown = st.slider("widow_grown", 0.0, 1.0, 0.04)
    #     widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, 0.1)
    #     lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, 0.3)
    #     p85_plus = st.slider("p85_plus", 0.0, 1.0, 0.06)
    #     accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, 0.05)
    #     # loneliness_weights = [["arnona_cat", 0.15], ["members_Water", 0.15], ["martial", 0.15], ["widow_grown", 0.04],
    #     #                       ["widow_elderlies", 0.1], ["lonely_elderlies", 0.3], ["p85_plus", 0.06],
    #     #                       ["accumulated_cases", 0.05]]
    #
    # elif health_kpi_button:
    #     pass
    # elif economic_strength_kpi_button:
    #     pass
    # elif clear_button:
    #     st.text("In this section you will see all the weights that create the KPI you selected")
