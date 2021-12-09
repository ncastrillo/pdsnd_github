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
    city = ""
    month = ""
    day = ""
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Select a city (chicago, new york city or washington): ")
        city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'):
        month = input("Select a month to analize (all, january, february, ... , june, july, ..., december): ")
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input("Select a day of week to analize (all, monday, tuesday, ... , sunday): ")
        day = day.lower()

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
    df['city'] = city
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # extract hour from the Start Time column to create an hour column
    df['start_hour'] = df['Start Time'].dt.hour
    
    # extract combinations of Start and End statios to create an hour column
    df['StartEnd Stations'] = df['Start Station']+" -> "+df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
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

    print('\nCalculating The Most Frequent Times of Travel for the filters selected...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month (from 1 to 12) is: ', most_common_month)
    list_month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    print('\t which is: ', list_month[most_common_month-1])

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: ', most_common_day)

    # TO DO: display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print('The most common start hour (from 0 to 23) is: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: ', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df['StartEnd Stations'].mode()[0]
    print('The most frequent combination of start station and end station trip: ', most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time for selected filters: ', total_time, 'seconds.')
    # get days, hours, mins and seconds of the total_seconds
    mmt, sst = divmod(int(total_time), 60)
    hht, mmt= divmod(mmt, 60)
    ddt, hht= divmod(hht, 24)
    print('\t which are: ', ddt, 'Days', hht, 'Hours', mmt, 'Minutes', sst, 'Seconds')

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time for selected filters: ', mean_time, 'seconds.')
    # get days, hours, mins, seconds
    mm, ss = divmod(int(mean_time), 60)
    hh, mm= divmod(mm, 60)
    dd, hh= divmod(hh, 24)
    print('\t which are: ', dd, 'Days', hh, 'Hours', mm, 'Minutes', ss, 'Seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types: \n', user_types)
    print('\n')
    
    # TO DO: Display counts of gender
    if df['city'].max() == 'washington':
        print('The washington dataset doesn\'t have Gender and Birth Year data')
    else:
        gender_count = df['Gender'].value_counts()
        print('Counts of gender: \n', gender_count)
        print('\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        birth_earliest = df['Birth Year'].min()
        print('The earliest year of birth is: ', birth_earliest)
        birth_recent = df['Birth Year'].max()
        print('The most recent year of birth is: ', birth_recent)
        birth_common = df['Birth Year'].mode()[0]
        print('The most common year of birth is: ', birth_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rows_data(df):
    st = 0
    more_data = input('\nWould you like to see the data? Enter yes or no.\n')
    while more_data.lower() == 'yes':
        df_slice = df.iloc[st: st+5]
        print(df_slice)
        st += 5
        more_data = input('\nWould you like to see 5 rows more of data? Enter yes or no.\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
      
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        rows_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()