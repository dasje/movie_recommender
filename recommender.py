import requests
import json


def get_movies_from_tastedive(media_name):
    '''Import similar movies from tastedive based on a movie name'''
    link = 'https://tastedive.com/api/similar'
    params = {'q': media_name, 'type': 'movies', 'limit': '5'}
    obj = requests.get(link, params)
    answer = obj.json()
    return answer


def extract_movie_titles(media_dict):
    '''Extract to list the names of the movies from get_movies_from_tastedive'''
    name_list = []
    try:
        name_list = [item['Name'] for item in media_dict['Similar']['Results']]
    except KeyError:
        print('Too many attempts, try later.')
    return name_list


def get_related_titles(movie_list):
    '''Create list of movies related to movies in list created by extract_movie_titles'''
    long_movie_list = []
    for x in movie_list:
        new_dict = get_movies_from_tastedive(x)
        new_list = extract_movie_titles(new_dict)
        for y in new_list:
            if y not in long_movie_list:
                long_movie_list.append(y)
    return long_movie_list


def get_movie_data(movie_title):
    '''Import movie data from OMDB'''
    murl = 'http://www.omdbapi.com/'
    params = {'apikey': 'e3c0e48', 't': movie_title, 'r': 'json'}
    obj = requests.get(murl, params)
    results = obj.json()
    return results


def get_movie_rating(omdb_dict):
    '''Extract RottenTomato movie ratings from OMDB movie data'''
    rot_tom_rates = []
    try:
        for x in omdb_dict['Ratings']:
            rot_tom_rates.append(x['Source'])
    except KeyError:
        print('Key Error')
    if 'Rotten Tomatoes' in rot_tom_rates:
        rot_tom_rate = [x['Value'] for x in omdb_dict['Ratings'] if x['Source'] == 'Rotten Tomatoes']
        rot_tom_rate = int(rot_tom_rate[0].replace('%', ''))
        return rot_tom_rate
    else:
        return 0


def get_sorted_recommendations(movie_list):
    '''Sort the recommendations from get_related_titles by RottenTomato ratings'''
    complete_movie_list = []
    complete_movie_ratings = []
    # take item from movie_list
    for movie in movie_list:
    # extract_movies(getmovies(movie from movie_list))
    # join resulting lists in complete_movie_list
        movies = extract_movie_titles(get_movies_from_tastedive(movie))
        for movie in movies:
            complete_movie_list.append(movie)
    # take item from complete_movie_list
    for movie in complete_movie_list:
    # get_movie_rating(get_movie_data(item from complete_movie_list))
    # append to complete_movie_ratings
        complete_movie_ratings.append(get_movie_rating(get_movie_data(movie)))
    # zip complete_movie_list and complete_movie_ratings
    new_list = zip(complete_movie_ratings, complete_movie_list)
    # sort list by number and reverse
    new_list = sorted(new_list, key = lambda x: x[0], reverse = True)
    new_lists = [x[1] for x in new_list]
    return new_lists



test_list = ['Bridesmaids', 'Sherlock Holmes', 'The Goonies', 'Tenet', 'Batman Begins']
sixth = get_sorted_recommendations(test_list)
print(sixth)
