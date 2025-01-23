import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_hours_mins_secs(seconds):
    """Convert seconds to hours, minutes, and seconds."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")
    city = ""
    city_names = list(CITY_DATA.keys())
    while city not in city_names:
        city = input(f"Input name of city {city_names}: ").strip().lower()

    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                    'july', 'august', 'september', 'october', 'november', 'december']
    month = ""
    while month not in valid_months:
        month = input("Input month (e.g., 'all', 'january', ... , 'december'): ").strip().lower()

    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    while day not in valid_days:
        day = input("Input day (e.g., 'all', 'monday', ... , 'sunday'): ").strip().lower()

    print(f"\nFilters applied - City: '{city}', Month: '{month}', Day: '{day}'")
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_path = CITY_DATA[city]
    df = pd.read_csv(file_path)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['Day'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Month' in df.columns:
        common_month = df['Month'].mode()[0]
        print(f"Most common month: {common_month.title()}")

    if 'Day' in df.columns:
        common_day = df['Day'].mode()[0]
        print(f"Most common day: {common_day.title()}")

    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f"Most common start hour: {common_hour} o'clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end_station}")

    common_trip = (df['Start Station'] + " -> " + df['End Station']).mode()[0]
    print(f"Most common trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    total_hours, total_mins, total_secs = get_hours_mins_secs(total_travel_time)
    print(f"Total travel time: {total_hours}h {total_mins}m {total_secs}s")

    mean_travel_time = df['Trip Duration'].mean()
    mean_hours, mean_mins, mean_secs = get_hours_mins_secs(mean_travel_time)
    print(f"Mean travel time: {mean_hours}h {mean_mins}m {mean_secs}s")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("\nUser Types:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender Distribution:")
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print(f"\nEarliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("No birth year data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays raw data in increments of 5 rows."""
    start_row = 0
    while True:
        show_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if show_data == 'yes':
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
            if start_row >= len(df):
                print("\nNo more data to display.")
                break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter yes or no.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data found for the selected filters.")
        else:
            display_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? ^^ Enter yes or no: ').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
