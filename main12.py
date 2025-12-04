
import pandas as pd
import matplotlib.pyplot as plt


# MODULE 1: CLASSES (Object Oriented Part)
# Purpose: Define what a "Building" looks like

class MeterReading:
    def __init__(self, date, kwh):
        self.date = date
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = [] # List to hold readings
    
    def add_reading(self, date, kwh):
        new_reading = MeterReading(date, kwh)
        self.readings.append(new_reading)


# MODULE 2: DATA INGESTION
# Purpose: Read CSV files and clean them

def load_data(file_list):
    print("...Loading Data...")
    all_data = [] # Empty list to store our tables
    
    for filename in file_list:
        try:
            # Read the CSV
            df = pd.read_csv(filename)
            
            # Create a Building Name from the filename
            # e.g., "library_block.csv" becomes "Library Block"
            name = filename.replace('.csv', '').replace('_', ' ').title()
            df['Building'] = name
            
            # Add to our list
            all_data.append(df)
            print(f"Read success: {filename}")
            
        except Exception as e:
            print(f"Could not read {filename}: {e}")
            
    # Combine everything into one big table
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Fix the Date column to be real dates (not just text)
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    
    return combined_df


# MODULE 3: ANALYSIS
# Purpose: Calculate the math and stats

def calculate_stats(df):
    print("...Calculating Stats...")
    
    # Total usage per day (for the Trend Line)
    daily_totals = df.groupby('Date')['KWh'].sum()
    
    # Summary per building (Mean, Max, Total)
    b_summary = df.groupby('Building')['KWh'].agg(['mean', 'max', 'sum'])
    
    return daily_totals, b_summary


# MODULE 4: VISUALIZATION
# Purpose: Draw the charts

def create_charts(df, daily_data, building_summary):
    print("...Drawing Charts...")
    
    # Create a layout with 3 rows
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))
    
    # 1. Trend Line
    ax1.plot(daily_data.index, daily_data.values, marker='o')
    ax1.set_title('Total Daily Energy Usage')
    ax1.set_ylabel('KWh')
    ax1.grid(True)
    
    # 2. Bar Chart
    names = building_summary.index
    averages = building_summary['mean']
    ax2.bar(names, averages, color='green')
    ax2.set_title('Average Usage by Building')
    
    # 3. Scatter Plot
    # We plot each building separately to get different colors
    for name in df['Building'].unique():
        subset = df[df['Building'] == name]
        ax3.scatter(subset['Date'], subset['KWh'], label=name)
    ax3.legend()
    ax3.set_title('Peak Usage Events')
    
    plt.tight_layout()
    plt.savefig('dashboard_modular.png')
    print("Chart saved as 'dashboard_modular.png'")


# MODULE 5: REPORTING
# Purpose: Save the final text and CSVs

def generate_report(df, building_summary):
    print("...Generating Report...")
    
    # Calculate key facts
    total_energy = df['KWh'].sum()
    top_building = building_summary['sum'].idxmax()
    
    # Create the text
    summary_text = f"""
    FINAL EXECUTIVE SUMMARY
    =======================
    Total Energy Consumed: {total_energy} KWh
    Highest Consuming Building: {top_building}
    """
    
    # Save to file
    with open('summary.txt', 'w') as f:
        f.write(summary_text)
        
    # Save cleaned data
    df.to_csv('cleaned_energy_data.csv', index=False)
    building_summary.to_csv('building_summary.csv')
    
    print(summary_text)


# MAIN EXECUTION
# This is where we run the modules in order


# 1. Define our files
my_files = ['library_block.csv', 'science_block.csv']


final_df = load_data(my_files)

if not final_df.empty:
    daily_stats, building_stats = calculate_stats(final_df)
    
    create_charts(final_df, daily_stats, building_stats)
    
    generate_report(final_df, building_stats)
    
    # OOP Check (Just to prove we did Task 3)
    lib = Building("Library")
    print("OOP System Ready.")
else:
    print("Something went wrong, no data loaded.")
