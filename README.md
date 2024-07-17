# Movie Recommendation App

## STILL IN PROGRESS
I used a dataset from Kaggle with information from __ movies and __ users.
[Dataset](https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system)
I used Django to store the information in a sqlite file and Vue.js as a frontend for a user to easily select movies.
In my intro to ML class, we discussed Collaborative Filtering methods and I love film so I thought it would be a good project to make a recommender system.
Just like with Netflix, you must select several movies you like and in my case rate them on a scale of 5 to make prediction easier.
Then, it will showcase recommendations as well as some stats about you (which genres you like)
Simulating watching a movie, you can select a movie and rate it and it will update its predictions.

Currently, I am reading the movies into the frontend and sending back the movies I've seen/rated into my User. I've just started the actual recommendation part using kNN algorithm.
