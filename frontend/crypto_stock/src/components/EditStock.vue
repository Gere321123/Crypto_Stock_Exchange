<template>
  <div>
    <h2>Tranzakcions</h2>
    <input v-model.number="tokensAmount" type="number" placeholder="Enter tokens amount" /> WBit
    <button v-if="loginasCompany" @click="uplodemoneyfunction">Uplode Money</button>
    <button @click="widrowMoney">Widrow Money</button>
    <WithdrawUplode 
      ref="connectComponent"
      :uplodemoney="uplodemoney"
      :loginasCompany = "loginasCompany"
      :sendValue="tokensAmount"
      :address="stock[1]"
      :network="stock[34]"
    />
    <h2>Edit Stock</h2>
    <form @submit.prevent="saveChanges">
      <div v-if="!loginasCompany">      
        <div>
          <label for="url">URL:</label>
          <input type="text" v-model="stock[1]" required />
        </div>
        <div>
          <label for="url">Network:</label>
          <input type="text" v-model="stock[34]" required />
        </div>
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
          <div v-for="(picture ,index) in otherPictures" :key="index">
            <input type="text" v-model="otherPictures[index]" placeholder="Enter picture URL" />
            <button type="button" @click="removeOtherPicture(index)">Remove</button>
          </div>
          <button type="button" @click="addOtherPicture">Add Picture URL</button>
        </div>

        <!-- Array for annual_demand -->
        <div>
          <label for="annual_demand">Annual Demand:</label>
          <div v-for="(demand, index) in annualdemand" :key="index">
            <input type="number" v-model="annualdemand[index]" placeholder="Enter demand value" />
            <button type="button" @click="removeAnnualDemand(index)">Remove</button>
          </div>
          <button type="button" @click="addAnnualDemand">Add Demand Value</button>
        </div>

        <div>
          <label for="website">Website:</label>
          <input type="text" v-model="stock[9]" />
        </div>
        <div v-if="!loginasCompany">
          <div>
            <label for="number_of_stock">Number of Stock:</label>
            <input type="number" v-model="stock[10]" required />
          </div>
          <div>
            <label for="virtual_Bit">Virtual-Bit:</label>
            <input type="number" v-model="stock[11]" required />
          </div>
          <div>
            <label for="virtual_Bit">User name:</label>
            <input type="text" v-model="stock[12]" required />
          </div>
        </div>
        <button type="submit">Save Stock</button>
      </form>
  </div>
</template>

<script>
import axios from "axios";
import WithdrawUplode from "./Stocks/WithdrawUplode.vue";
export default {
  data() {
    return {
      stock: {},
      otherPictures: [],
      annualdemand: [],
      id: '',
      loginasCompany: true,
      tokensAmount: 0,
      uplodemoney: true,
    };
  },
  components: { WithdrawUplode },
  props: {
    stockId: {
        type: String,
        required: false, // Optional, as it might come from the route
    },
},
  mounted() {
    this.loadStock();
  },
  methods: {
    async loadStock() {
      if (!this.stockId){
        this.loginasCompany = false; 
      }
    this.id = this.stockId || this.$route.params.stockId; // Use prop first, then fallback to route params
    if (!this.id) {
        console.error("No stockId provided");
        alert("Stock ID is missing!");
        return;
    }
    try {
        const response = await axios.get(`http://127.0.0.1:5000/stocks/${this.id}`);
        this.stock = response.data.stock;
        // Parse fields after loading
        this.otherPictures = this.stringToArray(this.stock[7]);
        this.annualdemand = this.stringToArray(this.stock[8]);
    } catch (error) {
        console.error("Error loading stock:", error);
        alert("Failed to load stock data.");
    }
},
uplodemoneyfunction() {
      if (this.tokensAmount > 0) {
        this.uplodemoney = true; // Indicate an "upload" operation
        this.$refs.connectComponent?.openModal(); // Open the modal
      } else {
        console.error("Please enter a valid tokens amount!");
      }
    },
    widrowMoney() {
      if (this.tokensAmount > 0) {
        this.uplodemoney = false; // Indicate a "withdraw" operation
        this.$refs.connectComponent?.openModal(); // Open the modal
      } else {
        console.error("Please enter a valid tokens amount!");
      }
    },

    async saveChanges() {
      this.stock[7] = "["+this.otherPictures.toString()+"]";
      this.stock[8] = "["+this.annualdemand.toString()+"]";

      console.log(this.stock);
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/stocks/${this.id}`,
          this.stock
        );
        alert(response.data.message || "Stock updated successfully!");
      } catch (error) {
        console.error("Error saving stock:", error);
        alert("Failed to save changes.");
      }
    },
    cancelEdit() {
      this.$router.push("/"); // Redirect to the main page or stock list
    },
    addAnnualDemand() {
      this.annualdemand.push('');  // Add an empty string for a new picture URL
    },
    addOtherPicture() {
      this.otherPictures.push('');  // Add an empty string for a new picture URL
    },
    removeAnnualDemand(index) {
      this.annualdemand.splice(index, 1);  // Remove picture URL at the specified index
    },
    removeOtherPicture(index) {
      this.otherPictures.splice(index, 1);  // Remove picture URL at the specified index
    },
    stringToArray(input) {
    // Check if the input is a valid array string
    if (input === "[]") {
      return [];
    }

    try {
      // Remove the square brackets and split the content
      const content = input.slice(1, -1); // Remove "[" and "]"
      if (!content.trim()) {
        return []; // If the content is empty, return an empty array
      }

      // Split by comma and trim each element
      return content.split(',').map(item => item.trim());
    } catch (error) {
      console.error("Invalid array string:", input);
      return [];
    }
    },
  },
};
</script>
