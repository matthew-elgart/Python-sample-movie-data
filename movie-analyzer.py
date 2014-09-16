'''
Created on Apr 3, 2014

@author: matthewelgart
'''
# general function for reading all three IMDB movie files
def readFile (filename):
    """
    given a filename that is formatted as tab separated values on each line
    return a list of lists of strings, where each line is represented
      as a list of separate string elements
    note, the header row is ignored
    """
    # some OSes need to know that the file might have some special characters
    f = open(filename)
    # convert reader to a list so we can close the file
    result = [ line.strip().split('\t') for line in f if len(line) > 1 ]
    # close the file so we do not take up extra system resources
    f.close()
    # throw away the header row(s) of the data
    return result[1:]


# general function for turning all three IMDB movie data into a dictionary
def processData (data, result):
    """
    given a list of lists of strings representing movie data,
    return a dictionary where
      key is a tuple of the movie's title and year
      value is the remaining information about the movie
    this function is parameterized in three additional ways:
      titleIndex is the index of the title in each list of movie information
      yearIndex is the index of the year in each list of movie information
      result is a dictionary in which to add this data
    """
    TITLE = 1
    YEAR = 2
    for d in data:
        # create key by using the given indices to find the title and year
        key = (d[TITLE].strip(), d[YEAR].strip())
        # create value from the remaining elements in the information list
        value = d[0:TITLE] + d[YEAR+1:]
        # add data to dictionary
        if key not in result:
            result[key] = []
        result[key] += value
        # OR:
        # result[key] = result.get(key, []) + value
    return result


# use this function to print the results of your functions
def printData (data):
    """
    prints the length and sorted contents of the sequence
    """
    print(str(len(data)) + '\t' + str(data))


def bothTopRatedAndGrossing (movies):
    """
    return a dictionary in the same format as the one given, but that
      includes only those movies that are both top rated and top grossing
    """
    result = {}
    for (k, v) in movies.items():
        # note, only movies that have all fields are in both
        #   (7 for cast + 2 for rating + 2 for gross)
        if len(v) == 11:
            result[k] = v
    return result


def uniqueDirectors (movies):
    """
    return list of strings, names of directors, sorted alphabetically
      for the given movies
    """
    # note, director guaranteed to be in the second spot in movie information list
    return sorted(set([ x[1] for x in movies.values() ]))


def directorsOfMostMovies (movies, count):
    """
    return list of tuples, (count, name), sorted by count from most to least of
      the directors and how many movies they directed
    note, only return the first "count" directors
    """
    directorCounts = {}
    for movieInfo in movies.values():
        key = movieInfo[1]
        if key not in directorCounts:
            directorCounts[key] = 0
        directorCounts[key] += 1
    return sorted([ (v, k) for (k,v) in directorCounts.items() ], reverse=True)[:count]
    # OR:
    # directors = [ x[1] for x in movies.values() ]
    # directorSet = set(directors)
    # return sorted([ (directors.count(d), d) for d in directorSet ], reverse=True)[:count]


def castFilmography (movies, minAppearances):
    """
    return list of lists, [ name, (title, year) ], sorted alphabetically by name
      the cast members that appeared in at least minAppearances movies
    """
    actors = {}
    for (k,v) in movies.items():
        for a in v[2:7]:
            actors[a] = actors.get(a, []) + [k]
    return sorted([ [k] + v for (k,v) in actors.items() if len(v) >= minAppearances ])


def uniqueCastMembers (movies):
    """
    return list of strings, names of cast members, sorted alphabetically
      that appeared in the given movies
    """
    actors = castFilmography(movies, 1)
    return sorted([ x[0] for x in actors ])
    # OR:
    # actors = set()
    # for v in movies.values():
    #     actors.add(v[2:7])
    # return sorted(actors)


def mostHighlyRatedCastMembers (movies, count, minAppearances):
    """
     return list of tuples, (average rating, name), sorted from greatest to least by rating
      of the top cast count cast members that appeared in at least minAppearances movies   
    """
    def getAverage (allMovies, castMovies):
        # return average rating for all movies in list castMovies
        ratings = [ float(allMovies[key][8]) for key in castMovies if float(allMovies[key][8]) < 10 ]
        numMovies = len(ratings)
        if numMovies > 0:
            return sum(ratings) / numMovies
        else:
            return 0
        # OR:
        # totalRating = 0
        # numMovies = 0
        # for key in castMovies: 
        #     rating = float(allMovies[key][8])  # rating or profit
        #     if rating < 10:                    # is a rating
        #         totalRating += rating
        #         numMovies += 1
        # if numMovies > 0:
        #     return totalRating / numMovies
        # else:
        #     return 0

    cast = castFilmography(movies, minAppearances)
    ratings = [ (getAverage(movies, castInfo[1:]), castInfo[0]) for castInfo in cast ]
    return sorted(ratings, reverse=True)[:count]


def mostProfitableDirectors (movies, count):
    """
    returns a list of tuples, (int money earned, string director name), 
      of length count, the directors whose movies made the most money
    """
    directors = {}
    for movieInfo in movies.values():
        key = movieInfo[0]               # director's name
        if len(movieInfo) == 10:
            value = float(movieInfo[9])  # profit
        else:
            value = float(movieInfo[7])  # rating or profit
        if value > 100:                  # not a rating
            if key not in directors:
                directors[key] = 0
            directors[key] += int(value)
    return sorted([(v, k) for (k,v) in directors.items() ], reverse=True)[:count]


def mostMoviesPerDecades (movies): 
    """
    returns a list of tuples, (number of movies, decade name) 
      for the given movies
    """
    movieDecades = {}
    for (title,year) in movies:
        key = year[:3]
        movieDecades[key] = movieDecades.get(key, 0) + 1
    return sorted([ (count, decade+'0s') for (decade,count) in movieDecades.items() ], reverse=True)
    # OR:
    # decades = [ k[1][:3]+'0s' for k in movies ]
    # return sorted([ (decades.count(d), d) for d in set(decades) ], reverse=True)



def mostTopBilled (movies, count):
    """
    given a dictionary whose definition is described above
    returns a list of tuples, (int, string), of length count, 
      the most times a cast member has been listed first in the movie's cast
    """
    # TODO: complete this function
    import operator
    topBilledDict = {}
    for (k,v) in movies.items():
        if v[2] not in topBilledDict:
            topBilledDict[v[2]] = 0
        topBilledDict[v[2]] += 1
    topBilledList = []
    for actor in topBilledDict:
        topBilledList += [(actor,topBilledDict[actor])]
    topBilledList = sorted(topBilledList)
    topBilledList = [(y,x) for (x,y) in topBilledList]
    topBilledList = sorted(topBilledList, key = operator.itemgetter(0), reverse = True)[:count]
    return topBilledList


def actorDirectorPairs (movies, count):
    """
    given a dictionary whose definition is described above
    returns a list of tuples, (int, (string, string)), of length count, 
      the most prolific pairs of director and cast member in movies
    """
    # TODO: complete this function
    import operator
    directorsDict = {}
    for (k,v) in movies.items():
        if v[1] not in directorsDict:
            directorsDict[v[1]] = []
        for actors in v[2:6]:
            directorsDict[v[1]] += [actors]
    actorDirectorList = []
    for director in directorsDict:
        for actor in set(directorsDict[director]):
            actorDirectorList += [((director, actor), directorsDict[director].count(actor))]
    actorDirectorList = [(y,x) for (x,y) in sorted(actorDirectorList)]
    actorDirectorList = sorted(actorDirectorList, key = operator.itemgetter(0), reverse = True)[:count]
    return actorDirectorList




# read data from files
# note, this file does not have a header row
cast = readFile("imdb_movies_cast.txt")
# note, these files have a header row
rated = readFile("imdb_movies_toprated.txt")
gross = readFile("imdb_movies_gross.txt")
# verify data that was read
#printData(cast)
#printData(rated)
#printData(gross)

# create separate dictionaries of just information from a specific file, where
#  key is a tuple of strings: (title, year)
#  values are a list of strings: [rank, director, actor1, actor2, actor3, actor4, actor5]
castMovies = processData(cast, {})
#  values are a list of strings: [rank, rating]
ratedMovies = processData(rated, {})
#  values is a list of strings: [rank, profits]
grossMovies = processData(gross, {})
# verify data that was read
#printData(castMovies)
#printData(ratedMovies)
#printData(grossMovies)

# combine results of processing data multiple times into ONE dictionary, where
#  key is a tuple of strings: (title, year)
#  values are a list of strings: [rank, director, actor1, actor2, actor3, actor4, actor5, X ]
#    where the last two or four elements are the rankings, rating, and/or profits
movies = {}
processData(cast, movies)
processData(rated, movies)
processData(gross, movies)
print("All movie data:")
printData(movies)

# answers to questions
'''print('Which movies are both top rated and top grossing?')
topMovies = bothTopRatedAndGrossing(movies)
printData(topMovies)

print('Who directed the movies that are either top rated or top grossing?')
directors = uniqueDirectors(movies)
printData(directors)

print('Who directed the movies that are both top rated and top grossing?')
directors = uniqueDirectors(topMovies)
printData(directors)

print('Top 10, by count, who directed the most movies that are either top rated or top grossing?')
prolificDirectors = directorsOfMostMovies(movies, 10)
printData(prolificDirectors)

print('Top 5, by count, who directed the most movies that are both top rated and top grossing?')
prolificDirectors = directorsOfMostMovies(topMovies, 5)
printData(prolificDirectors)

print('Who acted in at least 3 movies that are either top rated or top grossing?')
actors = castFilmography(movies, 3)
printData(actors)

print('Top 10, by count, who acted in the most movies that are either top rated or top grossing?')
prolificActors = [ x[0] for x in sorted(actors, key=len) ][:10]
printData(prolificActors)

print('Who directed and also starred in any movies that are either top rated or top grossing?')
directorAndActors = sorted(set(uniqueDirectors(movies)) & set(uniqueCastMembers(movies)))
printData(directorAndActors)

print('Top 20, by rating, who acted in any movies whose average rating is the highest?')
topActors = mostHighlyRatedCastMembers(movies, 20, 1)
printData(topActors)

print('Top 1, by rating, who acted in at least 4 movies whose average rating is the highest?')
topActors = mostHighlyRatedCastMembers(movies, 1, 4)
printData(topActors)

print('Top 10, by total, who directed the highest grossing movies?')
profitableDirectors = mostProfitableDirectors(movies, 10)
printData(profitableDirectors)

print('Which decades, from most to least, produced movies that are either top rated or top grossing?')
decades = mostMoviesPerDecades(movies)
printData(decades)

print('Which decades, from most to least, produced movies that are both top rated or top grossing?')
decades = mostMoviesPerDecades(topMovies)
printData(decades)'''

topBilledActors = mostTopBilled(movies, 5)
print(topBilledActors)

names = actorDirectorPairs(movies, 5)
print(names)
