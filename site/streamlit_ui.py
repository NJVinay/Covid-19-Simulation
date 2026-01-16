import streamlit as st  #Imports the Streamlit library for building the web app
import pandas as pd  # Imports pandas for data manipulation
import assignment2  # Imports assignment2 module containing the simulation logic

st.title("Covid - 19 Simulation Test Runner") 

SAMPLE_RATIO = st.number_input("Sample Ratio", value=float(1e6)) # Creates an input field for the sample ratio with a default value of 1 million

START_DATE = st.date_input("Start Date", value=pd.to_datetime('2021-04-01')) # Create an input field for the start date

END_DATE = st.date_input("End Date", value=pd.to_datetime('2022-04-30')) #Creates an input field for the end date

countries_df = pd.read_csv('a2-countries.csv')  # Read the CSV containing country data

SELECTED_COUNTRIES = st.multiselect("Select Countries", countries_df['country'].tolist()) #Creates a multiselect box for users to choose one or more countries from the list

#Adds a button to run the simulation 
if st.button("Run"):
    if SELECTED_COUNTRIES:  #Checks if at least one country has been selected
        #If countries are selected, displays the settings that will be used for the simulation
        st.write("Running with the following settings:")
        st.write(f"Sample Ratio: {SAMPLE_RATIO}")  #Shows chosen sample ratio
        st.write(f"Start Date: {START_DATE}")  #Shows chosen start date
        st.write(f"End Date: {END_DATE}")  #Shows chosen end date
        st.write(f"Selected Countries: {SELECTED_COUNTRIES}")  #Displays  selected countries
        
        assignment2.run('a2-countries.csv', SELECTED_COUNTRIES, SAMPLE_RATIO, START_DATE, END_DATE) # Calls the run function from the assignment2 module to execute the simulation
        
        st.success("Simulation completed successfully!")
    else:
        st.error("Please select at least one country.") #If no country is selected then it shows an error message to select at least one