import sqlite3
import objecttier

##################################################################  
# 
# get_stats
#
def get_stats(dbConn):
  print()
  print("General stats:")
  movies = objecttier.num_movies(dbConn)
  reviews = objecttier.num_reviews(dbConn)
  print("  # of movies:", f"{movies:,}")
  print("  # of reviews:", f"{reviews:,}")
  print()
##################################################################  
# 
# get_movie_info
#
def get_movie_info(dbConn):
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")
  print()
  movies = objecttier.get_movies(dbConn, name)
  
  if movies is None:  # error
    print("**Internal error: get_movies")
  elif len(movies) == 0:
    print("# of movies found:", f"{len(movies)}" )
  elif len(movies) > 100:
    print("# of movies found:", f"{len(movies)}" )
    print()
    print("There are too many movies to display, please narrow your search and try again...")
  else:
    print("# of movies found:", f"{len(movies)}" )
    print()
    for m in movies:
      print(m.Movie_ID, ":", 
            m.Title,
            f"({m.Release_Year})",)
##################################################################  
# 
# get_movie_details
#
def get_movie_details(dbConn):
  print()
  id = input("Enter movie id: ")
  print()
  movie_details = objecttier.get_movie_details(dbConn, id)

  if movie_details is None:  # error
    print("No such movie...")
  else:
    str1 = ""
    str2 = ""
    if len(movie_details.Genres) > 0:
      str1 = ","
    if len(movie_details.Production_Companies) > 0:
      str2 = ","
    print(movie_details.Movie_ID, ":", 
          f"{movie_details.Title}\n",
          f" Release date: {movie_details.Release_Date}\n",
          f" Runtime: {movie_details.Runtime} (mins)\n",
          f" Orig language: {movie_details.Original_Language}\n",
          f" Budget: ${movie_details.Budget:,} (USD)\n",
          f" Revenue: ${movie_details.Revenue:,} (USD)\n",
          f" Num reviews: {movie_details.Num_Reviews}\n",
          f" Avg rating: {(movie_details.Avg_Rating):.2f} (0..10)\n",
          f" Genres: {', '.join(movie_details.Genres)}{str1} \n",
          f" Production companies: {', '.join(movie_details.Production_Companies)}{str2} \n",
          f" Tagline: {movie_details.Tagline}",)
##################################################################  
# 
# get_top_N_movies
#
def get_top_N_movies(dbConn):
  print()
  N = int(input("N? "))
  if N < 1:
    print("Please enter a positive value for N...")
    print()
    return
  min_num_reviews = int(input("min number of reviews? "))
  if min_num_reviews < 1:
    print("Please enter a positive value for min number of reviews...")
    print()
    return
  top_N_movies = objecttier.get_top_N_movies(dbConn, N, min_num_reviews)
  print()
  
  if top_N_movies is None:  # error
    print("**Internal error: get_top_N_movies")
  else:
    for m in top_N_movies:
      print(m.Movie_ID, ":", 
            m.Title,
            f"({m.Release_Year}),",
            f"avg rating = {m.Avg_Rating:.2f}",
            f"({m.Num_Reviews} reviews)")
##################################################################  
# 
# insert_review
#
def insert_review(dbConn):
  print()
  rating = int(input("Enter rating (0..10): "))
  if rating < 0 or rating > 10:
    print("Invalid rating...")
    return
  id = input("Enter movie id: ")
  print()
  success = objecttier.add_review(dbConn, id, rating)
  if success == 1:
    print("Review successfully inserted")
  else:
    print("No such movie...")
##################################################################  
# 
# set_tagline
#
def set_tagline(dbConn):
  print()
  tagline = input("tagline? ")
  id = input("movie id? ")
  print()
  success = objecttier.set_tagline(dbConn, id, tagline)
  if success == 1:
    print("Tagline successfully set")
  else:
    print("No such movie...")
##################################################################  
# 
# MAIN OUTPUT BELOW
#
print('** Welcome to the MovieLens app **')
dbConn = sqlite3.connect('MovieLens.db')
get_stats(dbConn)
cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
      get_movie_info(dbConn)
    elif cmd == "2":
      get_movie_details(dbConn)
    elif cmd == "3":
      get_top_N_movies(dbConn)
    elif cmd == "4":
      insert_review(dbConn)
    elif cmd == "5":
      set_tagline(dbConn)
    else:
      print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

dbConn.close()
#
# done
#