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



def show_search_page():
    st.title("Search for an Anime")
    col1, col2= st.columns([7,1], vertical_alignment="bottom")
    with col1:
        user_input=st.text_input(label='',placeholder="Type here, try exact spelling...")

    with col2:
        ser_button= st.button(label=':globe_with_meridians:')

    

    if user_input:
        # Search for closest matches
        results = anime_df[(anime_df['Name'].str.contains(user_input, case=False, na=False))
                           |(anime_df['English name'].str.contains(user_input, case=False, na=False))]
        if not results.empty:
            st.write("### Closest Matches:")
            ##added
            #results= results.sort_values(by='Score')
            num_cols=3
            for i in range(0, len(results), num_cols):
                cols = st.columns(num_cols)
                for j, (idx, row) in enumerate(results.iloc[i:i+num_cols].iterrows()):
                    with cols[j]:
                        st.image(row['Image URL'], use_column_width=True)
                        if st.button(row['Name'], key=row['anime_id']):
                            st.session_state['selected_anime_id'] = row['anime_id']
                            st.session_state['page'] = 'details'
                            # Redirect to details page
                            #st.experimental_set_query_params(page='details')
                            #st.query_params(page='details')
            ###
            #for idx, row in results.head(8).iterrows():
                #if st.button(row['Name'], key=row['anime_id']):
                    #st.session_state['selected_anime_id'] = row['anime_id']
                    # Use session_state to trigger a change
                    #st.session_state['page'] = 'details'



def show_details_page():
    scroll_to_top_js = """
    <script>
    window.scrollTo(0, 0);
    </script>
    """
    
    # Execute the JavaScript to scroll to the top
    st.markdown(scroll_to_top_js, unsafe_allow_html=True)

    # Get the selected anime ID from session state
    selected_anime_id = st.session_state['selected_anime_id']
    
    # Retrieve the selected anime details from anime_df
    anime = anime_df[anime_df['anime_id'] == selected_anime_id].iloc[0]
    
    # Display the selected anime details
    st.title(anime['Name'])
    det_col1,det_col2= st.columns(2,vertical_alignment='bottom')
    with det_col1:
        st.image(anime['Image URL'], use_column_width=True)
    with det_col2:
        #st.write(anime['Synopsis'])
        st.text_area('Synopsis', anime['Synopsis'],height=200)
        st.write('Score: ',anime['Score'])
        st.write('Scored by: ',anime['Scored By'])
        st.write('favourite by: ',anime['Favorites'])
        st.write('Epsodes: ', anime['Episodes'])

    # Display similar anime
    st.write("### Similar Anime:")
    
    similar_animes = anime_dict.get(selected_anime_id, [])
    
    # Display the similar animes in a table format (3 per row)
    num_cols = 3
    if similar_animes:
        for i in range(0, len(similar_animes), num_cols):
            cols = st.columns(num_cols)
            for j, sim_id in enumerate(similar_animes[i:i+num_cols]):
                # Retrieve the similar anime details
                sim_anime = anime_df[anime_df['anime_id'] == sim_id].iloc[0]
                
                # Display the anime image and name in each column
                with cols[j]:
                    st.image(sim_anime['Image URL'], use_column_width=True)
                    if st.button(sim_anime['Name'], key=f'sim_{sim_id}'):
                        st.session_state['selected_anime_id'] = sim_id
                        st.session_state['page'] = 'details'
                        #st.experimental_set_query_params(page='details')
                        #st.query_params(page='details')
    else:
        st.write("No similar anime found.")

    # Button to go back to the search page
    if st.button("Back to Search"):
        st.session_state.pop('selected_anime_id', None)
        st.session_state['page'] = 'search'
        #st.experimental_set_query_params(page='search')
        #st.query_params(page='search')


# Main logic to switch between pages
if 'page' not in st.session_state:
    st.session_state['page'] = 'search'

if st.session_state['page'] == 'details':
    show_details_page()
else:
    show_search_page()