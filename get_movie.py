import argparse
import csv


def arguments():

    """
    The arguments that we will use on the command line
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--N',
                        type=int,
                        metavar='<n>',
                        help='How many movies do u want to see?')

    parser.add_argument('-g', '--genres',
                        type=str,
                        metavar='<genres>',
                        help='What genre of movies do u prefer?')

    parser.add_argument('-yf', '--year_from',
                        type=int,
                        metavar='<year_from>',
                        help='What year should I choose a movie from?')

    parser.add_argument('-yt', '--year_to',
                        type=int,
                        metavar='<year_to>',
                        help='What year should I choose a film for?')

    parser.add_argument('-r', '--regexp',
                        type=str,
                        metavar='<regexp>',
                        help='What should be in the title of the movie?')

    args = parser.parse_args()

    return args


def add_year(movieData):

    """
    Moving the year of release from the 'title' of the film to a separate place 'year'
    :param movieData: data about films with their rating
    :return:
    """

    for row in movieData:
        row['title'] = row['title'].strip()
        try:
            row['year'] = int(row['title'][-5:-1])
            row['title'] = row['title'][:-7]
        except:
            row['year'] = None

    return movieData


def add_rating(movieData, ratingData):

    """
    Adding a 'rating' to the movie data

    :param movieData
    :param ratingData
    :return: movieData: movie data with 'rating'
    """

    movie_id = {row['movieId']: [0, 0] for row in movieData}

    lst_movieId = []

    for row in ratingData:
        if row['movieId'] in movie_id:
            movie_id[row['movieId']][0] += float(row['rating'])
            movie_id[row['movieId']][1] += 1

    for k, v in movie_id.items():
        if v[1] != 0:
            movie_id[k] = round(v[0] / v[1], 1)
        else:
            movie_id[k] = None

    for row in movieData:
        for k, v in movie_id.items():
            if row['movieId'] == k:
                row['rating'] = v

    return movieData


def genre_filter(movieData, genres):

    """
    Filtering movieData by 'genres'

    :param movieData
    :param genres
    :return: filtered_data: Movies from the movieData with the specified genres
    """

    filtered_data = []
    genres = genres.split('|')

    for row in movieData:
        for genre in genres:
            if genre in row['genres'].split('|'):
                filtered_data.append(row)

    return filtered_data


def year_filter(movieData, year_from=None, year_to=None):

    """
    Filtering movieData by 'year'

    :param movieData:
    :param year_from: The minimum year of release of the film
    :param year_to: The maximum year of release of the film
    :return: filtered_data: Movies from the movieData with the specified release year
    """

    filtered_data = []

    for row in movieData:

        if row['year']:

            if year_to and year_from:
                if row['year'] >= year_from and row['year'] <= year_to:
                    filtered_data.append(row)

            elif year_to and not year_from:
                if row['year'] <= year_to:
                    filtered_data.append(row)

            elif not year_to and year_from:
                if row['year'] >= year_from:
                    filtered_data.append(row)

        else:
            continue

    return filtered_data


def regexp_filter(movieData, regexp):

    """
    Filtering movieData for the presence of a certain word in the 'title'

    :param movieData:
    :param regexp: Mandatory word in the title of the film
    :return: filtered_data: Movies with a specific word in the 'title'
    """

    filtered_data = []

    for row in movieData:
        if regexp in row['title']:
            filtered_data.append(row)

    return filtered_data


def output(movieData, genres=None, n=None):

    """
    Here the correct data output is formed

    :param movieData:
    :param genres:
    :param n:
    :return:
    """

    if genres:
        genres.split('|')
    else:
        genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary',
                  'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
                  'Sci-Fi', 'Thriller', 'War', 'Western']

    print('genre,title,year,rating')

    for i in genres:
        j = 0
        for row in movieData:
            if i in row['genres']:
                print(i + ',' + row['title'] + ',' + row['year'] + ',' + row['rating'])
                j += 1
            if j == n:
                break


def main():

    args = arguments()

    with open('movies.csv', 'r') as movie:
        movie_data = csv.DictReader(movie)

        movie_data = add_year(movie_data)

        if args.genres:
            movie_data = genre_filter(movie_data, args.genres)

        if args.year_from or args.year_to:
            movie_data = year_filter(movie_data, args.year_from, args.year_to)

        if args.regexp:
            movie_data = regexp_filter(movie_data, args.regexp)

        with open('ratings.csv', 'r') as rating:
            rating_data = csv.DictReader(rating)

            movie_data = add_rating(movie_data, rating_data)

        output(movie_data, args.genres, n=args.N)


if __name__ == '__main__':
    main()
