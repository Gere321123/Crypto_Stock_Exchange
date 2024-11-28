<template>
  <div>
    <h2>Edit Stock</h2>
    <form @submit.prevent="saveChanges">
        <div>
          <label for="url">URL:</label>
          <input type="text" v-model="stock[1]" required />
        </div>
        <div>
          <label for="url">Network:</label>
          <input type="text" v-model="network" required />
        </div>
        <div>
          <label for="companyname">Company Name:</label>
          <input type="text" v-model="stock[2]" required />
        </div>
        <div>
          <label for="description">Description:</label>
          <input type="text" v-model="stock[3]" />
        </div>
        <div>
          <label for="long_description">Long Description:</label>
          <input type="text" v-model="stock[4]" />
        </div>
        <div>
          <label for="picture_url">Picture URL:</label>
          <input type="text" v-model="stock[5]" />
        </div>
        <div>
          <label for="wallpaper_url">Wallpaper URL:</label>
          <input type="text" v-model="stock[6]" />
        </div>

        <!-- Array for other_pictures -->
        <div>
          <label for="other_pictures">Other Pictures:</label>
          <div v-for="(index) in stock[7]" :key="index">
            <input type="text" v-model="stock[7][index]" placeholder="Enter picture URL" />
            <button type="button" @click="removeOtherPicture(index)">Remove</button>
          </div>
          <button type="button" @click="addOtherPicture">Add Picture URL</button>
        </div>

        <!-- Array for annual_demand -->
        <div>
          <label for="annual_demand">Annual Demand:</label>
          <div v-for="(demand, index) in annual_demand" :key="index">
            <input type="number" v-model="annual_demand[index]" placeholder="Enter demand value" />
            <button type="button" @click="removeAnnualDemand(index)">Remove</button>
          </div>
          <button type="button" @click="addAnnualDemand">Add Demand Value</button>
        </div>

        <div>
          <label for="website">Website:</label>
          <input type="text" v-model="stock[9]" />
        </div>
        <div>
          <label for="number_of_stock">Number of Stock:</label>
          <input type="number" v-model="stock[10]" required />
        </div>
        <div>
          <label for="virtual_Bit">Virtual-Bit:</label>
          <input type="number" v-model="stock[11]" required />
        </div>
        <button type="submit">Save Stock</button>
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
      console.log("call this");
      const stockId = this.$route.params.stockId; // Get the stock ID from the route parameter
      console.log("id: ", stockId);
      try {
        const response = await axios.get(`http://127.0.0.1:5000/stocks/${stockId}`);
        console.log("response: ", response);
        this.stock = response.data.stock; // Populate the stock object with data from the server
        console.log("this.stock: ", this.stock);
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
