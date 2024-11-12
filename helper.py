import pandas as pd
import matplotlib.pyplot as plt

def create_plot(csv_file, countries):
    # Load the simulated data
    df = pd.read_csv(csv_file)

    # Filter the data for the selected countries
    filtered_df = df[df['country'].isin(countries)]

    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the data for each country
    for country in countries:
        country_data = filtered_df[filtered_df['country'] == country]
        ax.plot(country_data['date'], country_data['H'], label=f'{country} - Healthy', linestyle='-')
        ax.plot(country_data['date'], country_data['I'], label=f'{country} - Infected', linestyle='--')
        ax.plot(country_data['date'], country_data['S'], label=f'{country} - Symptoms', linestyle='-.')
        ax.plot(country_data['date'], country_data['M'], label=f'{country} - Immune', linestyle=':')
        ax.plot(country_data['date'], country_data['D'], label=f'{country} - Deceased', linestyle='-.')

    # Customize the plot
    ax.set_title('COVID-19 Simulation Results')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.legend()

    # Save or display the plot
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('covid_simulation_plot.png')  # Save plot as an image file
    plt.show()  # Display plot in a separate window
