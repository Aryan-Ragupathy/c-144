from flask import Flask,jsonify,request
import csv
from demographic import output
from content import get_recommendations

all_movies=[]
liked_movies=[]
not_liked_movies=[]
did_not_watch=[]

with open("final.csv") as f:
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:]

app=Flask(__name__)

@app.route("/get-movie")
def get_movie():
    movie_data={
        "title":all_movies[0][19],
        "poster_link":all_movies[0][27],
        "release_date":all_movies[0][13],
        "duration":all_movies[0][15],
        "rating":all_movies[0][20],
        "overview":all_movies[0][9]
    }
    return jsonify({
        "data":movie_data
    })

@app.route("/liked-movie",methods=["POST"])
def liked_movie():
    movie=all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status":"success"
    })

@app.route("/not-liked-movie",methods=["POST"])
def not_liked_movie():
    movie=all_movies[0]
    not_liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status":"success"
    })

@app.route("/did-not-watch",methods=["POST"])
def not_watched():
    movie=all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status":"success"
    })

@app.route("/popular-movies")
def popular_movies():
    movie_data=[]
    for movie in output:
        data={
            "title":movie[0],
            "poster_link":movie[1],
            "release_date":movie[2],
            "duration":movie[3],
            "rating":movie[4],
            'overview':movie[5]
        }
        movie_data.append(data)
    return jsonify({
        "data":movie_data
    })

@app.route("/recommended-movies")
def recommendation():
    all_recommended=[]
    for i in liked_movies:
        output=get_recommendations[i[19]]
        for j in output:
            all_recommended.append(j)
    import itertools
    all_recommended.sort()
    all_recommended=list(i for i in itertools.groupby(all_recommended))
    movie_data=[]
    for movie in all_recommended:
        data={
            "title":movie[0],
            "poster_link":movie[1],
            "release_date":movie[2],
            "duration":movie[3],
            "rating":movie[4],
            'overview':movie[5]
        }
        movie_data.append(data)
    return jsonify({
        "data":movie_data
    })

app.run()