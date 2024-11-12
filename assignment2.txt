import csv
from datetime import datetime, timedelta
import sim_parameters
import numpy as np
import helper
from pathlib import Path
import os
import matplotlib.pyplot as plt

#This function creates a sample dataset on basis of specified sample ratio of different age groups.
def generate_sample_data(data, sample_ratio, age_groups):
    """
    Function to generate sample data based on a given sample ratio for respective age groups.
    """
    sample_data = []  #Sample data is stored here.
    unique_id = 0  #This is to assign unique IDs from 0.
    
    #This is a loop for each entry in the provided data.
    for entry in data:
        #This is to calculate population size based on sample ratio.
        entry_population = int(float(entry['population']) / sample_ratio)
        
        #Iterating through each age group.
        for age_group in age_groups:
            #This is to determine how many people belong to this age group.
            age_group_population = int(entry_population * float(entry[age_group]) / 100)
            
            #This is for creating entries for each individual in this age group.
            sample_data.extend(
                {'unique_id': unique_id + count,  #Assigning a unique ID to each individual
                 'country': entry['country'],  #Recording the country data
                 'age_group_name': age_group}  #Specifying the age group
                for count in range(age_group_population)  #Creating entries for entire population in this age group
            )
            unique_id += age_group_population  #Updating unique ID counter for next batch
    return sample_data, unique_id  #Returning generated sample data and total count

#This function predicts the states for each individual over time based on transition probabilities.
def individual_person_states(dataList, probabilities, holding_times, state_choices):
    """
    Function to predict the states for each person id.
    """
    #Creating a dictionary converting state names to their indices.
    keysMap = {j: i for i, j in enumerate(probabilities.keys())}
    result = []  #Storing the results in this array.
    counter = 0  #This will track how long each person stays in their current state.
    
    #Looping through each individual in the data list.
    for index, data in enumerate(dataList):
        temp = data.copy()  #Copying the current individual's data for manipulation.
        
        if index == 0:
            temp['state'] = 'H'  #Initial state is set as "Healthy"
            temp['staying_days'] = 0  #As this is intial state, hence the value is 0
            temp['prev_state'] = 'H'  #Previous state is also "Healthy" as it is the initial state
        else:
            #Checking if individual has been in their current state long enough.
            if counter >= holding_times[result[-1]['state']]:
                counter = 0  #Reset the counter to 0 for the new state
                state = result[-1]['state']  #This will say the previous state
                temp_states = state_choices[keysMap[state]]  #This will check for possible next states
                temp_probs = [probabilities[state].get(j, 0) for j in keysMap]  #This will store transition probabilities for those states
                temp['state'] = np.random.choice(temp_states, p=temp_probs)[1]  #This will randomly select a next state based on probabilities.

            else:
                counter += 1  #Incrementing the counter as it remains in the same state
                temp['state'] = result[-1]['state']  #To continue in their current state
        
        temp['staying_days'] = counter  #To how many days stayed been in this state
        temp['prev_state'] = result[-1]['state'] if index > 0 else 'H'  #For tracking previous state
        
        result.append(temp)  #Appending this individual's updated info to the results
    return result  #Returns the final results for all individuals

def save_file(filename, data): #This function saves the given data to a CSV file.

    source_dir = os.getcwd()  #Gets the current working directory
    filepath = os.path.join(source_dir, filename)  #To create the full file path
      
    with open(filepath, 'w', newline='') as output_file: #Open the file for writing
        keys = data[0].keys() if data else []  #Grab the keys (column headers) from the data
        writer = csv.DictWriter(output_file, fieldnames=keys)  #Writes a CSV
        writer.writeheader()  #Writes header row
        writer.writerows(data)  #Writes data rows

def plot_graph_per_country(data, country, filled=True): #This function plots simulation results for each country.
    plt.figure(figsize=(10, 6))  #Sets size of the plot
    country_data = [row for row in data if row['country'] == country]  #Filter the data to include only the entries for the specified country.
    dates = [row['date'] for row in country_data]  # Get the list of dates for plotting
    states = ['H', 'I', 'S', 'M', 'D']  # Define the states: Healthy, Infected, Serious, Mild, Deceased
    colors = ['#267764', '#FF8201', '#C84B6D', '#02B5A0', '#767A79']  # Choose distinct colors for each state
    
    plt.gca()  #Gets the current axes for the plot
    
    #Loops through each state & plots it on graph.
    for i, state in enumerate(states):
        state_counts = [row[state] for row in country_data]  #Extracts counts for each state
        if filled:
            #"fill_between" is used for creating colored areas.
            plt.fill_between(dates, state_counts, color=colors[i], label=state, alpha=0.6)
        else:
            #Else simply plots lines for each state.
            plt.plot(dates, state_counts, color=colors[i], label=state)
    
    #Set up the labels and title for the plot.
    plt.xlabel('Date')
    plt.ylabel('Number of People')
    plt.title(f'COVID-19 State Transition Over Time - {country}')
    plt.legend()  
    
    plot_filename = f'covid_{country}_filled_plot.png'  
    plt.savefig(plot_filename)  #Saves the plot as an image
    plt.show() 

#This is the main function that runs the entire simulation process.
def run(countries_csv_file_info, choosen_countries, sample_ratio, start_date_str, end_date_str):
    existing_data = []  #This creates a list to store the data to read from the CSV file
    hold_times_dict = sim_parameters.HOLDING_TIMES  #Gets holding times from simulation parameters
    trans_probs = sim_parameters.TRANSITION_PROBS  #Gets transition probabilities for state changes
    age_groups = list(trans_probs.keys())  #List of all age groups from transition probabilities
    state_names = list(hold_times_dict[age_groups[0]].keys())  #List of state names
    
    source_dir = os.getcwd()  # Get the current working directory
    countries_csv_path = os.path.join(source_dir, countries_csv_file_info)  #This creates the path to the CSV file
    
    try:
        with open(countries_csv_path, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)  #Reads the CSV data into a dictionary format
            for row in csv_data:
                country_data = dict(row)  #To convert each row into a dictionary
                if country_data['country'] in choosen_countries:
                    existing_data.append(country_data)  #Adds this specific country's data to the list
    except FileNotFoundError:
        print(f"Error: {countries_csv_file_info} not found.")  #If  file is not found, prints an error message
        return
    
    #Convert date strings to date objects for easy manipulation.
    if isinstance(start_date_str, str):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()  #Converts start date to date object
    else:
        start_date = start_date_str

    if isinstance(end_date_str, str):
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()  # Converts end date to date object
    else:
        end_date = end_date_str
    
    #Creates list of dates between start & end date.
    date_range_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    #Generates sample data based on the population and sample ratio.
    sample_data, overall_population_count = generate_sample_data(existing_data, sample_ratio, age_groups)

    sample_result_data = []  #List to hold results for each date
    #For each individual in the sample data, this associates them with each date from date range.
    for sample_entry in sample_data:
        for date_entry in date_range_list:
            entry_copy = sample_entry.copy()  #Makes a copy of the individual's data
            entry_copy['date'] = date_entry  #Adds the date to this individual's data
            sample_result_data.append(entry_copy)  #Adds this entry to results

    #Creates a list of possible state transitions based on the transition probabilities.
    state_choices = [[j + i for i in trans_probs[age_groups[0]].keys()] for j in trans_probs[age_groups[0]].keys()]
    
    simulated_output = []  #Stores final simulation results
    print("Simulation started....")
    
    #Simulates the states for each individual over time.
    for unique_id in range(overall_population_count):
        test_data = [x for x in sample_result_data if x['unique_id'] == unique_id]  # Get all data for this individual
        age_group = test_data[0]['age_group_name']  # Identify the age group for the individual
        
        try:
            #Simulates the states for each individual
            simulation_result = individual_person_states(test_data, trans_probs[age_group], hold_times_dict[age_group], state_choices)
            simulated_output.extend(simulation_result)  #Adds the simulation result to our output
        except Exception as e:
            print(f"Error in simulation for unique_id {unique_id}: {e}")  #Handles any errors that occur during simulation
    
    print("Simulation has completed...")
    save_file('a2-covid-simulated-timeseries.csv', simulated_output)     # Save the simulated time-series data to a CSV file.
    
    print("Summarising the simulated data...")  
    summarised_data = []  #Stores summarized data
    
    #Summarizes data by country & state for each date.
    for date_entry in date_range_list:
        for country in choosen_countries:
            #Filters simulation results for this country & date.
            temp_data = [i for i in simulated_output[::-1] if i['country'] == country and i['date'] == date_entry]
            summary_detail = {'date': temp_data[0]['date'], 'country': temp_data[0]['country']}  #Creates a summary entry
            
            #Counts how many people are in each state & add that to summary.
            for state in state_names:
                state_count = len([j for j in temp_data if j['state'] == state])  #Counts number of people in current state
                summary_detail[state] = state_count  #Adds the count to the summary
            
            summarised_data.append(summary_detail)  #Appends this summary to the overall list
    print("Summarising the data is done.")
    
    save_file('a2-covid-summary-timeseries.csv', summarised_data)  #Saves summarized data to a CSV file.

    print("Creating plots for countries...")  #Creates separate plots for each country to visualize the data.
    for country in choosen_countries:
        plot_graph_per_country(summarised_data, country, filled=True)  # Plot the results for each country