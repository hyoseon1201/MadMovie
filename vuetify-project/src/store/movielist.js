import {defineStore} from 'pinia'
import axios from 'axios'

export const useMovieListStore = defineStore('movielist', {
  state: () => ({
    movies: [],
    actors: [],
    movie: null,
  }),
  actions: {
    async recommendMovies() {
      try {
        const token = localStorage.getItem('token');

        const response = await axios.get('http://127.0.0.1:8000/movies/recommend/', {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });

        this.movies = response.data;
      } catch (error) {
        console.error('Error fetching recommended movies:', error);
      }
    },

    async genresMovies(genres) {
      const response = await axios.get(`http://127.0.0.1:8000/movies/list/?genres=${genres}`)
      this.movies = response.data
    },

    async searchMovies(search) {
      const response = await axios.get(`http://127.0.0.1:8000/movies/list/?search=${search}`)
      this.movies = response.data
    },

    async detailMovie(id) {
      const response = await axios.get(`http://127.0.0.1:8000/movies/${id}/`)
      this.movies = response.data
    },

    async actorList(id) {
      const response = await axios.get(`http://127.0.0.1:8000/actors/${id}/`)
      this.actors = response.data
    },

    async articleList(movie_id, page) {
      const response = await axios.get(`http://127.0.0.1:8000/articles/${movie_id}/?page=${page}`)
      this.articles = response.data.results
      this.total_pages = response.data.total_pages
    },

    async articleDetail(article_id) {
      const response = await axios.get(`http://127.0.0.1:8000/articles/${article_id}/detail/`)
      this.article = response.data
    },

    async articleCreate(articleData) {
      try {
        const token = localStorage.getItem('token');

        const response = await axios.post(`http://127.0.0.1:8000/articles/create/`, articleData, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });

        this.articles = response.data;
        return response.data; // 새 게시글 객체 반환
      } catch (error) {
        console.error('Error creating article:', error);
      }
    },


    async articleDelete(articleId) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.delete(`http://127.0.0.1:8000/articles/${articleId}/delete/`, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });

        // Get the deleted article from the response
        const deletedArticle = response.data;

        // Update the articles list by filtering out the deleted article
        this.articles = this.articles.filter(article => article.id !== articleId);

        // Return the deleted article data
        return deletedArticle;
      } catch (error) {
        console.error('Error deleting article:', error);
        return null; // Return null or handle the error as needed
      }
    },

    async articleUpdate(articleId, updateData) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.patch(`http://127.0.0.1:8000/articles/${articleId}/update/`, updateData, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });
        const updatedIndex = this.articles.findIndex(article => article.id === articleId);
        if (updatedIndex !== -1) {
          this.articles[updatedIndex] = {...this.articles[updatedIndex], ...response.data};
        }
      } catch (error) {
        console.error('Error updating article:', error);
      }
    },

    async commentUpdate(commentId, updateData) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.patch(`http://127.0.0.1:8000/articles/${commentId}/comment/update/`, updateData, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });
        const updatedIndex = this.comments.findIndex(comment => comment.id === commentId);
        if (updatedIndex !== -1) {
          this.comments[updatedIndex] = {...this.comments[updatedIndex], ...response.data};
        }
      } catch (error) {
        console.error('Error updating comment:', error);
      }
    },

    async commentList(articleId) {
      const response = await axios.get(`http://127.0.0.1:8000/articles/${articleId}/comments/`)
      this.comments = response.data
    },

    async commentCreate(articleId, commentData) {
      try {
        if (!articleId || !commentData) {
          throw new Error("Invalid input: Article ID and comment data are required.")
        }

        const token = localStorage.getItem('token')
        const response = await axios.post(`http://127.0.0.1:8000/articles/${articleId}/comment/create/`, commentData, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        })
        return response.data

      } catch (error) {
        console.error('Error creating comment:', error)
        throw error
      }
    },

    async commentDelete(commentId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:8000/articles/${commentId}/comment/delete/`, {
          headers: {
            Authorization: token ? `Token ${token}` : ''
          }
        });
        this.comments = this.comments.filter(comment => comment.id !== commentId);
      } catch (error) {
        console.error('Error deleting comment:', error);
      }
    },
  }
})
