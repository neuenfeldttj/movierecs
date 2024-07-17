<template>
    <div>
      <h1>Movie List</h1>
      <div v-if="loading">
        <p>Loading Movies...</p>
      </div>
      <div v-else>
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
        ratedMovies: []
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
            console.log(this.ratedMovies);
            axios.post('http://localhost:8000/api/rated-movies/', this.ratedMovies)
            .then(response => {
                console.log('Movies submitted successfully:', response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
  }
  </script>