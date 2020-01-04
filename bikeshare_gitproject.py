import time
import pandas as pd

print('Hi! Let\'s explore some bikeshare data :)')

bike_data = { 'chicago': pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/chicago.csv'),
              'new york': pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/new_york_city.csv'),
              'washington': pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/washington.csv') }

def get_filters():
    city = get_city()
    month = get_month()
    day = get_day()
    return [city, month, day]

#city input from user
def get_city():

    print('We have bikeshare data on three US cities: Chicago, New York and Washington.')
    time.sleep(1)
    print('Which CITY would you like to analyze?')
    time.sleep(1)

    while True:
        city = input('Your entry: ').lower()
        if city in (bike_data.keys()):
            print('Thanks! you have entered: ', city)
            time.sleep(1)
            return city
            break
        else:
            print('Whoops! That doesn\'t look right. Please re-enter')
            time.sleep(1)

#get month input from user
def get_month():

    print('\nWe have user data for the six months of January til June (inclusive)...')
    time.sleep(2)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    correct_entry = False
    print("\nWhat MONTH are you interested in? You can also type 'all' to analyze all months.")
    time.sleep(1)

    while not correct_entry:
        month = input('Your entry: ').lower()
        if month in months:
            correct_entry = True
            print('Thanks! You have entered: ', month)
            mo_idx = months.index(month)
            time.sleep(1)
        else:
            print('Whoops! That doesn\'t look right. Please re-enter')
            time.sleep(1)

    return(mo_idx)

#get day input from user
def get_day():

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday', 'all']
    correct_entry = False
    print("\nWhat DAY are you interested in? You can also type 'all' to analyze all days.")
    time.sleep(1)

    while not correct_entry:
        day = input('Your entry: ').lower()
        if day in days:
            correct_entry = True
            print('Thanks! You have entered: ', day)
            day_idx = days.index(day)
            time.sleep(1)
        else:
            print('Whoops! That doesn\'t look right. Please re-enter')
            time.sleep(1)

    return(day_idx)

#create a subset of available data based on user inputs
def load_data(city, month, day):

    #city filter
    if city == 'chicago':
        city_filter_df = pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/chicago.csv')
    elif city == 'new york':
        city_filter_df = pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/new_york_city.csv')
    else:
        city_filter_df = pd.read_csv('D:/BCNV/Documents/BCNV info/AMP projects/Python project/washington.csv')

    #month filter
    if month != 0:
        month_filter_df = city_filter_df[pd.to_datetime(city_filter_df['Start Time'],format='%Y-%m-%d %H:%M:%S').dt.month==month]
    else:
        month_filter_df = city_filter_df

    #day filter
    if day < 7:
        day_filter_df = month_filter_df[pd.to_datetime(month_filter_df['Start Time'],format='%Y-%m-%d %H:%M:%S').dt.dayofweek==day]
    else:
        day_filter_df = month_filter_df

    return day_filter_df

#extract time stats
def time_stats(df):

    bike_data['Start Time'] = pd.to_datetime(df['Start Time'])
    bike_data['End Time'] = pd.to_datetime(df['End Time'])

    print('\nGenerating Time Stats...\n')
    start_time = time.time()

    # TO DO: display the most common month
    bike_data['Month'] = bike_data['Start Time'].dt.month
    most_common_month = bike_data['Month'].mode()[0]
    print("The most popular MONTH of the year is: %s\nNote: if you entered a month the value returned will be that month\'s value. Enter 'all' to see the most popular month\nkey: january = 1, february = 2... etc." %(most_common_month))

    # TO DO: display the most common day of week
    bike_data['Day'] = bike_data['Start Time'].dt.dayofweek
    most_common_day = bike_data['Day'].mode()[0] + 1
    print("The most popular DAY of the week is: %s\nNote: if you entered a day the value returned will be that day\'s value. Enter 'all' to see the most popular day\nkey: monday = 1, tuesday = 2... etc." %(most_common_day))

    # TO DO: display the most common start hour
    bike_data['Hour'] = bike_data['Start Time'].dt.hour
    most_common_hour = bike_data['Hour'].mode()[0]
    print("The most popular HOUR of the day is: %s\nNote: we use 24-hour time, e.g. '17' means 5pm" %(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#extract station stats
def station_stats(df):

    print('\nGenerating Station Stats...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most popular starting point is: ', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most popular ending point is: ', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    station_combos = df['Start Station'] + ' TO ' + df['End Station']
    most_common_trip = station_combos.mode()[0]
    print('The most popular trip is: ', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#extract trip stats
def trip_duration_stats(df):

    print('\nGenerating Trip Stats...\n')
    start_time = time.time()

    # TO DO: display total travel time
    bike_data['Minutes'] = bike_data['End Time'] - bike_data['Start Time']
    total_travel_time = bike_data['Minutes'].sum()
    print('Our bikes have been used a total of %s based on these inputs' %(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = bike_data['Minutes'].mean()
    print('The average travel time is %s based on these inputs' %(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#extract user stats
def user_stats(df):

    print('\nGenerating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    else:
        print('Sorry, there is no gender data available')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        oldest_user_born = int(df['Birth Year'].min())
        print('The oldest user was born in: ', oldest_user_born)
        youngest_user_born = int(df['Birth Year'].max())
        print('The youngest user was born in: ', youngest_user_born)
        typical_user_born = int(df['Birth Year'].mode()[0])
        print('The most common birth year of our users is: ', typical_user_born)
    else:
        print('Sorry, there is no birth year data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#ask if user wants to see raw data
def raw_data(df):
    rd_requests = 0

    while True:

        see_raw_data = input("\nWould you like to see 5 rows of raw user data? Enter 'yes' or 'no': ")

        rd_response = ['yes', 'no']

        if see_raw_data not in rd_response:
            print("Whoops! That doesn\'t look right. Please enter either 'yes' or 'no'")
        elif see_raw_data.lower() == 'no':
            print('\nNo raw data requested')
            break
        else:
            strt_row = 5 * rd_requests
            end_row = strt_row + 5
            if rd_requests == 0:
                print("\nOkay. Here\'s the first (most recent) 5 rows of data...\n")
                print(df.iloc[strt_row:end_row,:])
                rd_requests += 1
            else:
                print("\nOkay. Here\'s another 5 rows of data...\n")
                print(df.iloc[strt_row:end_row,:])
                rd_requests += 1


#bring it all together and determine run sequence
def main():
    while True:
        return_filters = get_filters()
        df = load_data(return_filters[0], return_filters[1], return_filters[2])
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a great day! We hope this has been helpful :)')
            break


if __name__ == "__main__":
	main()
