import streamlit as st
import time
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from background_img.background_img import set_png_as_page_bg
from login_page import loginn
from PIL import Image
import pydeck
import math
from functioned import *
from prediction import *

st.set_page_config(page_title="SoCity", page_icon="background_img/favicon.ico" ,layout="wide")
# set_png_as_page_bg('background_img/3_background_img_1920_1080.png')
set_png_as_page_bg('background_img/Simple Cute Desktop Wallpapers - WallpaperSafari.png')
# st.set_page_config(page_title='SoCity', layout = 'wide', page_icon = building, initial_sidebar_state = 'auto')
# st.set_page_config(
#         page_title="Hello world",
#         page_icon="chart_with_upwards_trend",
#         layout="wide",
#     )


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


login_icon = st.container()

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


def header(name):
    st.markdown(f'<p style="color: #8F2A2A; font-size: 20px; font-family: Cooper Black;"> {name} </p>',
                unsafe_allow_html=True)

def update_session_state(key, value):
    del st.session_state[key]
    st.session_state[key] = value

def main():
    with st.sidebar:
        choose = option_menu("SoCity", ["File Upload", "Social KPI", "Prediction", "About"],
                             icons=['upload', 'sliders', 'kanban', 'person lines fill'],

                             menu_icon="building", default_index=0,
    #                          bi bi-building
    #                          app-indicator
                             styles={
                                 "container": {"padding": "5!important", "background-color": "white"},
                                 "icon": {"color": "black", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#FF4B4B"},
                             }
                             )
    if 'flag' not in st.session_state:
        st.session_state['flag'] = False

    if choose == "File Upload":
    #     uploaded_file = None
        with about_header:
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">The File Upload section</p>', unsafe_allow_html=True)
            st.text("Team GABOT")
            uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'], key="uploaded_file")
            if uploaded_file is not None:
                st.session_state['flag'] = True
                with st.spinner('Working on your file, just a sec..'):
    #                 time.sleep(20)
    #             df = pd.read_csv(uploaded_file)
                    df, raw_df = rawToValCatagorized(uploaded_file)
                    st.session_state['raw_df'] = raw_df
                    df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
                    loneliness_dict, health_dict, economic_strength_dict = {}, {}, {}
                    loneliness_dict, health_dict, economic_strength_dict = default_weights(df, loneliness_dict, health_dict, economic_strength_dict)
                    st.session_state['loneliness_dict'] = loneliness_dict
                    st.session_state['health_dict'] = health_dict
                    st.session_state['economic_strength_dict'] = economic_strength_dict

                    df_scored, df_knn = MetricsCalc(raw_df, df, loneliness_dict, health_dict, economic_strength_dict, False, True)
#                     st.write(df_scored)
                    map_df = addAggMetrics(df_scored)
                    
                    df_scored.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)

                    st.session_state['df_scored'] = df_scored
                    st.session_state['df_knn'] = df_knn
                    st.session_state['map_df'] = map_df

                #     global map_df
#                     map_df = df_scored[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
                    

                st.success("File was uploaded!")
  
            else:
                st.session_state['flag'] = False

    elif choose == "Social KPI" and st.session_state['flag'] is False:
        with kpi_header:
    #         st.title("The visualization of our KPI's")
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">The visualization of our KPIs</p>', unsafe_allow_html=True)

        st.error("You didn't upload a CSV file. please go back to 'File Upload' section!")

    elif choose == "Social KPI" and st.session_state['flag'] is True:
        with kpi_header:
    #         st.title("The visualization of our KPI's")
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">The visualization of our KPIs</p>', unsafe_allow_html=True)
            st.write("An unfortunate phenomenon that has been occurring is reports by neighbors of bad smells coming from apartments, resulting in the discovery of lonely elderlies who have died in their homes.")
            st.write("In this project we wish to reduce the number of these sad cases by using data to indicate households in risk. \nDuring the project we came to an understanding that this situation is a combination of three social KPI’s which are Loneliness, health and economic strength.")
            st.write("By the data provided for us from the “HAMAL”, we were able to establish metrics to calculate these KPI’s. \nOn this view we give you the opportunity to control the weight of each metric’s parameters, so you can observe how much it has affected the social KPI's.")

            with kpi_selection:
                header("KPI Selection")
                KPI_names = ["Loneliness", "Health", "Economic Strength"]
                KPI_page = st.radio("", KPI_names)


            with kpi_weights:
                header("KPI weights")

                if KPI_page == "Loneliness":
                    even_col, odd_col = st.columns(2)
                    index = 0
                    temp_col = even_col
                    loneliness_dict = st.session_state['loneliness_dict']
                    min_val = min(filter(lambda x: x > 0, list(loneliness_dict.values())))
    #                 st.write(min_val)

                    for key, val in loneliness_dict.items():
                        loneliness_dict[f"{key}"] = round(round(val/min_val, 3))
    #                     loneliness_dict[f"{key}"] = round(val*10, 3)
                    loneliness_hebrew_dict={'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                            'members_Water_score':('מספר נפשות במשק בית', 'הסבר על המדד'),
                                            'martial_score':('סטטוס משפחתי של ראש משק הבית', 'הסבר על המדד'),
                                            'widow_grown_score':('מספר אלמנים מבוגרים באזור סטטיסטי', 'הסבר על המדד'),
                                            'widow_elderlies_score':('מספר אלמנים זקנים באזור סטטיסטי', 'הסבר על המדד'),
                                            'lonely_elderlies_score':('מספר מבוגרים בודדים באזור סטטיסטי', 'הסבר על המדד'),
                                            'p85_plus_score':('מספר בני 85 ומעלה באזור סטטיסטי', 'הסבר על המדד'),
                                            'accumulated_cases_score':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                            'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                            'area_per_person_score':('שטח לאדם במשק בית', 'הסבר על המדד'),
                                            'Ownership_score':('סוג בעלות על הדירה (שכירות/בעלות)', 'הסבר על המדד')
                                           }
                    curr_loneliness_dict = loneliness_dict.copy()
                    for key, val in curr_loneliness_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_loneliness_dict[f'{key}'] = temp_col.select_slider(f'{loneliness_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Loneliness_slider_{key}', help=f'{loneliness_hebrew_dict[key][1]}')
                            index += 1

                    sum_of_weights = round(sum(list(curr_loneliness_dict.values())), 3)
    #                 st.write(sum_of_weights)
                    loneliness_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_loneliness_dict.items()}
    #                 update_session_state("loneliness_dict", loneliness_dict)
                    st.session_state['loneliness_dict'] = loneliness_dict
 
                    curr_df = MetricsCalc(st.session_state['raw_df'], st.session_state['df_scored'], loneliness_dict, st.session_state['health_dict'], st.session_state['economic_strength_dict'], True, False)
                    st.session_state['df_scores'] = curr_df
                    map_df = addAggMetrics(curr_df)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        
                    R_color_AVG, G_color_AVG, R_color_STRCT, G_color_STRCT = [], [], [], []
                    num_of_rows = map_df.shape[0]
#                     num_of_rows_range = [i for i in range(num_of_rows)]
#                     st.write(map_df)
                    for avg in list(map_df["Loneliness_score_AVG"]):
                        avg = round(avg)
                        if avg == 1:
                            R_color_AVG.append(44)
                            G_color_AVG.append(186)
                        elif avg == 2:
                            R_color_AVG.append(163)
                            G_color_AVG.append(255)
                        elif avg == 3:
                            R_color_AVG.append(255)
                            G_color_AVG.append(244)
                        elif avg == 4:
                            R_color_AVG.append(255)
                            G_color_AVG.append(167)
                        elif avg == 5:
                            R_color_AVG.append(255)
                            G_color_AVG.append(0)
                   
                    for strct in list(map_df["Loneliness_score_STRCT"]):
                        if strct == 1:
                            R_color_STRCT.append(44)
                            G_color_STRCT.append(186)
                        elif strct == 2:
                            R_color_STRCT.append(163)
                            G_color_STRCT.append(255)
                        elif strct == 3:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(244)
                        elif strct == 4:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(167)
                        elif strct == 5:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(0)

    #                 map_df["R_color"] = R_color
    #                 map_df["G_color"] = G_color
    #                 st.session_state["R_color"] = R_color
    #                 st.session_state["G_color"] = G_color
                    
                    
#                     map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
#                     st.write(R_color_AVG, num_of_rows)
                    map_df["R_color_AVG"] = R_color_AVG # st.session_state["R_color"]
                    map_df["G_color_AVG"] = G_color_AVG # st.session_state["G_color"]  
                    map_df["R_color_STRCT"] = R_color_STRCT # st.session_state["R_color"]
                    map_df["G_color_STRCT"] = G_color_STRCT # st.session_state["G_color"]    
    #                 update_session_state("map_df", map_df)
                    st.session_state['map_df'] = map_df

                    WORST = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Loneliness_score_STRCT",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_STRCT", "G_color_STRCT", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    AVERAGE = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Loneliness_score_AVG",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_AVG", "G_color_AVG", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    tooltip_AVG = {
                        "html": "<b>Loneliness KPI (Average) = math.round({Loneliness_score_AVG})</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }
                    tooltip_STRCT = {
                        "html": "<b>Loneliness KPI (Worst) = {Loneliness_score_STRCT}</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }

                    view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                    view.pitch = 75
                    view.bearing = 60
                    view.zoom = 14
                    
                    layer, tooltip = "", ""
                    option = st.selectbox('Choose the Layer?',('Loneliness AVERAGE score per building', 'Loneliness WORST score per building'))
                    if option == 'Loneliness AVERAGE score per building':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    else: 
                        layer = WORST 
                        tooltip = tooltip_STRCT
                        
                    r = pydeck.Deck(
                        layer,
                        initial_view_state=view,
                        tooltip=tooltip,
                        map_provider="mapbox",
                        map_style=pydeck.map_styles.SATELLITE,
                    )
                    
                    st.pydeck_chart(r)

                elif KPI_page == "Health":
                    even_col, odd_col = st.columns(2)
                    index = 0
                    temp_col = even_col
                    health_dict = st.session_state['health_dict']
                    min_val = min(filter(lambda x: x > 0, list(health_dict.values())))
    #                 st.write(min_val)
                    for key, val in health_dict.items():
                        health_dict[f"{key}"] = round(round(val/min_val, 3))
    #                     loneliness_dict[f"{key}"] = round(val*10, 3)
                    health_hebrew_dict={'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                        'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                        'hashlama_kizvat_nechut_elderlies_score':('מספר מקבלי השלמה לקצבת נכות לאזרח ותיק באזור סטטיסטי', 'הסבר על המדד'),
                                        'Mekabley_kizbaot_nechut_score':('מספר מקבלי קיצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                        'zachaim_kizbat_nechut_children_score':('מספר ילדים הזכאים לקצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                        'mekabley_kizbaot_from_injured_Work_score':('מספר מקבלי קיצבת תאונות עבודה באזור סטטיסטי', 'הסבר על המדד'),
                                        'mekabley_kizba_siud_score':('מספר מקבלי קצבת סיעוד באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_cases_score':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_recoveries_score':('סה"כ מקרי הבראה מקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_hospitalized_score':('סה"כ מקרי התאשפזות בעקבות קורונה באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_vaccination_first_dose_score':('סה"כ כמות מתחסנים בחיסון ראשון באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_vaccination_second_dose_score':('סה"כ כמות מתחסנים בחיסון שני באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_vaccination_third_dose_score':('סה"כ כמות מתחסנים בחיסון שלישי באזור סטטיסטי', 'הסבר על המדד')
                                       }
                    curr_health_dict = health_dict.copy()
                    for key, val in curr_health_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_health_dict[f'{key}'] = temp_col.select_slider(f'{health_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Health_slider_{key}', help=f'{health_hebrew_dict[key][1]}')
    #                         curr_loneliness_dict[f'{key}'] = temp_col.slider(f'loneliness_slider: {key}', min_value=0.0, max_value=10.0,
    #                                                                     value=val, key=f'loneliness_slider_{key}')
                            index += 1

                    sum_of_weights = round(sum(list(curr_health_dict.values())), 3)
    #                 st.write(sum_of_weights)
                    health_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_health_dict.items()}
    #                 update_session_state("loneliness_dict", loneliness_dict)
                    st.session_state['health_dict'] = health_dict
    #                 map_df = get_map_df()
    #                 GUI_tuple = ("L", loneliness_dict)            
    #                 loneliness_dict = weights_update(GUI_tuple)
    #                 st.write(st.session_state['df_scored'])
                    curr_df = MetricsCalc(st.session_state['raw_df'], st.session_state['df_scored'], st.session_state['health_dict'], health_dict, st.session_state['economic_strength_dict'], True, False)
                    st.session_state['df_scores'] = curr_df
                    map_df = addAggMetrics(curr_df)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        
                    R_color_AVG, G_color_AVG, R_color_STRCT, G_color_STRCT = [], [], [], []
                    num_of_rows = map_df.shape[0]
#                     num_of_rows_range = [i for i in range(num_of_rows)]
#                     st.write(map_df)
                    for avg in list(map_df["Health_score_AVG"]):
                        avg = round(avg)
                        if avg == 1:
                            R_color_AVG.append(44)
                            G_color_AVG.append(186)
                        elif avg == 2:
                            R_color_AVG.append(163)
                            G_color_AVG.append(255)
                        elif avg == 3:
                            R_color_AVG.append(255)
                            G_color_AVG.append(244)
                        elif avg == 4:
                            R_color_AVG.append(255)
                            G_color_AVG.append(167)
                        elif avg == 5:
                            R_color_AVG.append(255)
                            G_color_AVG.append(0)
                   
                    for strct in list(map_df["Health_score_STRCT"]):
                        if strct == 1:
                            R_color_STRCT.append(44)
                            G_color_STRCT.append(186)
                        elif strct == 2:
                            R_color_STRCT.append(163)
                            G_color_STRCT.append(255)
                        elif strct == 3:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(244)
                        elif strct == 4:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(167)
                        elif strct == 5:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(0)

    #                 map_df["R_color"] = R_color
    #                 map_df["G_color"] = G_color
    #                 st.session_state["R_color"] = R_color
    #                 st.session_state["G_color"] = G_color
                    
                    
#                     map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
#                     st.write(R_color_AVG, num_of_rows)
                    map_df["R_color_AVG"] = R_color_AVG # st.session_state["R_color"]
                    map_df["G_color_AVG"] = G_color_AVG # st.session_state["G_color"]  
                    map_df["R_color_STRCT"] = R_color_STRCT # st.session_state["R_color"]
                    map_df["G_color_STRCT"] = G_color_STRCT # st.session_state["G_color"]    
    #                 update_session_state("map_df", map_df)
                    st.session_state['map_df'] = map_df

                    WORST = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Health_score_STRCT",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_STRCT", "G_color_STRCT", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    AVERAGE = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Health_score_AVG",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_AVG", "G_color_AVG", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    tooltip_AVG = {
                        "html": "<b>Health KPI (Average) = math.round({Health_score_AVG})</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }
                    tooltip_STRCT = {
                        "html": "<b>Health KPI (Worst) = {Health_score_STRCT}</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }

                    view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                    view.pitch = 75
                    view.bearing = 60
                    view.zoom = 14
                    
                    layer, tooltip = "", ""
                    option = st.selectbox('Choose the Layer?',('Health AVERAGE score per building', 'Health WORST score per building'))
                    if option == 'Health AVERAGE score per building':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    else: layer = WORST, tooltip = tooltip_STRCT
                        
                    r = pydeck.Deck(
                        layer,
                        initial_view_state=view,
                        tooltip=tooltip,
                        map_provider="mapbox",
                        map_style=pydeck.map_styles.SATELLITE,
                    )
                    st.pydeck_chart(r)

                elif KPI_page == "Economic Strength":
                    even_col, odd_col = st.columns(2)
                    index = 0
                    temp_col = even_col
                    economic_strength_dict = st.session_state['economic_strength_dict']
                    min_val = min(filter(lambda x: x > 0, list(economic_strength_dict.values())))
    #                 st.write(min_val)
                    for key, val in economic_strength_dict.items():
                        economic_strength_dict[f"{key}"] = round(round(val/min_val, 3))
    #                     loneliness_dict[f"{key}"] = round(val*10, 3)
                    economic_strength_hebrew_dict={'area_per_person_score':('שטח לאדם במשק בית', 'הסבר על המדד'),
                                                    'socio_economic_score':('ציון סוציו אקונומי', 'הסבר על המדד'),
                                                    'mekabley_kizba_siud_score':('מספר מקבלי קצבת סיעוד באזור סטטיסטי', 'הסבר על המדד'),
                                                    'mekabley_kizbaot_from_injured_Work_score':('מספר מקבלי קיצבת תאונות עבודה באזור סטטיסטי', 'הסבר על המדד'),
                                                    'zachaim_kizbat_nechut_children_score':('מספר ילדים הזכאים לקצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                                    'Mekabley_kizbaot_nechut_score':('מספר מקבלי קיצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                                    'Mekabley_mezonot_score':('מספר מקבלי מזונות באזור סטטיסטי', 'הסבר על המדד'),
                                                    'Hashlamat_hachnasa_sheerim_family_score':('מספר מקבלי השלמת הכנסה שארים באזור סטטיסטי', 'הסבר על המדד'),
                                                    'hashlama_kizvat_nechut_elderlies_score':('מספר מקבלי השלמה לקצבת נכות לאזרח ותיק באזור סטטיסטי', 'הסבר על המדד'),
                                                    'hashlamta_hachnasa_family_eldelies_score':('מספר מקבלי השלמת הכנסה מבוגרים במשפחה באזור סטטיסטי', 'הסבר על המדד'),
                                                    'mekabley_kizva_elderlies_score':('מספר מקבלי קצבת זקנה באזור סטטיסטי', 'הסבר על המדד'),
                                                    'avtachat_hachansa_family_score':('מספר מקבלי הבטחת הכנסה משפחות באזור סטטיסטי', 'הסבר על המדד'),
                                                    'income_per_person_score':('סך הכל הכנסה פר נפש במשק בית', 'הסבר על המדד'),
                                                    'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                                    'Ownership_score':('סוג בעלות על הדירה (שכירות/בעלות)', 'הסבר על המדד'),
                                                    'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                                    'martial_score':('סטטוס משפחתי של ראש משק הבית', 'הסבר על המדד'),
                                                    'members_Water_score':('מספר נפשות במשק בית', 'הסבר על המדד'),
                                                    'near_106_pizul_and_dangerous_buildings_score':('בניין שנמצא במרחק של עד 25 מטר מבניין מסוכן או בניין שעבר פיצול', 'הסבר על המדד')
                                                  }
                    curr_economic_strength_dict = economic_strength_dict.copy()
                    for key, val in curr_economic_strength_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_economic_strength_dict[f'{key}'] = temp_col.select_slider(f'{economic_strength_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Economic_Strength_slider_{key}', help=f'{economic_strength_hebrew_dict[key][1]}')
    #                         curr_loneliness_dict[f'{key}'] = temp_col.slider(f'loneliness_slider: {key}', min_value=0.0, max_value=10.0,
    #                                                                     value=val, key=f'loneliness_slider_{key}')
                            index += 1

                    sum_of_weights = round(sum(list(curr_economic_strength_dict.values())), 3)
    #                 st.write(sum_of_weights)
                    economic_strength_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_economic_strength_dict.items()}
    #                 update_session_state("loneliness_dict", loneliness_dict)
                    st.session_state['economic_strength_dict'] = economic_strength_dict
    #                 map_df = get_map_df()
    #                 GUI_tuple = ("L", loneliness_dict)            
    #                 loneliness_dict = weights_update(GUI_tuple)
    #                 st.write(st.session_state['df_scored'])
                    curr_df = MetricsCalc(st.session_state['raw_df'], st.session_state['df_scored'], st.session_state['loneliness_dict'], st.session_state['health_dict'], economic_strength_dict, True, False)
                    st.session_state['df_scores'] = curr_df
                    map_df = addAggMetrics(curr_df)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        
                    R_color_AVG, G_color_AVG, R_color_STRCT, G_color_STRCT = [], [], [], []
                    num_of_rows = map_df.shape[0]
#                     num_of_rows_range = [i for i in range(num_of_rows)]
#                     st.write(map_df)
                    for avg in list(map_df["Economic_Strength_score_AVG"]):
                        avg = round(avg)
                        if avg == 1:
                            R_color_AVG.append(44)
                            G_color_AVG.append(186)
                        elif avg == 2:
                            R_color_AVG.append(163)
                            G_color_AVG.append(255)
                        elif avg == 3:
                            R_color_AVG.append(255)
                            G_color_AVG.append(244)
                        elif avg == 4:
                            R_color_AVG.append(255)
                            G_color_AVG.append(167)
                        elif avg == 5:
                            R_color_AVG.append(255)
                            G_color_AVG.append(0)
                   
                    for strct in list(map_df["Economic_Strength_score_STRCT"]):
                        if strct == 1:
                            R_color_STRCT.append(44)
                            G_color_STRCT.append(186)
                        elif strct == 2:
                            R_color_STRCT.append(163)
                            G_color_STRCT.append(255)
                        elif strct == 3:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(244)
                        elif strct == 4:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(167)
                        elif strct == 5:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(0)

    #                 map_df["R_color"] = R_color
    #                 map_df["G_color"] = G_color
    #                 st.session_state["R_color"] = R_color
    #                 st.session_state["G_color"] = G_color
                    
                    
#                     map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
#                     st.write(R_color_AVG, num_of_rows)
                    map_df["R_color_AVG"] = R_color_AVG # st.session_state["R_color"]
                    map_df["G_color_AVG"] = G_color_AVG # st.session_state["G_color"]  
                    map_df["R_color_STRCT"] = R_color_STRCT # st.session_state["R_color"]
                    map_df["G_color_STRCT"] = G_color_STRCT # st.session_state["G_color"]    
    #                 update_session_state("map_df", map_df)
                    st.session_state['map_df'] = map_df

                    WORST = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Economic_Strength_score_STRCT",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_STRCT", "G_color_STRCT", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    AVERAGE = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        map_df,
                        get_position=['lon', 'lat'],
                        get_elevation="Economic_Strength_score_AVG",
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["R_color_AVG", "G_color_AVG", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
                    tooltip_AVG = {
                        "html": "<b>Economic Strength KPI (Average) = round({Economic_Strength_score_AVG})</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }
                    tooltip_STRCT = {
                        "html": "<b>Economic Strength KPI (Worst) = {Economic_Strength_score_STRCT}</b>",
                        "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                    }

                    view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                    view.pitch = 75
                    view.bearing = 60
                    view.zoom = 14
                    
                    layer, tooltip = "", ""
                    option = st.selectbox('Choose the Layer?',('Economic Strength AVERAGE score per building', 'Economic Strength WORST score per building'))
                    if option == 'Economic Strength AVERAGE score per building':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    else: layer = WORST, tooltip = tooltip_STRCT
                        
                    r = pydeck.Deck(
                        layer,
                        initial_view_state=view,
                        tooltip=tooltip,
                        map_provider="mapbox",
                        map_style=pydeck.map_styles.SATELLITE,
                    )
                    st.pydeck_chart(r)

    elif choose == "Prediction" and st.session_state['flag'] is False:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The Prediction section</p>', unsafe_allow_html=True)
        
        st.error("You didn't upload a CSV file. please go back to 'File Upload' section!")
        
    elif choose == "Prediction" and st.session_state['flag'] is True:
    #     st.balloons()
    #     st.title("The Prediction section")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The Prediction section</p>', unsafe_allow_html=True)
#         knn_file = st.file_uploader("Choose a CSV file for KNN", type=['csv'], key="knn_file")
        new_file = st.file_uploader("Choose a new CSV file for prediction", type=['csv'], key="new_file")
        if new_file is not None:
            new_df = pd.read_csv(new_file)
            st.session_state['new_df'] = new_df
            st.success("File was uploaded!")

#             st.write(new_df)
#             st.write(st.session_state['df_knn'])
#         if st.button('Predict!'):

            with st.spinner('Predicting for you, it may take a few minutes to complete..'):
                perc_risk, df_risk = prediction_main(st.session_state['df_knn'], new_df)
#                 col1, col2, col3 = st.columns(3)
#                 col1.subheader("")
#                 col2.subheader("Households which are under risk")
#                 col2.metric(label="", value=f'{round(perc_risk,3)}%')
#                 col3.subheader("")
#                 st.metric(label="Households which are under risk", value=f'{round(perc_risk,3)}%')
                st.title(f'{round(perc_risk,3)}% of the households are under risk')
                
                st.dataframe(df_risk)

                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')

                csv = convert_df(df_risk)
                st.download_button(
                     label="Download the predicted data as CSV",
                     data=csv,
                     file_name='Prediction.csv',
                     mime='text/csv',
                    )


    elif choose == "About":
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
    #     st.markdown(""" <style> .font {
    #     font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
    #     </style> """, unsafe_allow_html=True)
    #     st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    #     with st.form(key='columns_in_form2', clear_on_submit=True):  # clear_on_submit=True > form will be reset/cleared once it's submitted
    #         Name = st.text_input(label='Please Enter Your Name')  # Collect user feedback
    #         Email = st.text_input(label='Please Enter Email')  # Collect user feedback
    #         Message = st.text_input(label='Please Enter Your Message')  # Collect user feedback
    #         submitted = st.form_submit_button('Submit')
    #         if submitted:
    #             st.write('Thanks for your contacting us. \nWe will respond to your questions or inquiries as soon as possible! \n   Team GABOT')
    
# def St_login():
#     name, authentication_status, authenticator = login()
#     login_stat = True
# #     st.write(authentication_status)

#     st.warning('Please enter your username and password')

#     if authentication_status:
#         authenticator.logout('Logout', 'main')
#         st.sidebar.write('Welcome *%s*' % (name))
#         main()  
#     elif authentication_status == False:
#         st.error('Username/Password is incorrect')
#     elif authentication_status == None:
#         st.warning('Please enter your username and password')


# streamlit_app.py

def check_password():  
#     """Returns `True` if the user had a correct password."""
#     def login_page_only():
#         col_1, col_2, col_3 = st.columns(3)
#         with col_1:
#             st.write("")

#         with col_2:
#             image = Image.open('background_img/login_page_icon.png')
#             st.image(image)

#         with col_3:
#             st.write("")
#         st.info('Please enter Username and Password')
    def password_entered():
#         """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.write("")

        with col_2:
            image = Image.open('background_img/login_page_icon.png')
            st.image(image)

        with col_3:
            st.write("")
        st.info('Please enter Username and Password')
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
#         is_register = st.button("Submit")
#         if is_register:
    # Password Incorrect.
        return False
    elif not st.session_state["password_correct"]:
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.write("")

        with col_2:
            image = Image.open('background_img/login_page_icon.png')
            st.image(image)

        with col_3:
            st.write("")
        st.info('Please enter Username and Password')
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
#         is_register = st.button("Submit")
#         if is_register:
    # Password Incorrect.
        st.error("Username/Password is incorrect 😕")
        return False
    else:
#         if is_register:
    # Password correct.
        return True

# if check_password():
#     st.write("Here goes your normal Streamlit app...")
#     st.button("Click me")




if __name__ == "__main__":
#     St_login()
#     main()
    
#     name, authentication_status, username, authenticator = loginn()
# # #     login_stat = True
# # #     st.write(authentication_status)
#     if authentication_status:
#         authenticator.logout('Logout', 'main')
#         st.sidebar.write('Welcome *%s*' % (name))
#         main()
#     elif authentication_status == False:
#         st.error('Username/Password is incorrect')
#     elif authentication_status == None:
#         st.warning('Please enter your username and password')  
    if check_password():
#         st.write("Here goes your normal Streamlit app...")
#         st.button("Click me")
        main()
        
#         st.subheader("Register")
#         with st.expander("Registering"):
#             name_register = st.text_input("Your name")
#             user_name_register = st.text_input("User name")
#             password_register = st.text_input("Password", type="password")
#             is_register = st.button("Submit")
#             if is_register:
#                 register_user(user_name_register, password_register, name_register)
