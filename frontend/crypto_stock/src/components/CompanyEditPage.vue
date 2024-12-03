<template>
  <div>
    <h1>Company Edit Page</h1>
    <div>
      <h2>Change Password</h2>
      <form @submit.prevent="handleChangePassword">
        <div>
          <label for="new-password">New Password:</label>
          <input type="password" v-model="newPassword" required />
        </div>
        <div>
          <label for="confirm-password">Confirm Password:</label>
          <input type="password" v-model="confirmPassword" required />
        </div>
        <button type="submit">Change Password</button>
      </form>
      <p v-if="passwordMessage">{{ passwordMessage }}</p>
    </div>
  </div>

  <EditStock v-if="stockId" :stockId="stockId" />
  
</template>

<script>
import axios from "axios";
import EditStock from "./EditStock.vue";

export default {
  components: {
    EditStock,
  },
  data() {
    return {
      stockId: null, // Store the stock ID for the username
      newPassword: "", // New password input
      confirmPassword: "", // Confirm password input
      passwordMessage: "", // Feedback for the user
    };
  },
  methods: {
    async fetchStockId() {
      const username = this.$route.params.username; // Assuming username is passed as a route param
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/stock-by-username/${username}`
        );
        this.stockId = response.data.stockId; // Assign the stock ID
      } catch (error) {
        console.error("Error fetching stock ID:", error);
      }
    },
    async handleChangePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.passwordMessage = "Passwords do not match.";
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/change-password",
          {
            username: this.$route.params.username, // Pass username
            newPassword: this.newPassword,
          }
        );
        this.passwordMessage = response.data.message;
      } catch (error) {
        console.error("Error changing password:", error);
        this.passwordMessage = "Failed to change password.";
      }
    },
  },
  mounted() {
    this.fetchStockId(); // Fetch stock ID when the component is mounted
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
