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
# Utils
import base64 
import time
from datetime import datetime, timedelta
from pytz import timezone
curr_time = time.localtime()
# tz = timezone('Europe/Berlin')
timestr = (datetime.now() + timedelta(hours=3)).strftime("%d%m%Y_%H%M")
# timestr = time.strftime("%d%m%Y_%H%M") + datetime.timedelta(hours=3)

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
Yuvi_pic = Image.open(r'Team_members_pictures/yuval.png')
Tal_pic = Image.open(r'Team_members_pictures/tal.png')
Dana_pic = Image.open(r'Team_members_pictures/dana.png')
Gal_pic = Image.open(r'Team_members_pictures/gal.png')
Niv_pic = Image.open(r'Team_members_pictures/niv2.png')

kpi_header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()

st.session_state["finish_Prediction_flag"] = False


def header(name):
    st.markdown(f'<p style="color: #8F2A2A; font-size: 20px; font-family: Cooper Black;"> {name} </p>',
                unsafe_allow_html=True)

def subheader(name):
    st.markdown(f'<p style="color: #000000; font-family: Calibri; font-size: 16px; "> {name} </p>',
                unsafe_allow_html=True)

def about_home_subheader(name):
    st.markdown(f'<p style="color: #000000; font-family: Calibri; font-size: 18px; "> {name} </p>',
                unsafe_allow_html=True)

def perc_subheader(name):
    st.markdown(f'<p style="color: #000000; font-size: 19px; "> {name} </p>',
                unsafe_allow_html=True)

def update_session_state(key, value):
    del st.session_state[key]
    st.session_state[key] = value

def main():
    with st.sidebar:
        
        image = Image.open('background_img/SoCityFINAL-LOGO_wide.png')
        st.image(image)

        choose = option_menu("SoCity", ["Home", "File Upload", "Social KPIs", "Risk", "Prediction", "About Us"],
                             icons=['house', 'upload', 'sliders','bullseye', 'kanban', 'person lines fill'],

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
    
    if choose == "Home":
    #     uploaded_file = None
        with about_header:
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Home</p>', unsafe_allow_html=True)
            about_home_subheader("In our society where the socio-economic gaps are getting wider, loneliness has become a common phenomenon, and health issues can negatively impact quality of life, many families find themselves struggling to survive.")
            about_home_subheader("<b style='color: #FF4B4B'>SoCity main goal is to enable the authorities to make data-driven decisions about social issues and turn the spotlight on households at risk, so they can help them.</b>")
            about_home_subheader("In this project we collected data from the local authorities in order to calculate social measures for life quality, as defined by “Joint” organization.")
            about_home_subheader("SoCity gives you the opportunity to see those measures on a map, so you can get spatial understanding regarding the population at risk.")
#             subheader("By the data provided for us from the “HAMAL”, we were able to establish metrics to calculate these KPIs. ")
#             subheader("On this view we give you the opportunity to control the weight of each metric’s parameters, ")
#             subheader("so you can observe how much it has affected the social KPI and the Risk.")
            
			
    if choose == "File Upload":
    #     uploaded_file = None
        with about_header:
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">File Upload</p>', unsafe_allow_html=True)
#             st.text("Team GABOT")
            uploaded_file = st.file_uploader("Choose a CSV file to analyze", type=['csv'], key="uploaded_file")
            if uploaded_file is not None:
                st.session_state['flag'] = True
                with st.spinner('Uploading, it may take a few minutes..'):
                    df,raw_df = rawToValCatagorized(uploaded_file)
                    st.session_state['df'] = df
                    st.session_state['raw_df'] = raw_df
                    df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
                    loneliness_dict, health_dict, economic_strength_dict = {}, {}, {}
                    loneliness_dict, health_dict, economic_strength_dict = default_weights(df, loneliness_dict, health_dict, economic_strength_dict)
                    st.session_state['loneliness_dict'] = loneliness_dict
                    st.session_state['health_dict'] = health_dict
                    st.session_state['economic_strength_dict'] = economic_strength_dict

                    df_scored, df_knn = MetricsCalc(raw_df, df, loneliness_dict, health_dict, economic_strength_dict, False, True)
                    map_df = addAggMetrics(df_scored, False)

                    df_scored.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)

                    st.session_state['df_scored'] = df_scored
                    st.session_state['df_knn'] = df_knn
                    st.session_state['map_df'] = map_df

                    st.success("File was uploaded!")
  
            else:
                st.session_state['flag'] = False

            
    elif choose == "Social KPIs" and st.session_state['flag'] is False:
        with kpi_header:
    #         st.title("The visualization of our KPI's")
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Social KPIs</p>', unsafe_allow_html=True)

        st.error("CSV file was not uploaded. Please go back to 'File Upload' page!")

    elif choose == "Social KPIs" and st.session_state['flag'] is True:
        with kpi_header:
    #         st.title("The visualization of our KPI's")
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Social KPIs</p>', unsafe_allow_html=True)
            subheader("Social KPIs are our three social metrics - Loneliness, Health, Economic Strength. These are formed and calculated based on the given data and defined by the “Joint” organization and influenced by weights.")
            subheader("SoCity enables you not only to explore and analyze the data as given but also to take control over the weighting process of each parameter, for each metric. This flexibility enables you to determine the importance of different parameters and reflects changes regarding resource allocation.")
            subheader("Choose a KPI and set each parameter according to your urban planning and perception. This modification affects ‘Risk’.")

            with kpi_selection:
                header("KPI Selection")
                KPI_names = ["Loneliness", "Health", "Economic Strength"]
                KPI_page = st.radio("", KPI_names)

            with kpi_weights:
                header("KPI weights")

                if KPI_page == "Loneliness":
#                     if st.button("Reset Weights"):
#                         loneliness_dict = {}
#                         loneliness_dict = loneliness_default_weights(st.session_state['df'], loneliness_dict)
#                         st.session_state['loneliness_dict'] = loneliness_dict

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
                                            'corona_immunity':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                            'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                            'area_per_person_score':('שטח לאדם במשק בית', 'הסבר על המדד'),
                                            'Ownership_score':('סוג בעלות על הדירה (שכירות/בעלות)', 'הסבר על המדד')
                                           }
                                            
			
                    loneliness_english_dict={'arnona_cat_score':('Arnona discount per household','If and under what circumstance the household get arnona discount'),
						'members_Water_score':('Number of people per household','Number of people living in this house according to water records'),
						'martial_score':('Marital status of head of household','The marital status can be one of the followings widow,single,married, divorced') ,
						'widow_grown_score':('Number of older (18 - 67) widows in statistical area', 'The number of grown widows in ages 18-67 who live in the statistical area'),
						'widow_elderlies_score':('Number of elderly (above 67) widows in statistical area','The number of elderlies widows (67 and older) who live in statistical area'),
						'lonely_elderlies_score':('Number of lonely elderlies (above 67) in statistical area','The number of elderlies (67 and older) that defined lonely according to municipalities records'),
						'p85_plus_score':('Number of people aged 85 and above in statistical area','Number of people aged 85 and above in statistical area according to municipalities records'),
						'corona_immunity_score':('Corona status per statistical area','Calculation of Corona parameters in statistical area'),
					     	'age_score':('Age of head of household','The age of the head of the household according to municipalities records'),
						'area_per_person_score':('Area per person per household', 'Built-up area of the household divided by the number of people live in the house'),
						'Ownership_score':('Type of property ownership (rent/ownership)', 'Indicate whether the house is rent or owned by the head of the household')
					    }

                    curr_loneliness_dict = loneliness_dict.copy()
                    for key, val in curr_loneliness_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_loneliness_dict[f'{key}'] = temp_col.select_slider(f'{loneliness_english_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Loneliness_slider_{key}', help=f'{loneliness_english_dict[key][1]}')
                            index += 1

                    sum_of_weights = round(sum(list(curr_loneliness_dict.values())), 3)
    #                 st.write(sum_of_weights)
                    loneliness_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_loneliness_dict.items()}
    #                 update_session_state("loneliness_dict", loneliness_dict)
                    st.session_state['loneliness_dict'] = loneliness_dict
 
                    curr_df = MetricsCalc(st.session_state['raw_df'], st.session_state['df_scored'], loneliness_dict, st.session_state['health_dict'], st.session_state['economic_strength_dict'], True, False)
                    st.session_state['df_scores'] = curr_df
                    map_df = addAggMetrics(curr_df, False)
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
                        "html": "<b>Loneliness KPI (Average) = {Loneliness_score_AVG}</b>",
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
                    option = st.selectbox('Choose the Layer:',('Display by average', 'Display by worst'))
                    if option == 'Display by average':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    elif option == 'Display by worst':
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
#                     if st.button("Reset Weights"):
#                         health_dict = {}
#                         health_dict = health_default_weights(st.session_state['df'], health_dict)
#                         st.session_state['health_dict'] = health_dict
			
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
                                        'corona_immunity_score':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                       }
                    health_english_dict={'arnona_cat_score':('Arnona discount per household','If and under what circumstance the household get arnona discount'),
					'age_score':('Age of head of household','The age of the head of the household according to municipalities records'),
					'hashlama_kizvat_nechut_elderlies_score':('Completion of a disability allowance for a senior citizen in statistical area','The number of elderlies (67+) in statistical area, who get Completion of a disability allowance'),
					'Mekabley_kizbaot_nechut_score':('Disability allowance recipients in statistical area','The number of people in statistical area, who get a disability allowance'),
					'zachaim_kizbat_nechut_children_score':('Children entitled to a disability allowance in statistical area','The number of children in statistical area, who are entitled to a disability allowance'),
					'mekabley_kizbaot_from_injured_Work_score':('Allowance recipients due to a work injury in statistical area', 'The number of people in statistical area who get an allowance due to a work injury'),
					'mekabley_kizba_siud_score':('Recipients of nursing allowance in statistical area', 'The number of people in statistical area who get nursing allowance'),
					'corona_immunity_score':('Corona status per statistical area','Calculation of Corona parameters in statistical area')
					  }
	
                    curr_health_dict = health_dict.copy()
                    for key, val in curr_health_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_health_dict[f'{key}'] = temp_col.select_slider(f'{health_english_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Health_slider_{key}', help=f'{health_english_dict[key][1]}')
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
                    map_df = addAggMetrics(curr_df, False)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        
                    R_color_AVG, G_color_AVG, R_color_STRCT, G_color_STRCT = [], [], [], []
                    num_of_rows = map_df.shape[0]
#                     num_of_rows_range = [i for i in range(num_of_rows)]
#                     st.write(map_df)
                    for avg in list(map_df["Health_score_AVG"]):
                        avg = round(avg)
                        if avg == 1:
                            R_color_AVG.append(255)
                            G_color_AVG.append(0)
                        elif avg == 2:
                            R_color_AVG.append(255)
                            G_color_AVG.append(167)
                        elif avg == 3:
                            R_color_AVG.append(255)
                            G_color_AVG.append(244)
                        elif avg == 4:
                            R_color_AVG.append(163)
                            G_color_AVG.append(255)
                        elif avg == 5:
                            R_color_AVG.append(44)
                            G_color_AVG.append(186)
                   
                    for strct in list(map_df["Health_score_STRCT"]):
                        if strct == 1:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(0)
                        elif strct == 2:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(167)
                        elif strct == 3:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(244)
                        elif strct == 4:
                            R_color_STRCT.append(163)
                            G_color_STRCT.append(255)
                        elif strct == 5:
                            R_color_STRCT.append(44)
                            G_color_STRCT.append(186)

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
                        "html": "<b>Health KPI (Average) = {Health_score_AVG}</b>",
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
                    option = st.selectbox('Choose the Layer:',('Display by average', 'Display by worst'))
                    if option == 'Display by average':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    elif option == 'Display by worst':
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

                elif KPI_page == "Economic Strength":
#                     if st.button("Reset Weights"):
#                         economic_strength_dict = {}
#                         economic_strength_dict = economic_strength_default_weights(st.session_state['df'], economic_strength_dict)
#                         st.session_state['economic_strength_dict'] = economic_strength_dict
			
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
                    economic_strenght_english_dict={'area_per_person_score':('Area per person per household','Built-up area of the household divided by the number of people live in the house'),
						'socio_economic_score':('Socio-economic score','The socio economic score of the statistical area'),
						'mekabley_kizba_siud_score':('Recipients of nursing allowance in statistical area', 'The number of household in statistical area who get nursing allowance'),
						'mekabley_kizbaot_from_injured_Work_score':('Allowance recipients due to a work injury in statistical area', 'The number of households in statistical area who get an allowance due to a work injury'),
						'zachaim_kizbat_nechut_children_score':('Children entitled to a disability allowance in statistical area','The number of children in statistical area, who are entitled to a disability allowance'),
						'Mekabley_kizbaot_nechut_score':('Disability allowance recipients in statistical area','The number of households in statistical area, who get a disability allowance'),
						'Mekabley_mezonot_score':('Alimony recipients in statistical area','The number of households in statistical area, who get child support payments'),
						'Hashlamat_hachnasa_sheerim_family_score':('Income completion of death benefits in statistical areas','The number of households in statistical area, who get death benefits'),
						'hashlama_kizvat_nechut_elderlies_score':('Completion of a disability allowance for a senior citizen in statistical area','The number of elderlies (67+) in statistical area, who get Completion of a disability allowance'),
						'hashlamta_hachnasa_family_eldelies_score':('Recipients of income completions due to elderlies in the family in statistical area', 'The number of household in statistical area  which get income completions due to elderlies in the family'),
						'mekabley_kizva_elderlies_score':('Recipients of elderly allowance in statistical area','The number of households in statistical area who get elderly allowance'),
						'avtachat_hachansa_family_score':('Recipients of family income security in statistical area', 'The number of households which get family income security in statistical area'),
						'income_per_person_score':('Total income per person per household','The total income of household divided by the number of people live in the house'),
						'arnona_cat_score':('Arnona discount per household','If and under what circumstance the household get arnona discount'),
						'Ownership_score':('Type of property ownership (rent/ownership)','Indicate whether the house is rent or owned by the head of the household'),
						'age_score':('Age of head of household','The age of the head of the household according to municipalities records'),
						'martial_score':('Marital status of head of household','The marital status can be one of the followings widow,single,married, divorced'),
						'members_Water_score':('Number of people per household','Number of people living in this house according to water records'),
						'near_106_pizul_and_dangerous_buildings_score':('A building that is up to 25 meters away from a dangerous building or a building that has been split','')
						  }

                    curr_economic_strength_dict = economic_strength_dict.copy()
                    for key, val in curr_economic_strength_dict.items():
                        if index % 2 == 0:
                            temp_col = even_col
                        if index % 2 == 1:
                            temp_col = odd_col
                        if val != 0:
                            curr_economic_strength_dict[f'{key}'] = temp_col.select_slider(f'{economic_strenght_english_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                        value=val, key=f'Economic_Strength_slider_{key}', help=f'{economic_strenght_english_dict[key][1]}')
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
                    map_df = addAggMetrics(curr_df, False)
                    map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        
                    R_color_AVG, G_color_AVG, R_color_STRCT, G_color_STRCT = [], [], [], []
#                     num_of_rows = map_df.shape[0]
#                     num_of_rows_range = [i for i in range(num_of_rows)]
#                     st.write(map_df)
                    for avg in list(map_df["Economic_Strength_score_AVG"]):
                        avg = round(avg)
                        if avg == 1:
                            R_color_AVG.append(255)
                            G_color_AVG.append(0)
                        elif avg == 2:
                            R_color_AVG.append(255)
                            G_color_AVG.append(167)
                        elif avg == 3:
                            R_color_AVG.append(255)
                            G_color_AVG.append(244)
                        elif avg == 4:
                            R_color_AVG.append(163)
                            G_color_AVG.append(255)
                        elif avg == 5:
                            R_color_AVG.append(44)
                            G_color_AVG.append(186)
                   
                    for strct in list(map_df["Economic_Strength_score_STRCT"]):
                        if strct == 1:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(0)
                        elif strct == 2:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(167)
                        elif strct == 3:
                            R_color_STRCT.append(255)
                            G_color_STRCT.append(244)
                        elif strct == 4:
                            R_color_STRCT.append(163)
                            G_color_STRCT.append(255)
                        elif strct == 5:
                            R_color_STRCT.append(44)
                            G_color_STRCT.append(186)

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
                        "html": "<b>Economic Strength KPI (Average) = {Economic_Strength_score_AVG}</b>",
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
                    option = st.selectbox('Choose the Layer:',('Display by average', 'Display by worst'))
                    if option == 'Display by average':
                        layer = AVERAGE
                        tooltip = tooltip_AVG
                    elif option == 'Display by worst':
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
                    
    
    elif choose == "Risk" and st.session_state['flag'] is False:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Risk</p>', unsafe_allow_html=True)
        
        st.error("CSV file was not uploaded. Please go back to 'File Upload' page!")
        
        
    elif choose == "Risk" and st.session_state['flag'] is True:
    #     st.balloons()
    #     st.title("The Prediction section")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Risk</p>', unsafe_allow_html=True)
        subheader("SoCity combines data and visualization, not only to present the data, but to spot households under risk. During the project we came to an understanding that “risk” is a combination of three social KPIs which are Loneliness, Health and Economic strength. The following view presents the buildings that have at least one household under risk, based on the metrics as defined in 'social KPIs' page.")
#         subheader("This view presents the buildings that have at least one household in risk, considering the changes that were made on social KPIs view. For the most convenient and effective data processing we present the household in risk in two ways:")
#         subheader("1.  On a map - you can get partial understanding")
#         subheader("2.  In a table - you can get more details about the household in risk and act to help them. You can download this data for future usage.")
         # \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
        with st.spinner('Processing, it may take a few minutes..'):
            curr_df = MetricsCalc(st.session_state['raw_df'], st.session_state['df_scored'], st.session_state['loneliness_dict'], st.session_state['health_dict'], st.session_state['health_dict'], True, False)
            st.session_state['df_scores'] = curr_df
            under_risk_list_df = CalcRisk(curr_df)
            perc = round(under_risk_list_df.query('Risk == 1').count()[1]/under_risk_list_df.shape[0],3)*100
        
            col1, col2 = st.columns([3, 1])
#                 col1, col2, col3 = st.columns(3)
#                 col1.subheader("")
#                 col2.subheader("Households which are under risk")
#                 col2.metric(label="", value=f'{round(perc_risk,3)}%')
#                 col3.subheader("")
#                 st.metric(label="Households which are under risk", value=f'{round(perc_risk,3)}%')

            col1.header("")
            col1.subheader("")
            col1.subheader("")
            col1.subheader(f'{round(perc,3)}% of the households are under risk')


            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            colors = ['#FF4B4B', '#00aef0']
            labels = ['', '']
            sizes = [perc/100, 1-(perc/100)]
            explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90,colors=colors)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            col2.pyplot(fig1)
        
            under_risk_list_df = under_risk_list_df.query('Risk == 1').sort_values(by=['R_function'], ascending=False)[['STAT','lat','lon','Loneliness_score','Health_score','Economic_Strength_score']]
            subheader("List of under-risk households:")    
            
            under_risk_list_df.rename(columns = {'lon' : 'east', 'lat' : 'north'}, inplace = True)
            st.dataframe(under_risk_list_df, 800)

            under_risk_list_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
            
            download = FileDownloader(under_risk_list_df.to_csv(),file_ext='csv').download()
            st.markdown("")
            subheader("For your convenience, visualization of under-risk buildings over the map. Notice that the darker the spot the more households under risk in this building")
            map_df = addAggMetrics(curr_df, True)
            map_df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
        # /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                
        
        st.session_state['Risk_df'] = map_df # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#         st.title(f'{round(perc_risk,3)}% of the households are under risk') # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#         st.dataframe(Risk_df) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#         def convert_df(df):
#             # IMPORTANT: Cache the conversion to prevent computation on every rerun
#             return df.to_csv().encode('utf-8')

#         csv = convert_df(df_risk) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#         if st.download_button(
#              label="Download the Risk data as CSV",
#              data=csv,
#              file_name='Prediction.csv',
#              mime='text/csv',
#             ):
#             st.stop()
        
        Risk_layer = pydeck.Layer(
                        'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                        under_risk_list_df,
                        get_position=['lon', 'lat'],
#                         get_elevation="Risk", # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        elevation_scale=20,
    #                     radius=40,
                        get_radius = 10,
                        auto_highlight=True,
    #                     get_radius=10000,          # Radius is given in meters
                        # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                        # new: ["R_color", "G_color", "0", "120"],
                        get_fill_color=["255", "0", "0", "120"],  # Set an RGBA value for fill
    #                     elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        coverage=5 #0.1
                        )
        Risk_tooltip = {
            "html": "<b>Risk index (Worst) = 1)</b>",
            "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
        }

        view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
        view.pitch = 75
        view.bearing = 60
        view.zoom = 14

        r = pydeck.Deck(
            Risk_layer,
            initial_view_state=view,
            tooltip=Risk_tooltip,
            map_provider="mapbox",
            map_style=pydeck.map_styles.SATELLITE,
        )
        st.pydeck_chart(r)
#         knn_file = st.file_uploader("Choose a CSV file for KNN", type=['csv'], key="knn_file")
#         new_file = st.file_uploader("Choose a new CSV file to predict", type=['csv'], key="new_file")
#         if new_file is not None:
#             new_df = pd.read_csv(new_file)
#             st.session_state['new_df'] = new_df
#             st.success("File was uploaded!")

# #             st.write(new_df)
# #             st.write(st.session_state['df_knn'])
# #         if st.button('Predict!'):

#             with st.spinner('Processing, it may take a few minutes..'):
#                 perc_risk, df_risk = prediction_main(st.session_state['df_knn'], new_df)
# #                 col1, col2, col3 = st.columns(3)
# #                 col1.subheader("")
# #                 col2.subheader("Households which are under risk")
# #                 col2.metric(label="", value=f'{round(perc_risk,3)}%')
# #                 col3.subheader("")
# #                 st.metric(label="Households which are under risk", value=f'{round(perc_risk,3)}%')
#                 st.title(f'{round(perc_risk,3)}% of the households are under risk')
                
#                 st.dataframe(df_risk)

#                 def convert_df(df):
#                     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#                     return df.to_csv().encode('utf-8')

#                 csv = convert_df(df_risk)
#                 st.download_button(
#                      label="Download the predicted data as CSV",
#                      data=csv,
#                      file_name='Prediction.csv',
#                      mime='text/csv',
#                     )
        
        
    elif choose == "Prediction" and st.session_state['flag'] is False:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Prediction</p>', unsafe_allow_html=True)
        
        st.error("CSV file was not uploaded. Please go back to 'File Upload' page!")
        
    elif choose == "Prediction" and st.session_state['flag'] is True:
    #     st.balloons()
    #     st.title("The Prediction section")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Prediction</p>', unsafe_allow_html=True)
#         knn_file = st.file_uploader("Choose a CSV file for KNN", type=['csv'], key="knn_file")
        subheader("In order to generalize the system for future usage, where the data format is similar but not identical to the initial format, ")
        subheader("a KNN model is used to predict the risk of a new given set of households. ")
        subheader("Upload new data and get the information about the percentage and the household in risk. ")
        subheader("You can also download the results for further processing.")
        new_file = st.file_uploader("Choose a new CSV file to predict", type=['csv'], key="new_file")    
        if new_file is not None:
            new_df = pd.read_csv(new_file)
            st.session_state['new_df'] = new_df
            st.success("File was uploaded!")

    #             st.write(new_df)
    #             st.write(st.session_state['df_knn'])
    #         if st.button('Predict!'):
    #         finish_flag = False
            with st.spinner('Predicting, it may take a few minutes..'):
                perc_risk, df_risk = prediction_main(st.session_state['df_knn'], new_df)
                col1, col2 = st.columns([3, 1])
    #                 col1, col2, col3 = st.columns(3)
    #                 col1.subheader("")
    #                 col2.subheader("Households which are under risk")
    #                 col2.metric(label="", value=f'{round(perc_risk,3)}%')
    #                 col3.subheader("")
    #                 st.metric(label="Households which are under risk", value=f'{round(perc_risk,3)}%')

                col1.header("")
                col1.subheader("")
                col1.subheader("")
                col1.subheader(f'{round(perc_risk,3)}% of the households are under risk')


                # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                colors = ['#FF4B4B', '#00aef0']
                labels = ['', '']
                sizes = [perc_risk/100, 1-(perc_risk/100)]
                explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90,colors=colors)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                col2.pyplot(fig1)

                df_risk = df_risk.query('Risk == 1').sort_values(by=['R_function'], ascending=False)[['index','STAT','east','north','pred_Loneliness','pred_Health','pred_Economic_Strength']]

                st.dataframe(df_risk)
#                 st.session_state["finish_Prediction_flag"] = True
                
#                 if st.button("Download the predicted data as CSV"):
#                     df_risk.to_csv('Prediction.csv', index=False ,encoding = 'utf-8')
# #                     files.download('Prediction.csv')
#                     st.stop()
                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')

                csv = convert_df(df_risk)
#                 st.download_button(
#                      label="Download the predicted data as CSV",
#                      data=csv,
#                      file_name='Prediction.csv',
#                      mime='text/csv'
# #                     ,
# #                      on_click=st.stop(),
#                     )
                download = FileDownloader(df_risk.to_csv(),file_ext='csv').download()
                    
#         if (new_file is not None) and (finish_flag == True):
#         def convert_df(df):
#             # IMPORTANT: Cache the conversion to prevent computation on every rerun
#             return df.to_csv().encode('utf-8')

#         csv = convert_df(df_risk)
#         st.download_button(
#              label="Download the predicted data as CSV",
#              data=csv,
#              file_name='Prediction.csv',
#              mime='text/csv',
#             )
    
    elif choose == "About Us":
        #         st.title("The About section")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About Us</p>', unsafe_allow_html=True)
        about_home_subheader("We are information system engineering students at the Technion.")
        about_home_subheader("As a part of our studies we had to work on a final project that combines the knowledge we gained during the last four years of our studies.")
        about_home_subheader("Beside the fact that we are very good friends, we have also a lot of experience working together,")
        about_home_subheader("so the decision to unite into a team was natural and immediate.")
        about_home_subheader("but after hearing and realizing the large impact this project may have on our society we didn’t think twice.")
        about_home_subheader("We were thrilled and excited to work on a project with large added value that contributes to society.")
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

    if ("password_correct" not in st.session_state) or (not st.session_state["password_correct"]):
        col_1, col_2, col_3, col_4, col_5, col_6, col_7 = st.columns(7)
        with col_1:
            st.write("")

        with col_2:
            st.write("")

        with col_3:
            st.write("")
        
        with col_4:
            image = Image.open('background_img/SoCityFINAL-LOGO.png')
            st.image(image)
            
        with col_5:
            st.write("")
            
        with col_6:
            st.write("")
            
        with col_7:
            st.write("")
            
#         st.info('Please enter Username and Password')
        # First run, show inputs for username + password.
        st.text_input("Username", value="Admin", key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
#         is_register = st.button("Submit")
#         if is_register:
    # Password Incorrect.
        if ("password_correct" not in st.session_state):
            st.warning("Press enter to submit")
        elif (not st.session_state["password_correct"]):
            st.error("Username/Password is incorrect 😕")
        return False
#     elif not st.session_state["password_correct"]:
#         col_1, col_2, col_3, col_4, col_5, col_6, col_7 = st.columns(7)
#         with col_1:
#             st.write("")

#         with col_2:
#             st.write("")

#         with col_3:
#             st.write("")
        
#         with col_4:
#             image = Image.open('background_img/SoCityFINAL-LOGO.png')
#             st.image(image)
            
#         with col_5:
#             st.write("")
            
#         with col_6:
#             st.write("")
            
#         with col_7:
#             st.write("")
            
        
            
            
#         st.info('Please enter Username and Password')
#         # Password not correct, show input + error.
#         st.text_input("Username", key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
# #         is_register = st.button("Submit")
# #         if is_register:
#     # Password Incorrect.
#         st.error("Username/Password is incorrect 😕")
#         return False
    else:
#         if is_register:
    # Password correct.
        return True
    
    
    
def csv_downloader(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "new_text_file_{}_.csv".format(timestr)
# 	st.markdown("#### Download File ###")
	href = f'<a href="data:file/csv;base64,{b64}" style="text-decoration:none;" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)

# Class
class FileDownloader(object):
	"""docstring for FileDownloader
	>>> download = FileDownloader(data,filename,file_ext).download()
	"""
	def __init__(self, data,filename='prediction',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext

	def download(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}.{}".format(self.filename,timestr,self.file_ext)
# 		st.markdown("#### Download File ###")
		href = f'<div class="download"><a href="data:file/{self.file_ext};base64,{b64}" style="text-decoration:none;color:#000000" download="{new_filename}">Download</a></div>'
		st.markdown(href,unsafe_allow_html=True)



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
