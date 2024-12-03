<template>
  <div>
      <h2>Admin Login</h2>
      <form @submit.prevent="handleLogin">
          <div>
              <label for="username">Username:</label>
              <input type="text" v-model="username" required />
          </div>
          <div>
              <label for="password">Password:</label>
              <input type="password" v-model="password" required />
          </div>
          <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
      return {
          username: '',
          password: '',
          errorMessage: ''
      };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.username,
          password: this.password
        });

        alert(response.data.message);

        // Redirect based on user type
        if (response.data.role === 'admin') {
          this.$router.push({ name: 'StocksPage' });
        } else if (response.data.role === 'company') {
          this.$router.push({ name: 'CompanyEditPage' });
        }
      } catch (error) {
        this.errorMessage = "Invalid credentials. Please try again.";
      }
    }
}
};
</script>

<style scoped>
  /* Add your CSS styles here */
</style>