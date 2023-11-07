import time
import pandas as pd

#Global variables

#Dictionary for the cities the user will want to discover.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
#end Global variables

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #Return variables.
    #city, month, day

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input("Would you like to see data for Chicago, New York City, or Washington? \n")

        #Force the import to be lower case to make input case insensitive
        city=city.lower()

        if(city in CITY_DATA):
            break
        else:
            print("Sorry that was not a valid city. \n")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Would you filter by month for the city of " + city.title() + "? Type \"all\" for no time filter \n")

        # Force the import to be lower case to make input case insensitive
        month = month.lower()

        if (month in months):
            break
        else:
            print("Sorry that was not a valid month. \n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Please type the day or \"all\" to see all days of the week \n")

        # Force the import to be lower case to make input case insensitive
        day = day.lower()

        if (day in days):
            break
        else:
            print("Sorry that was not a valid day of the week. \n")

    print('-'*50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    #Convert Start Time to a datetime object so the month and day can be extracted easier.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract the of month and day
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour

    #If the user specified a month and/or day of the week, filter the results to the user input.
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        day = days.index(day)
        df = df[df['Weekday'] == day]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        df: Pandas data frame you wish to work with.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month is: ', df['Month'].mode()[0])

    # display the most common day of week
    print('Most Common Day of the week is: ', df['Weekday'].mode()[0])

    # display the most common start hour
    print('Most Common Hour is: ', df['Hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        df: Pandas data frame you wish to work with.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print('The most commonly used start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print('\nThe most commonly used end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print('\nThe most frequent combination of trips are from', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        df: Pandas data frame you wish to work with.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()

    # Divide by 60 get the minute total, then mod to get the remaining seconds.
    minutes = total_duration // 60
    seconds = total_duration % 60

    hours = minutes // 60

    # Now that the hours have been calculated, mod to get the remaining minutes.
    minutes = minutes % 60

    print(f"The total trip duration is {hours} hours, {minutes} minutes and {seconds} seconds.")

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())

    minutes = average_duration // 60
    seconds = average_duration % 60

    # If the minutes is over 60, format the print out to include the hours.
    if minutes > 60:
        hours = minutes // 60

        # Now that the hours have been calculated, mod to get the remaining minutes.
        minutes = minutes % 60

        print(f"\nThe average trip duration is {hours} hours, {minutes} minutes and {seconds} seconds.")
    else:
        print(f"\nThe average trip duration is {minutes} minutes and {seconds} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        df: Pandas data frame you wish to work with.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")

    # Display counts of gender
    # Otherwise that notify the user that the gender column is absent.
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])

        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def display_raw_data(df):
    """
    Displays 5 lines of raw data at a time.
    Args:
        df: Pandas data frame you wish to work with.
    """

    response = ""
    i = 1

    while response.lower() != 'no':
        response = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')

        if response.lower() == 'yes':
            # print current 5 lines
            print(df[i:i + 5])

            # increase index i by 5 to print next 5 lines in new execution
            i = i + 5
        elif response.lower()!= ('no'):
            #filtering out bad responses.
            print('Yes or no are the only accepted responses\n')

    print('-'*50)
    
def main():
    while True:
        #Get the city, month, and day from the user.
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #After the user input has been validated, get the stats from the databases.
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()