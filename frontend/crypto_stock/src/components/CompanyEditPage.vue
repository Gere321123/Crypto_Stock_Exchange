<template>
  <div>
    <h1>Company Edit Page</h1>
    <EditStock v-if="stockId" :stockId="stockId" />
  </div>
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
        console.log( this.stockId);
      } catch (error) {
        console.error("Error fetching stock ID:", error);
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
