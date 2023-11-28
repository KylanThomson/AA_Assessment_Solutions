import pandas as pd

# Function to extract revenue
def extract_revenue(product_list):
    if pd.isna(product_list):
        return None
    parts = product_list.split(';')
    if len(parts) > 3:
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

    # Merge DataFrames on 'visitor_id'
    joined_df = pd.merge(visitor_activity, ab_testing_data, on='visitor_id', how='inner')
    print("\nJoined DataFrame:\n", joined_df.head(), "\n")

    # Define the list of page names where guests search for flights
    page_names = ['shopping:matrixavailability', 'shopping:bundledavailability', 'shopping:calendaravailability']

    # Unique visitor search activities
    unique_searches = (visitor_activity[visitor_activity['pagename'].isin(page_names)].drop_duplicates(subset=['visitor_id', 'product_list']))
    print("\nSearches per visitor\n", unique_searches['visitor_id'].value_counts())

    # Apply the extract_revenue function to the dataframe
    joined_df['revenue'] = joined_df['product_list'].apply(extract_revenue)
    print("\nAdded Revenue Column:\n", joined_df.head())

    # Filter and deduplicate reservations
    made_reservation = joined_df[joined_df['pagename'] == 'booking:reservation']
    made_reservation = made_reservation.drop_duplicates(subset='purchaseid', keep='first')
    print(made_reservation)
    
    # Visitor count per variation that purchased a flight
    print("\nVisitor count per variation that purchased a flight:\n", made_reservation['variation'].value_counts())

    # Unique purchases per variation
    print("\nUnique Purchases per variation\n", made_reservation['variation'].value_counts())

    # Displaying unique visits per variation
    print("\nUnique Visits Per Variation:\n", ab_testing_data['variation'].value_counts())

    # Save the joined DataFrame with added revenue column to a new CSV file
    joined_df.to_csv('joined_data.csv', index=False)

if __name__ == "__main__":
    main()
