import re


def viewed_movies(path):
    f = open(path, 'r')
    movies = f.readlines()
    not_series = []
    for movie in movies:
        if re.search("season|serie|volume", movie, re.IGNORECASE) == None:
            m = movie.split(',')[0].strip('\"')
            not_series.append(m)
    f.close()
    return not_series


def ids_of_movies(path):
    f = open(path, 'r')
    lines = f.readlines()
    all_movies = {}
    for movie in lines:
        content_type = movie.split("\t")[1]
        if content_type == 'movie':
            _id = movie.split("\t")[0]
            m = movie.split("\t")[2].strip().lower()
            if all_movies.get(m) == None:
                all_movies[m] = [_id]
            else:
                all_movies[m].append(_id)
    return all_movies


def rating_of_movies(path):
    f = open(path, 'r')
    lines = f.readlines()
    all_ratings = {}
    for movie in lines:
        _id = movie.split("\t")[0]
        rating = movie.split("\t")[1]
        number = movie.split("\t")[2]
        all_ratings[_id] = (float(rating), int(number.strip()))
    return all_ratings


def get_rating_of_most_voted(name, ratings, ids):
    name_ids = ids.get(name.strip().lower())
    rating = 0.0
    if name_ids == None:
        return None
    elif len(name_ids) == 1:
        _id = name_ids[0]
        (rating, _) = ratings.get(_id)
    else:
        highest_votes = 0
        for name_id in name_ids:
            if ratings.get(name_id) == None:
                continue
            (_rating, votes) = ratings.get(name_id)
            if highest_votes < votes:
                highest_votes = votes
                rating = _rating
    return rating


def main():
    ids = ids_of_movies('./title.basics.tsv')
    vm = viewed_movies('./NetflixViewingHistory.csv')
    ratings = rating_of_movies('./title.ratings.tsv')
    all_ratings = list(
        map(lambda m: get_rating_of_most_voted(m, ratings, ids), vm))
    with_out_None = []
    for rating in all_ratings:
        if rating != None:
            with_out_None.append(rating)
    print('your avg is: ' + str(round(sum(with_out_None) / len(with_out_None), 2)))


main()
