import pandas as pd

df = pd.read_csv(r'C:\Users\YourUsername\Downloads\2024-09-18-data_export.csv')

#Check first 5 rows
print(df.head())

# Convert 'Start Time' to datetime to ensure proper grouping by day
df['Start Time'] = pd.to_datetime(df['Start Time'], format='mixed').dt.date

#Convert to numberic for calculating
df['PeakEPS'] = pd.to_numeric(df['PeakEPS'], errors='coerce')
df['AverageEPS'] = pd.to_numeric(df['AverageEPS'], errors='coerce')
 
# For each day, insert a row with the total value
df_total_rows = pd.DataFrame()
 
# Iterating over unique dates and adding total rows
for date in df['Start Time'].unique():
    # Filter the data for the specific date
    df_day = df[df['Start Time'] == date]
    # Create a new row for the total
    total_row = pd.DataFrame({
        'Start Time': [date],
        'Hostname': ['Total'],
        'PeakEPS': [df_day['PeakEPS'].sum()],
        'AverageEPS': [df_day['AverageEPS'].sum()]
    })

    # Append the rows of the day and the total row
    df_total_rows = pd.concat([df_total_rows, df_day, total_row], ignore_index=True)

    # Create the threshold row to be inserted after the total row
    threshold_row = pd.DataFrame({
        'Start Time': [date],
        'Hostname': ['Threshold'],
        'PeakEPS': [8600],
        'AverageEPS': [8600]
    })
    
    # Append the threshold row right after the total row
    df_total_rows = pd.concat([df_total_rows, threshold_row], ignore_index=True)
 
# Save the new dataframe with the total rows to a CSV file
output_file_path = r'C:\Users\YourUsername\Downloads\new_export.csv'
df_total_rows.to_csv(output_file_path, index=False)
 
output_file_path