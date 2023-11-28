import pandas as pd

# Function to extract revenue
def extract_revenue(product_list):
    if pd.isna(product_list):
        return None
    parts = product_list.split(';')
    if len(parts) > 3:
        print('revenue')
        print(parts[3])
        return parts[3]
    return None

def main():
    # Reading the CSV files
    visitor_activity = pd.read_csv('Web Data Homework - Dataset 1.csv') 
    ab_testing_data = pd.read_csv('Experiment Decisions Homework - Dataset 2.csv') 


    # Displaying the first few rows of each dataframe
    print("Web Data Homework - Dataset 1.csv:")
    print(visitor_activity.head())
    print("\nExperiment Decisions Homework - Dataset 2.csv:")
    print(ab_testing_data.head())

    # Inner Join merging Web Data Homework - Dataset 1.csv with Experiment Decisions Homework - Dataset 2.csv on cisitor_id
    joined_df = pd.merge(visitor_activity, ab_testing_data, on='visitor_id', how='inner')

    # Displaying the joined DataFrame
    print("\nJoined DataFrame:")
    print(joined_df.head())

    # Define the list of page names where guests search for flights
    page_names = ['shopping:matrixavailability', 'shopping:bundledavailability', 'shopping:calendaravailability']

    # Creating a DataFrame of unique visitor search activities
    unique_df = (visitor_activity[visitor_activity['pagename'].isin(page_names)].drop_duplicates(subset=['visitor_id', 'product_list']))
    
    # Displaying searches per visitor
    print("\nSearches per visitor")
    print(unique_df['visitor_id'].value_counts())

    # Apply the extract_revenue function to the dataframe
    joined_df['revenue'] = joined_df['product_list'].apply(extract_revenue)

    # Filter the DataFrame to include only rows where 'pagename' is 'booking:reservation'
    # This creates a subset of the data where a booking reservation was made
    made_reservation = joined_df[joined_df['pagename'] == 'booking:reservation']

    # Remove duplicate entries based on 'purchaseid'
    # 'drop_duplicates' ensures each reservation is counted only once
    made_reservation = made_reservation.drop_duplicates(subset='purchaseid', keep='first')
    print(made_reservation)
    
    # Counting and displaying number of unique purchases per variation
    print("\nVisitor count per variation that purchased a flight:")
    print(made_reservation['variation'].value_counts())

    # Counting and displaying number of unique purchases per variation
    print("\nUnique Purchases per variation")
    print(made_reservation['variation'].value_counts())

    # Displaying unique visits per variation
    print("\nUnique Visits Per Variation:")
    print(ab_testing_data['variation'].value_counts())

    # Save the joined DataFrame to a new CSV file
    joined_df.to_csv('joined_data.csv', index=False)

if __name__ == "__main__":
    main()
