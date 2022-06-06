import streamlit as st
import time
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
# import streamlit.components.v1 as html
from background_img.background_img import set_png_as_page_bg
from PIL import Image
# import cv2
# from st_aggrid import AgGrid
# import plotly.express as px
# import io
st.set_page_config(layout="wide")
set_png_as_page_bg('background_img/3_background_img_1920_1080.png')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

about_header = st.container()
pic_about_header = st.container()
Yuvi_pic = Image.open(r'Team_members_pictures/Yuval.jpeg')
Tal_pic = Image.open(r'Team_members_pictures/Tal.jpeg')
Dana_pic = Image.open(r'Team_members_pictures/Dana.jpeg')
Gal_pic = Image.open(r'Team_members_pictures/Gal.jpeg')
Niv_pic = Image.open(r'Team_members_pictures/Niv.jpeg')

kpi_header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()
Loneliness_default_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]


def header(name):
    st.markdown(f'<p style="color: #8F2A2A; font-size: 20px; font-family: Cooper Black;"> {name} </p>',
                unsafe_allow_html=True)

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

with st.sidebar:
    # st.sidebar
    # options_names = ["Prediction", "KPI"]
    # choose_page = st.radio("Choose", options_names)
#     selectbox('Select page',['Country data','Continent data']) 
    choose = option_menu("GABOT", ["About", "Prediction", "Social KPI", "Contact"],
                         icons=['person lines fill', 'kanban', 'sliders', 'pencil square'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "white"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#FF4B4B"},
                         }
                         )

if choose == "About":
    with about_header:
#         st.title("The About section")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The About section</p>', unsafe_allow_html=True)
        st.text("Team GABOT")
        Yuvi, Tal, Dana, Gal, Niv = st.columns(5)
        with Yuvi:
            st.image(Yuvi_pic, width=130)
        with Tal:
            st.image(Tal_pic, width=130)
        with Dana:
            st.image(Dana_pic, width=130)
        with Gal:
            st.image(Gal_pic, width=130)
        with Niv:
            st.image(Niv_pic, width=130)

elif choose == "Prediction":
#     st.balloons()
#     st.title("The Prediction section")
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">The Prediction section</p>', unsafe_allow_html=True)
    st.text("Here we will predict")

elif choose == "Social KPI":
    with kpi_header:
#         st.title("The visualization of our KPI's")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The visualization of our KPIs</p>', unsafe_allow_html=True)
        st.write("The Loneliness KPI is .....text....")
        st.write("The Health KPI is .....text....")
        st.write("The Economic Strength KPI is .....text....")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv','xls','xlsx'], key="uploaded_file")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
            map_df = df[["lat", "lon"]]
            
#             st.write(dataframe)
#         for uploaded_file in uploaded_files:
#              bytes_data = uploaded_file.read()
#              st.write("filename:", uploaded_file.name)
#              st.write(bytes_data)
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Loneliness KPI:", "2", "-1")
#         col2.metric("Health KPI:", "4", "+1")
#         col3.metric("Economic Strength KPI:", "3", "-1")
#         col1.text("The average loneliness \nlevel of households in \nHadar neighborhood")
#         col2.text("The average health level \nof households in Hadar \nneighborhood")
#         col3.text("The average economic \nstrength level of \nhouseholds in Hadar \nneighborhood")

        with kpi_selection:
            header("KPI Selection")
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
            header("KPI weights")
            current_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
            Loneliness_kpi_dict = {"arnona_cat": 0, "members_Water": 0, "martial": 0, "widow_grown": 0, "widow_elderlies": 0,
                                   "lonely_elderlies": 0, "p85_plus": 0, "accumulated_cases": 0}

            param_dict = ["Arnona discount", "Number of tenants", "Martial status", "Number of older widows per statistical area", "Number of elderly widows per statistical area", "Number of lonely elders per statistical area", "Number of people over the age of 85 per statistical area", "Number of cases of Covid-19 infection per statistical area"]
            basic_ratio = [3, 3, 3, 1, 2, 6, 1, 1]
            current_ratio = [3, 3, 3, 1, 2, 6, 1, 1]

            if KPI_page == "Loneliness":
                even_col, odd_col = st.columns(2)
                # st.balloons()
                Loneliness_kpi_dict_keys = list(Loneliness_kpi_dict.keys())
                index = 0
                temp_col = even_col
                for key in Loneliness_kpi_dict.keys():
                    if index % 2 == 0:
                        temp_col = even_col
                    if index % 2 == 1:
                        temp_col = odd_col
                    Loneliness_kpi_dict[key] = temp_col.select_slider(f'{param_dict[index]}', options=[1, 2, 3, 4, 5, 6, 7],
                                                                value=current_ratio[index], key=Loneliness_kpi_dict_keys[index])
                    index += 1

                sum_of_weights = round(sum(list(Loneliness_kpi_dict.values())), 5)
                st.write(sum_of_weights)
                Loneliness_weights_dict = {key: round(weight/sum_of_weights, 5) for key, weight in Loneliness_kpi_dict.items()}
                st.write(Loneliness_weights_dict)
                st.map(map_df, zoom=13)
                st.pydeck_chart(pdk.Deck(
                     map_style='mapbox://styles/mapbox/light-v9',
                     initial_view_state=pdk.ViewState(
                         latitude=37.76,
                         longitude=-122.4,
                         zoom=11,
                         pitch=50,
                     ),
                     layers=[
                         pdk.Layer(
                            'HexagonLayer',
                            data=df,
                            get_position='[lon, lat]',
                            radius=200,
                            elevation_scale=4,
                            elevation_range=[0, 1000],
                            pickable=True,
                            extruded=True,
                         ),
                         pdk.Layer(
                             'ScatterplotLayer',
                             data=df,
                             get_position='[lon, lat]',
                             get_color='[200, 30, 0, 160]',
                             get_radius=200,
                         ),
                     ],
                 ))
                # get df from model.py after multiply it by the new weights and group by it by statistical area (average) 
                # st.table(df)

            elif KPI_page == "Health":
                st.title("Working on it")
                # st.snow()
                # my_bar = st.progress(0)
                # for percent_complete in range(100):
                #     time.sleep(0.1)
                #     my_bar.progress(percent_complete + 1)
            elif KPI_page == "Economic Strength":
                # st.balloons()
                st.write("Not Economic Strength")
                Loneliness_kpi_dict_keys = list(Loneliness_kpi_dict.keys())
                index = 0
                for key in Loneliness_kpi_dict.keys():
                    Loneliness_kpi_dict[key] = st.select_slider('Explanation', options=[1, 2, 3, 4, 5, 6, 7],
                                                                value=current_ratio[index],
                                                                key=Loneliness_kpi_dict_keys[index])
                    index += 1

                sum_of_weights = round(sum(list(Loneliness_kpi_dict.values())), 5)
                st.write(sum_of_weights)
                Loneliness_weights_dict = {key: round(weight / sum_of_weights, 5) for key, weight in
                                           Loneliness_kpi_dict.items()}
                st.write(Loneliness_weights_dict)
                # with st.spinner('Exporting File..'):
                #     time.sleep(3)
                # st.success('Done!')

            # health_weights = [["arnona_cat", 0.2], ["age", 0.08], ["hashlama_kizvat_nechut_elderlies", (-2) * 0.08],
            #                   ["Mekabley_kizbaot_nechut", (-2) * 0.1], ["zachaim_kizbat_nechut_children", (-2) * 0.09],
            #                   ["mekabley_kizbaot_from_injured_Work", (-2) * 0.11], ["mekabley_kizba_siud", (-2) * 0.15],
            #                   ["accumulated_cases", 0.05], ["accumulated_recoveries", (-2) * 0.01],
            #                   ["accumulated_hospitalized", (-2) * 0.07], ["accumulated_vaccination_first_dose", (-2) * 0.02],
            #                   ["accumulated_vaccination_second_dose", (-2) * 0.02],
            #                   ["accumulated_vaccination_third_dose", (-2) * 0.02]]
            # economic_strength_weights = [["Ownership", 0.35], ["arnona_cat", 0.1], ["income_per_person", 0.2],
            #                              ["avtachat_hachansa_family", 0.022], ["mekabley_kizva_elderlies", 0.022],
            #                              ["hashlamta_hachnasa_family_eldelies", 0.022],
            #                              ["hashlama_kizvat_nechut_elderlies", 0.022],
            #                              ["Hashlamat_hachnasa_sheerim_family", 0.022], ["Mekabley_mezonot", 0.022],
            #                              ["Mekabley_kizbaot_nechut", 0.022], ["zachaim_kizbat_nechut_children", 0.022],
            #                              ["mekabley_kizbaot_from_injured_Work", 0.022], ["mekabley_kizba_siud", 0.022],
            #                              ["socio_economic", 0.1], ["area_per_person", 0.03]]

            #     st.text("In this section you will see all the weights that create the KPI you selected")

elif choose == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2', clear_on_submit=True):  # clear_on_submit=True > form will be reset/cleared once it's submitted
        Name = st.text_input(label='Please Enter Your Name')  # Collect user feedback
        Email = st.text_input(label='Please Enter Email')  # Collect user feedback
        Message = st.text_input(label='Please Enter Your Message')  # Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. \nWe will respond to your questions or inquiries as soon as possible! \n   Team GABOT')
