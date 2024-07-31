import streamlit as st
import numpy as np
import pandas as pd
import pickle

#st.set_page_config(page_title="Anime Recommendation",
 #                  page_icon="",
  #                 initial_sidebar_state="collapsed"
#)

with open(r'anime_dict.pkl', 'rb') as file:
    anime_dict = pickle.load(file)

with open(r'anime_stlit.pkl', 'rb') as file:
    anime_df = pickle.load(file)

st.title("Welcome")


def show_search_page():
    col1, col2= st.columns([7,1], vertical_alignment="bottom")
    with col1:
        search=st.text_input(label='',placeholder="Type here, try exact spelling...")

    with col2:
        ser_button= st.button(label=':globe_with_meridians:')

    if ser_button:
        matching_rows= anime_df[(anime_df['English name'].str.contains(search,case=False, na= False))
                                | (anime_df['Name'].str.contains(search,case=False,na=False))]
        
        if not matching_rows.empty:
            st.write("Matching entries found:")
            top_rows= matching_rows.head(8)

            num_col=3

            for i in range(0, min(len(top_rows),8), num_col):
                cols= st.columns(num_col)
                for j,col in enumerate(cols):
                    if i+j <len(top_rows):
                        row= top_rows.iloc[i+j]
                        image_url= row['Image URL']
                        name= row['Name']

                        #col.markdown(f'<a href="#" target="_blank"><img src="{image_url}" alt="{name}" style="width:150px;height:150px;"></a>', unsafe_allow_html=True)
                        #col.markdown(f'<a href="#" target="_blank">{name}</a>', unsafe_allow_html=True)
                        
                        with col:
                            st.image(image_url, use_column_width=True)
                            if col.button(f"{name}", key=name):
                                st.session_state['selected_anime'] = {
                                        'name': name,
                                        'image': image_url,
                                        
                                    }
                                st.experimental_rerun()

        else:
            st.write("No matching entries found.")

show_search_page()
