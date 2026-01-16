# COVID-19 Simulation

A comprehensive data-driven simulation model for COVID-19 that studies state transitions and forecasts disease progression across different countries and age groups. This project demonstrates the power of computational modeling in understanding pandemic dynamics and aiding in strategic decision-making.

## Overview

This simulation models COVID-19 disease progression through five distinct states:

- **H (Healthy)**: Susceptible individuals
- **I (Infected)**: Individuals who have contracted the virus
- **S (Serious)**: Severe cases requiring intensive care
- **M (Mild/Immune)**: Recovered individuals with immunity
- **D (Deceased)**: Fatal cases

The model uses age-specific transition probabilities and holding times to simulate realistic disease progression over time.

## Features

- **Multi-Country Support**: Simulate COVID-19 progression across 150+ countries
- **Age-Stratified Modeling**: Five age groups (less_5, 5_to_14, 15_to_24, 25_to_64, over_65) with distinct epidemiological parameters
- **Interactive Web Interface**: Streamlit-based UI for easy configuration and execution
- **Flexible Sampling**: Adjustable sample ratios for computational efficiency
- **Comprehensive Visualization**: Automatic generation of filled area plots and line graphs
- **Time-Series Output**: Detailed CSV exports of individual-level and aggregated data

## Project Structure

```
????????? assignment2.py          # Core simulation engine
????????? streamlit_ui.py         # Interactive web interface
????????? sim_parameters.py       # Transition probabilities and holding times
????????? helper.py               # Plotting utilities
????????? test.py                 # Unit tests
????????? a2-countries.csv        # Country demographic data (154 countries)
????????? README.md               # This file
????????? *.txt                   # Documentation files
```

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Dependencies

```bash
pip install numpy pandas matplotlib streamlit
```

## Usage

### Method 1: Interactive Web Interface (Recommended)

1. Launch the Streamlit app:

```bash
streamlit run streamlit_ui.py
```

2. Configure simulation parameters:

   - **Sample Ratio**: Population scaling factor (default: 1,000,000)
   - **Start Date**: Simulation start date
   - **End Date**: Simulation end date
   - **Countries**: Select one or more countries from the dropdown

3. Click "Run" to execute the simulation

### Method 2: Python Script

```python
import assignment2

# Run simulation for specific countries
assignment2.run(
    countries_csv_file_info='a2-countries.csv',
    choosen_countries=['Afghanistan', 'Sweden', 'Japan'],
    sample_ratio=1e6,
    start_date='2021-04-01',
    end_date='2022-04-30'
)
```

### Method 3: Unit Tests

```bash
python test.py
```

## Simulation Parameters

### Transition Probabilities (sim_parameters.py)

Age-specific probabilities for state transitions:

- Young age groups (<24): Lower infection rates (10%), minimal mortality (1%)
- Adult groups (25-64): Higher infection rates (30%), moderate mortality (5-20%)
- Elderly (65+): Highest risk with 30% infection rate and up to 40% mortality from serious cases

### Holding Times

Duration (in days) individuals remain in each state:

- **Infected (I)**: 4 days
- **Serious (S)**: 14 days
- **Mild/Immune (M)**: 120 days
- **Healthy/Deceased**: 0 days (no holding time)

## Output Files

The simulation generates three types of output:

1. **a2-covid-simulated-timeseries.csv**: Individual-level state transitions over time

   - Columns: unique_id, country, age_group_name, date, state, staying_days, prev_state

2. **a2-covid-summary-timeseries.csv**: Aggregated daily counts by country and state

   - Columns: date, country, H, I, S, M, D

3. **covid\_{country}\_filled_plot.png**: Visualization for each simulated country

## Key Functions

### `generate_sample_data(data, sample_ratio, age_groups)`

Generates a sample population based on demographic data and specified sampling ratio.

### `individual_person_states(dataList, probabilities, holding_times, state_choices)`

Simulates disease progression for each individual using Markov chain state transitions.

### `run(countries_csv_file_info, choosen_countries, sample_ratio, start_date_str, end_date_str)`

Main orchestration function that executes the complete simulation pipeline.

### `plot_graph_per_country(data, country, filled=True)`

Creates filled area plots showing state distribution over time for each country.

## Algorithm Details

The simulation employs a discrete-time Markov chain approach:

1. **Population Sampling**: Scales country populations using the sample ratio while preserving age distributions
2. **State Initialization**: All individuals start in the "Healthy" (H) state
3. **Daily State Transitions**: For each day and individual:
   - Check if holding time for current state has elapsed
   - If elapsed, randomly select next state based on age-specific transition probabilities
   - If not elapsed, remain in current state
4. **Data Aggregation**: Summarize individual states by country and date
5. **Visualization**: Generate plots showing epidemic curves

## Data Source

The `a2-countries.csv` file contains demographic information for 154 countries including:

- Total population
- Median age
- Age distribution percentages (5 age groups)

## Performance Considerations

- Sample ratios of 1,000,000 (1M) are recommended for computational efficiency
- Larger date ranges increase processing time linearly
- Memory usage scales with: (population / sample_ratio) ?? number of days ?? number of countries

## Limitations

- Assumes closed populations (no migration)
- Homogeneous mixing within countries
- Fixed transition probabilities over time
- No intervention modeling (vaccines, lockdowns, etc.)

## Future Enhancements

- Vaccination modeling
- Regional/sub-national resolution
- Dynamic transmission rates
- Healthcare capacity constraints
- Multiple virus variants

## Contributing

This project was developed as part of an academic assignment. Contributions, improvements, and extensions are welcome.

## License

This project is available for educational and research purposes.

## Contact

For questions or collaboration opportunities, please refer to the repository owner.

---

**Note**: This is a simplified epidemiological model designed for educational purposes. It should not be used for real-world policy decisions without extensive validation and refinement.

## Netlify Deployment

Netlify cannot run the Streamlit server, so this repo ships a static build path. The Netlify build uses `scripts/build_static.py` to run a small, fixed simulation and publish the resulting charts and CSVs as a static site.

- Build command: `python -m pip install -r requirements.txt && python scripts/build_static.py`
- Publish directory: `docs`
- Customize the snapshot by editing `DEFAULT_COUNTRIES`, `DEFAULT_START_DATE`, `DEFAULT_END_DATE`, and `DEFAULT_SAMPLE_RATIO` in `scripts/build_static.py`.

If you want the interactive UI, deploy `streamlit_ui.py` to Streamlit Community Cloud, Render, or another Python host instead of Netlify.

## GitHub Pages

Run `python scripts/build_static.py` to precompute the outputs into `docs/`, then commit the `docs/` folder and set GitHub Pages to serve from the `/docs` directory on your default branch.
