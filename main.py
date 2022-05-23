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
    elif sign == -1:
        return count_negatives
    else:
        return count_zeros + count_negatives


# def increase_one_kpi(kpi_name, decrease_val, kpis_dict):
#     diff_dict = {key: 0 for key in kpis_dict.keys()}
#     for key, val in kpis_dict.items():
#         diff_dict[key] = val - decrease_val
#     while diff_dict.values() < 0:
#         # max_negative_val = -1
#         # for val in diff_dict.values():
#         #     if val < 0 & val > max_negative_val:
#         #         max_negative_val = val
#         num_of_negatives = count_by_sign(-1)
#         min_negative_val = min(diff_dict.values())
#         diff_avg =
#         for key, val in kpis_dict.items():


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
    Loneliness_kpi_dict = {"arnona_cat": 0, "members_Water": 0, "martial": 0, "widow_grown": 0, "widow_elderlies": 0,
                           "lonely_elderlies": 0, "p85_plus": 0, "accumulated_cases": 0}

    basic_ratio = [3, 3, 3, 1, 2, 6, 1, 1]
    current_ratio = [3, 3, 3, 1, 2, 6, 1, 1]
    reset_kpi_weight_button = st.button("Reset")

    if KPI_page == "Loneliness":
        st.balloons()
        Loneliness_kpi_dict_keys = list(Loneliness_kpi_dict.keys())
        index = 0
        for key in Loneliness_kpi_dict.keys():
            Loneliness_kpi_dict[key] = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
                                                        value=f'{current_ratio[index]}', key=Loneliness_kpi_dict_keys[index])
            index += 1
        # arnona_cat = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                               value=f'{basic_ratio[0]}', key="arnona_cat")
        # members_Water = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                                  value=f'{basic_ratio[1]}', key="members_Water")
        # martial = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                            value=f'{basic_ratio[2]}', key="martial")
        # widow_grown = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                                value=f'{basic_ratio[3]}', key="widow_grown")
        # widow_elderlies = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                                    value=f'{basic_ratio[4]}', key="widow_elderlies")
        # lonely_elderlies = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                                     value=f'{basic_ratio[5]}', key="lonely_elderlies")
        # p85_plus = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                             value=f'{basic_ratio[6]}', key="p85_plus")
        # accumulated_cases = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
        #                                      value=f'{basic_ratio[7]}', key="accumulated_cases")
        if reset_kpi_weight_button:
            current_ratio = basic_ratio.copy()
            # index = 0
            # for key in Loneliness_kpi_dict.keys():
            #     Loneliness_kpi_dict[key] = st.select_slider('Explanation', options=['1', '2', '3', '4', '5', '6', '7'],
            #                                                 value=f'{current_ratio[index]}',
            #                                                 key=Loneliness_kpi_dict_keys[index])
            #     index += 1

        sum_of_weights = sum(Loneliness_kpi_dict.values())
        st.write(sum_of_weights)
        # else:
        #     index = 0
        #     for key in Loneliness_kpi_dict.keys():
        #         Loneliness_kpi_dict[key] = st.select_slider(

    #                                         'Explanation',
    #                                         options=['1', '2', '3', '4', '5', '6', '7'],
    #                                         value=f'{current_ratio[index]}')
    #         index += 1
    #     if current_values == [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]:
    #         Loneliness_kpi_names = ["arnona_cat", "members_Water", "martial", "widow_grown", "widow_elderlies",
    #                                 "lonely_elderlies", "p85_plus", "accumulated_cases"]
    #         arnona_cat = st.slider("arnona_cat", 0.0, 1.0, current_values[0], key="arnona_cat")
    #         members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1], key="members_Water")
    #         martial = st.slider("martial", 0.0, 1.0, current_values[2], key="martial")
    #         widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3], key="widow_grown")
    #         widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4], key="widow_elderlies")
    #         lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5], key="lonely_elderlies")
    #         p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6], key="p85_plus")
    #         accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7], key="accumulated_cases")
    #
    #     # del members_Water
    #     st.write(st.session_state)
    #     # for ind, kpi_name in enumerate(Loneliness_kpi_names):
    #     #     if f"{kpi_name}" not in st.session_state:
    #     #         # st.session_state[f"{kpi_name}"] = Loneliness_default_values[ind]
    #     #         st.session_state.arnona_cat = 0.15
    #
    #     if arnona_cat != current_values[0]:
    #         diff_val = round(arnona_cat - current_values[0], 4)
    #         count = count_by_sign()
    #         avg_diff = round(diff_val / count, 4)  # בכמה לשנות כל משקל
    #         current_values[0] = arnona_cat
    #         st.write(diff_val, "--", avg_diff)
    #
    #         if diff_val > 0:
    #             for i in range(8):
    #                 if i == 0:
    #                     del st.session_state[f"{Loneliness_kpi_names[i]}"]
    #                     arnona_cat = st.slider(f"{Loneliness_kpi_names[i]}", 0.0, 1.0, current_values[i], key=f"{Loneliness_kpi_names[i]}")
    #                 if (i != 0) & (current_values[i] != 0):
    #                     current_values[i] = round(current_values[i] - avg_diff, 4)
    #                     # if current_values[i] < 0:
    #                     #     count = count_non_zeros()
    #                     # update_slider(Loneliness_kpi_names[i], current_values[i])
    #                     del st.session_state[f"{Loneliness_kpi_names[i]}"]
    #             members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1], key="members_Water")
    #             martial = st.slider("martial", 0.0, 1.0, current_values[2], key="martial")
    #             widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3], key="widow_grown")
    #             widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4], key="widow_elderlies")
    #             lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5], key="lonely_elderlies")
    #             p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6], key="p85_plus")
    #             accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7], key="accumulated_cases")
    #
    #
    #         else:
    #             for i in range(8):
    #                 if i == 0:
    #                     del st.session_state[f"{Loneliness_kpi_names[i]}"]
    #                     arnona_cat = st.slider(f"{Loneliness_kpi_names[i]}", 0.0, 1.0, current_values[i],
    #                                            key=f"{Loneliness_kpi_names[i]}")
    #                 if i != 0:
    #                     current_values[i] = round(current_values[i] + avg_diff, 4)
    #                     # update_slider(Loneliness_kpi_names[i], current_values[i])
    #                     del st.session_state[f"{Loneliness_kpi_names[i]}"]
    #             members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1], key="members_Water")
    #             martial = st.slider("martial", 0.0, 1.0, current_values[2], key="martial")
    #             widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3], key="widow_grown")
    #             widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4], key="widow_elderlies")
    #             lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5], key="lonely_elderlies")
    #             p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6], key="p85_plus")
    #             accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7], key="accumulated_cases")
    #
    #     # temp_values = [arnona_cat, members_Water, martial, widow_grown, widow_elderlies, lonely_elderlies, p85_plus,
    #     #                accumulated_cases]
    # # loneliness_weights = [["arnona_cat", 0.15], ["members_Water", 0.15], ["martial", 0.15], ["widow_grown", 0.04],
    # #                       ["widow_elderlies", 0.1], ["lonely_elderlies", 0.3], ["p85_plus", 0.06],
    # #                       ["accumulated_cases", 0.05]]
    elif KPI_page == "Health":
        st.snow()
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
