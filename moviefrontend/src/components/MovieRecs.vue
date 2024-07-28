<template>
    <div>
      <h1>Movie List</h1>
      <div v-if="loading">
        <p>Loading Movies...</p>
      </div>
      <div v-else class="container">
        <div class="left">
        <select v-model="selectedMovies" multiple="true">
            <option v-for="movie in movies" :key="movie.id" :value="movie.title">{{ movie.title }}</option>
         </select>
         <div v-for="(m, i) in ratedMovies" :key="i">
            <p>{{ m.title }}</p>
            <label for="ratingInput">Rating:</label>
            <input
            type="number"
            v-model.number="m.rating"
            step="0.5"
            min="1"
            max="5"
            />
         </div>
         <button @click="sendMovies()">Update</button>
         </div>
         <div class="right">
         <select v-model="predictedMovie">
            <option v-for="movie in movies" :key="movie.id" :value="movie.title">{{ movie.title }}</option>
         </select>
         <button @click="predMovie()">Predict</button>
         </div>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        movies: [],
        loading: true,
        selectedMovies: [],
        ratedMovies: [],
        predictedMovie: null
      }
    },
    mounted() {
      axios.get('http://localhost:8000/api/movies/')
        .then(response => {
          this.movies = response.data;
          this.loading = false;
        })
        .catch(error => console.error('Error:', error));
    },

    watch: {
        selectedMovies(newMovies) {
            this.ratedMovies = newMovies.map(title => {
                const exists = this.ratedMovies.find(movie => movie.title === title);
                return {
                    title,
                    rating: exists ? exists.rating : 0
                };
            });
        }
    },

    methods: {
        sendMovies() {
            axios.post('http://localhost:8000/api/rated-movies/', this.ratedMovies)
            .then(response => {
                console.log('Movies submitted successfully:', response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        predMovie() {
            axios.post('http://localhost:8000/api/predict-movie/', {title: this.predictedMovie})
            .then(response => {
                console.log('Movie submitted successfully:', response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
  }
  </script>
  <style scoped>
  .container {
    display: grid;
    grid-template-areas: "left right";
    width: 100vw;
    height: 100vh;
  }
  .left {
    grid-area: left;
    width:50vw;
  }
  .right {
    grid-area: right;
  }
</style>