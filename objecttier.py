# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

  def __init__(self, id, title, year):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:

  def __init__(self, id, title, year, num_rev, avg_rat):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = num_rev
    self._Avg_Rating = avg_rat

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

  def __init__(self, id, title, release_date, runtime, original_language,
               budget, revenue, num_reviews, avg_rating, tagline, genres,
               production_companies):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = release_date
    self._Runtime = runtime
    self._Original_Language = original_language
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = num_reviews
    self._Avg_Rating = avg_rating
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = production_companies

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  sql = """SELECT COUNT(Movie_ID) FROM Movies"""
  try:
    row = datatier.select_one_row(dbConn, sql, None)
    if row:
      return row[0]
    return 0
  except Exception as err:
    print("num_moves failed:", err)
    return -1
  finally:
    pass


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = """SELECT COUNT(Rating) FROM Ratings"""
  try:
    row = datatier.select_one_row(dbConn, sql, None)
    if row:
      return row[0]
    return 0
  except Exception as err:
    print("num_reviews failed:", err)
    return -1
  finally:
    pass


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by movie id;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """SELECT Movie_ID, Title, strftime('%Y', Release_Date) as Year FROM Movies WHERE Title LIKE ? ORDER BY Movie_ID ASC"""
  param = [pattern]
  try:
    rows = datatier.select_n_rows(dbConn, sql, param)
    movies = []
    if rows:
      for row in rows:
        movies.append(Movie(row[0], row[1], row[2]))
    return movies
  except Exception as err:
    print("get_movies failed:", err)
    return []
  finally:
    pass


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  sql = """SELECT Movies.Movie_ID, Title, date(Release_Date), Runtime, Original_Language, Budget, Revenue, COUNT(Ratings.Movie_ID), COALESCE(AVG(Rating), 0) as AVE, COALESCE(Tagline, "") AS Tagline FROM Movies LEFT JOIN Ratings On Movies.Movie_ID = Ratings.Movie_ID LEFT JOIN Movie_Taglines ON Movies.Movie_ID = Movie_Taglines.Movie_ID WHERE Movies.Movie_ID = ?"""
  sql2 = """SELECT Genre_Name FROM Genres LEFT JOIN Movie_Genres ON Genres.Genre_ID = Movie_Genres.Genre_ID WHERE Movie_Genres.Movie_ID = ? ORDER BY Genre_Name ASC"""
  sql3 = """SELECT Company_Name FROM Companies LEFT JOIN Movie_Production_Companies ON Companies.Company_ID = Movie_Production_Companies.Company_ID WHERE Movie_Production_Companies.Movie_ID = ? ORDER BY Company_Name ASC"""
  param = [movie_id]
  try:
    row = datatier.select_one_row(dbConn, sql, param)
    row2 = datatier.select_n_rows(dbConn, sql2, param)
    genre = []
    for r in row2:
      genre.append(str(r[0]))
    row3 = datatier.select_n_rows(dbConn, sql3, param)
    prod_comp = []
    for r in row3:
      prod_comp.append(str(r[0]))
    if row and row[0]:
      return MovieDetails(row[0], row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7], row[8], row[9], genre, prod_comp)
    else:
      return None
  except Exception as err:
    print("get_movie_details failed:", err)
    return None
  finally:
    pass


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  sql = """SELECT Movies.Movie_ID, Title, strftime('%Y', Release_Date) as Year, COUNT(Rating) AS Total, AVG(Rating) AS AVE FROM Movies LEFT JOIN Ratings On Movies.Movie_ID = Ratings.Movie_ID GROUP BY Movies.Movie_ID HAVING Total >= ? ORDER BY AVE DESC limit ?"""
  param = [min_num_reviews, N]
  try:
    rows = datatier.select_n_rows(dbConn, sql, param)
    movieRatings = []
    if rows:
      for row in rows:
        movieRatings.append(MovieRating(row[0], row[1], row[2], row[3],
                                        row[4]))
    return movieRatings
  except Exception as err:
    print("get_top_N_movies failed:", err)
    return []
  finally:
    pass


##################################################################
#
# add_review:
#F
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  sql = """SELECT Movie_ID FROM Movies WHERE Movie_ID = ?"""
  param = [movie_id]
  try:
    row = datatier.select_one_row(dbConn, sql, param)
    if row:
      sql = """INSERT INTO Ratings (Movie_ID, Rating) VALUES (?, ?)"""
      param = [movie_id, rating]
      success = datatier.perform_action(dbConn, sql, param)
      if success:
        return 1
    return 0
  except Exception as err:
    print("add_review failed:", err)
    return 0
  finally:
    pass


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  sql = """SELECT Movie_ID FROM Movies WHERE Movie_ID = ?"""
  sql2 = """SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = ?"""
  sql3 = """UPDATE Movie_Taglines SET [Tagline] = ? WHERE Movie_ID = ?"""
  sql4 = """INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?)"""
  param = [movie_id]
  try:
    row = datatier.select_one_row(dbConn, sql, param)
    if row:
      row = datatier.select_one_row(dbConn, sql2, param)
      if row:
        param = [tagline, movie_id]
        success = datatier.perform_action(dbConn, sql3, param)
      else:
        param = [movie_id, tagline]
        success = datatier.perform_action(dbConn, sql4, param)
      if success:
          return 1
    return 0
  except Exception as err:
    print("set_tagline failed:", err)
    return 0
  finally:
    pass