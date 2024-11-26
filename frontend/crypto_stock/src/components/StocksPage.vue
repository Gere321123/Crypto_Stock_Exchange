<template>
  <div>
    <h2>Register User</h2>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Register</button>
    </form>

    <!-- Success message -->
    <p v-if="message">{{ message }}</p>

    <!-- Only show stock creation form if registration is successful -->
    <div v-if="isRegistered">
      <h2>Create a Stock Item</h2>
      <form @submit.prevent="createStock">
        <div>
          <label for="url">URL:</label>
          <input type="text" v-model="url" required />
        </div>
        <div>
          <label for="url">Network:</label>
          <input type="text" v-model="network" required />
        </div>
        <div>
          <label for="companyname">Company Name:</label>
          <input type="text" v-model="companyname" required />
        </div>
        <div>
          <label for="description">Description:</label>
          <input type="text" v-model="description" />
        </div>
        <div>
          <label for="long_description">Long Description:</label>
          <input type="text" v-model="long_description" />
        </div>
        <div>
          <label for="picture_url">Picture URL:</label>
          <input type="text" v-model="picture_url" />
        </div>
        <div>
          <label for="wallpaper_url">Wallpaper URL:</label>
          <input type="text" v-model="wallpaper_url" />
        </div>

        <!-- Array for other_pictures -->
        <div>
          <label for="other_pictures">Other Pictures:</label>
          <div v-for="(picture, index) in other_pictures" :key="index">
            <input type="text" v-model="other_pictures[index]" placeholder="Enter picture URL" />
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
          <input type="text" v-model="website" />
        </div>
        <div>
          <label for="number_of_stock">Number of Stock:</label>
          <input type="number" v-model="number_of_stock" required />
        </div>
        <div>
          <label for="virtual_Bit">Virtual-Bit:</label>
          <input type="number" v-model="virtual_Bit" required />
        </div>
        <button type="submit">Create Stock</button>
      </form>
    </div>

    <div>
      <h3>Existing Stocks</h3>
      <ul>
        <li v-for="stock in stocks" :key="stock.id">
          {{ stock.companyname }} - {{ stock.description }} - ${{ stock.price }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      url: '',
      network: '',
      companyname: '',
      description: '',
      long_description: '',
      picture_url: '',
      wallpaper_url: '',
      website: '',
      number_of_stock: null,
      virtual_Bit: 0,
      username: '',
      password: '',   // Added to capture password
      other_pictures: [],  // Array for other pictures URLs
      annual_demand: [],   // Array for annual demand values
      stocks: [],
      isRegistered: false, // Flag to check if registration is complete
      message: '',         // Message for registration status
    };
  },
  async created() {
    // Fetch all stocks on page load
    try {
      const response = await axios.get('http://127.0.0.1:5000/stocks');
      this.stocks = response.data.stocks;
    } catch (error) {
      console.error("Error fetching stocks:", error);
    }
  },
  methods: {
      async registerUser() {
  try {
      const response = await axios.post('http://127.0.0.1:5000/register', {
          username: this.username,
          password: this.password,
          is_admin: false,  // Regular user, not an admin
      });
      this.message = response.data.message || "Registration successful! You can now create a stock.";
      this.isRegistered = true; // Set flag to show stock creation form
  } catch (error) {
      this.message = error.response ? error.response.data.message : "An error occurred.";
  }
},

    async createStock() {
      const stockData = {
        url: this.url,
        network: this.network,
        companyname: this.companyname,
        description: this.description,
        long_description: this.long_description,
        picture_url: this.picture_url,
        wallpaper_url: this.wallpaper_url,
        other_pictures: this.other_pictures,  // Pass array as JSON
        annual_demand: this.annual_demand,    // Pass array as JSON
        website: this.website,
        number_of_stock: this.number_of_stock,
        virtual_Bit: this.virtual_Bit,
        username: this.username
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/stocks', stockData);
        alert(response.data.message);
        // Reload stocks after creating a new one
        this.stocks.push(stockData);
        // Clear input fields after creation
        this.resetForm();
      } catch (error) {
        console.error("Error creating stock:", error);
      }
    },
    addOtherPicture() {
      this.other_pictures.push('');  // Add an empty string for a new picture URL
    },
    removeOtherPicture(index) {
      this.other_pictures.splice(index, 1);  // Remove picture URL at the specified index
    },
    addAnnualDemand() {
      this.annual_demand.push(null);  // Add a new null entry for a demand value
    },
    removeAnnualDemand(index) {
      this.annual_demand.splice(index, 1);  // Remove demand value at the specified index
    },
    resetForm() {
      this.url = '';
      this.network = '';
      this.companyname = '';
      this.description = '';
      this.long_description = '';
      this.picture_url = '';
      this.wallpaper_url = '';
      this.other_pictures = [];
      this.annual_demand = [];
      this.website = '';
      this.number_of_stock = null;
      this.virtual_Bit = 0;
      this.username = '';
      this.password = '';
    }
  }
};
</script>
