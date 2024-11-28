<template>
  <div>
    <h2>Edit Stock</h2>
    <form @submit.prevent="saveChanges">
      <div>
        <label for="url">URL:</label>
        <input type="text" v-model="stock.url" required />
      </div>
      <div>
        <label for="network">Network:</label>
        <input type="text" v-model="stock.network" required />
      </div>
      <div>
        <label for="companyname">Company Name:</label>
        <input type="text" v-model="stock.companyname" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <input type="text" v-model="stock.description" />
      </div>
      <div>
        <label for="long_description">Long Description:</label>
        <input type="text" v-model="stock.long_description" />
      </div>
      <div>
        <label for="picture_url">Picture URL:</label>
        <input type="text" v-model="stock.picture_url" />
      </div>
      <div>
        <label for="wallpaper_url">Wallpaper URL:</label>
        <input type="text" v-model="stock.wallpaper_url" />
      </div>
      <div>
        <label for="website">Website:</label>
        <input type="text" v-model="stock.website" />
      </div>
      <div>
        <label for="number_of_stock">Number of Stock:</label>
        <input type="number" v-model="stock.number_of_stock" required />
      </div>
      <div>
        <label for="virtual_Bit">Virtual-Bit:</label>
        <input type="number" v-model="stock.virtual_Bit" required />
      </div>
      <button type="submit">Save Changes</button>
      <button type="button" @click="cancelEdit">Cancel</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      stock: {
        id: null,
        url: "",
        network: "",
        companyname: "",
        description: "",
        long_description: "",
        picture_url: "",
        wallpaper_url: "",
        website: "",
        number_of_stock: null,
        virtual_Bit: 0,
      },
    };
  },
  mounted() {
    this.loadStock();
  },
  methods: {
    async loadStock() {
      const stockId = this.$route.params.stockId; // Get the stock ID from the route parameter
      try {
        const response = await axios.get(`http://127.0.0.1:5000/stocks/${stockId}`);
        this.stock = response.data.stock; // Populate the stock object with data from the server
      } catch (error) {
        console.error("Error loading stock:", error);
        alert("Failed to load stock data.");
      }
    },
    async saveChanges() {
      try {
        const response = await axios.put(`http://127.0.0.1:5000/stocks/${this.stock.id}`, this.stock);
        alert(response.data.message || "Stock updated successfully!");
        this.$router.push("/"); // Redirect to the main page or stock list
      } catch (error) {
        console.error("Error saving stock changes:", error);
        alert("Failed to save changes.");
      }
    },
    cancelEdit() {
      this.$router.push("/"); // Redirect to the main page or stock list
    },
  },
};
</script>
