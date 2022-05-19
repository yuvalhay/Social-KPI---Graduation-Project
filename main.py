import streamlit as st
import setuptools

setuptools.setup(
    name="streamlit-option-menu",
    version="0.3.2",
    author="Victor Yan",
    author_email="victoryhb@163.com",
    description="streamlit-option-menu is a simple Streamlit component that allows users to select a single item from a list of options in a menu.",
    long_description="""streamlit-option-menu is a simple Streamlit component that allows users to select a single item from a list of options in a menu.
It is similar in function to st.selectbox(), except that:
- It uses a simple static list to display the options instead of a dropdown
- It has configurable icons for each option item and the menu title
It is built on [streamlit-component-template-vue](https://github.com/andfanilo/streamlit-component-template-vue), styled with [Bootstrap](https://getbootstrap.com/) and with icons from [bootstrap-icons](https://icons.getbootstrap.com/)
## Installation
```
pip install streamlit-option-menu
```
## Parameters
The `option_menu` function accepts the following parameters:
- menu_title (required): the title of the menu; pass None to hide the title
- options (required): list of (string) options to display in the menu; set an option to "---" if you want to insert a section separator
- default_index (optional, default=0): the index of the selected option by default
- menu_icon (optional, default="menu-up"): name of the [bootstrap-icon](https://icons.getbootstrap.com/) to be used for the menu title
- icons (optional, default=["caret-right"]): list of [bootstrap-icon](https://icons.getbootstrap.com/) names to be used for each option; its length should be equal to the length of options
- orientation (optional, default="vertical"): "vertical" or "horizontal"; whether to display the menu vertically or horizontally
The function returns the (string) option currently selected
## Example
```
import streamlit as st
from streamlit_option_menu import option_menu
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected
# horizontal Menu
selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected2
```
""",
    long_description_content_type="text/plain",
    url="https://github.com/yuvalhay/Social-KPI---Graduation-Project/streamlit-option-menu",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
from streamlit_option_menu import option_menu

# import streamlit.components.v1 as html
# from PIL import Image
# import cv2
# from st_aggrid import AgGrid
# import plotly.express as px
# import io

header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()

with st.sidebar:
    # st.sidebar
    # options_names = ["Prediction", "KPI"]
    # choose_page = st.radio("Choose", options_names)

    choose = option_menu("App Gallery", ["About", "Prediction", "Social KPI", "Contact"],
                         icons=['person lines fill', 'pc display horizontal', 'people', 'pencil square'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "orange"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )

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
    Loneliness_default_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
    # Loneliness_sliders = [st.slider("arnona_cat", 0.0, 1.0, Loneliness_default_values[0]),
    #                       st.slider("members_Water", 0.0, 1.0, Loneliness_default_values[1]),
    #                       st.slider("martial", 0.0, 1.0, Loneliness_default_values[2]),
    #                       st.slider("widow_grown", 0.0, 1.0, Loneliness_default_values[3]),
    #                       st.slider("widow_elderlies", 0.0, 1.0, Loneliness_default_values[4]),
    #                       st.slider("lonely_elderlies", 0.0, 1.0, Loneliness_default_values[5]),
    #                       st.slider("p85_plus", 0.0, 1.0, Loneliness_default_values[6]),
    #                       st.slider("accumulated_cases", 0.0, 1.0, Loneliness_default_values[7])]
    if KPI_page == "Loneliness":
        current_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
        arnona_cat = st.slider("arnona_cat", 0.0, 1.0, Loneliness_default_values[0])
        members_Water = st.slider("members_Water", 0.0, 1.0, Loneliness_default_values[1])
        martial = st.slider("martial", 0.0, 1.0, Loneliness_default_values[2])
        widow_grown = st.slider("widow_grown", 0.0, 1.0, Loneliness_default_values[3])
        widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, Loneliness_default_values[4])
        lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, Loneliness_default_values[5])
        p85_plus = st.slider("p85_plus", 0.0, 1.0, Loneliness_default_values[6])
        accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, Loneliness_default_values[7])

        if arnona_cat != current_values[0]:
            diff_val = arnona_cat - current_values[0]
            avg_diff = diff_val/7  # בכמה לשנות כל משקל
            current_values[0] = arnona_cat
            if diff_val > 0:
                for i in range(8):
                    if i != 0:
                        current_values[i] = current_values[i] - avg_diff

                members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1])
                martial = st.slider("martial", 0.0, 1.0, current_values[2])
                widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3])
                widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4])
                lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5])
                p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6])
                accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7])

            else:
                for i in range(8):
                    if i != 0:
                        current_values[i] += avg_diff

                members_Water = st.slider("members_Water", 0.0, 1.0, current_values[1])
                martial = st.slider("martial", 0.0, 1.0, current_values[2])
                widow_grown = st.slider("widow_grown", 0.0, 1.0, current_values[3])
                widow_elderlies = st.slider("widow_elderlies", 0.0, 1.0, current_values[4])
                lonely_elderlies = st.slider("lonely_elderlies", 0.0, 1.0, current_values[5])
                p85_plus = st.slider("p85_plus", 0.0, 1.0, current_values[6])
                accumulated_cases = st.slider("accumulated_cases", 0.0, 1.0, current_values[7])

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
