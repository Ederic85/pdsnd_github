import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('city to explore (chicago, new york city, washington): ').lower()
    
    while city not in CITY_DATA:
        city = input('Input not applicable, please enter a valid city to explore (chicago, new york city, washington): ')

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('filter results by month (all, january, february, ... , june): ').lower()
    
    while month not in months:
        month = input('Input not applicable, please enter a valid moth to explore (all, january, february, ... , june): ')
    
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('filter results by day (all, monday, tuesday, ... sunday): ').lower()

    while day not in days:
        day = input('input not applicable, (all, monday, tuesday, ... sunday): ')
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # write df to Excel Sheet
    #df.to_excel("output_whole.xlsx")
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # write df to Excel Sheet
    #df.to_excel("output_with_StartTime.xlsx")
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common Month:', months[most_common_month - 1])
    
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common Day:', most_common_day)

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common End Station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['stations combined'] = df['Start Station'] + ' | ' + df['End Station']
    most_common_comb_station = df['stations combined'].mode()[0]
    print('Most common combined stations :', most_common_comb_station)

    #write df to Excel Sheet
    #df.to_excel("output.xlsx")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    travel_time = df['Travel Time'].sum()
    print('Total Travel Time:', travel_time)
    
    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].nunique()
    print('Counts of User Types:', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_counts, '\n')
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_date_of_birth = df['Birth Year'].min()
        most_recent_date_of_birth = df['Birth Year'].max()
        most_common_date_of_birth = df['Birth Year'].mode()[0]
        print('Date of Birth (Oldest User):', earliest_date_of_birth)
        print('Date of Birth (Youngest User):', most_recent_date_of_birth)
        print('Date of Birth (Most Common):', most_common_date_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        row = 0
        end_row = row + 5
        display_raw_data = input('do you want to display raw data from your query (yes or no): ').lower()
        while display_raw_data == 'yes':
            if row < 5:
                print(df.head(end_row))
                display_raw_data = input('display more? (yes or no): ').lower()
                row += 5
                end_row += 5
            else:
                print(df.iloc[row:end_row])
                display_raw_data = input('display more? (yes or no): ').lower()
                row += 5
                end_row += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
