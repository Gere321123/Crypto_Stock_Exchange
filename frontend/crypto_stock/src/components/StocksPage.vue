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
    <div >
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
          <label for="companyname">Country:</label>
          <input type="text" v-model="country" required />
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
        <div>
          <label for="virtual_Bit">Username:</label>
          <input type="text" v-model="stockUsername" required />
        </div>
        <button type="submit">Create Stock</button>
      </form>
    </div>

    <div>
    <h3>Existing Users</h3>
    <ul>
      <li v-for="user in users" :key="user[0]">
        {{ user[0] }} - {{ user[1] }}
        <button @click="deleteUser(user[0])">Delete</button>
      </li>
    </ul>
  </div>

  <div>
    <h3>Existing Stocks</h3>
    <ul>
      <li v-for="stock in stocks" :key="stock[0]">
        {{ stock[2] }} - {{ stock[3] }} - ${{ stock[16] }}
        <button @click="editStock(stock[0])">Edit</button>
        <button @click="deleteStock(stock[0])">Delete</button>
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
      country :'',
      website: '',
      number_of_stock: null,
      virtual_Bit: 0,
      username: '',
      stockUsername: '',
      password: '',   // Added to capture password
      other_pictures: [],  // Array for other pictures URLs
      annual_demand: [],   // Array for annual demand values
      stocks: [],
      users:[],
      message: '',         // Message for registration status
    };
  },
 mounted() {
  this.fetchStocks();
  this.fetchUsers();
  },
  methods: {
    async fetchStocks() {
      try {
        const response = await fetch('http://localhost:5000/stocks');
        const data = await response.json();
        this.stocks = data.stocks; 
      } catch (error) {
        console.error('Error fetching stocks:', error);
      }
    },
    async deleteUser(username) {
      if (confirm(`Are you sure you want to delete user "${username}"?`)) {
        try {
          const response = await fetch(`http://localhost:5000/users/${username}`, {
            method: 'DELETE'
          });
          if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to delete user.');
          }
          // Remove the user from the local array if deletion succeeds
          this.users = this.users.filter((user) => user[0] !== username);
          alert(`User "${username}" deleted successfully.`);
        } catch (error) {
          console.error("Error deleting user:", error);
          alert(`An error occurred: ${error.message}`);
        }
      }
    },
    async fetchUsers() {
      try {
        const response = await fetch('http://localhost:5000/users');
        const data = await response.json();
        this.users = data.users; 
      } catch (error) {
        console.error('Error fetching stocks:', error);
      }
    },editStock(stockId) {
      this.$router.push({ name: "EditStock", params: { stockId } });
    },
    deleteStock(stockId) {
      if (confirm("Are you sure you want to delete this stock?")) {
        // Send a DELETE request to the server to remove the stock
        fetch(`http://localhost:5000/stocks/${stockId}`, {
          method: "DELETE",
        })
          .then((response) => {
            if (response.ok) {
              // Remove the stock from the local list
              this.stocks = this.stocks.filter((stock) => stock.id !== stockId);
              alert("Stock deleted successfully.");
            } else {
              alert("Failed to delete stock.");
            }
          })
          .catch((error) => {
            console.error("Error deleting stock:", error);
            alert("An error occurred while deleting the stock.");
          });
      }
    },
      async registerUser() {
  try {
      const response = await axios.post('http://127.0.0.1:5000/register', {
          username: this.username,
          password: this.password,
          is_admin: false,  // Regular user, not an admin
      });
      this.message = response.data.message || "Registration successful! You can now create a stock.";
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
        username: this.stockUsername,
        country: this.country,
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
      this.stockUsername = '';
      this.username = '';
      this.password = '';
      this.country = '';
    }
  },
};
</script>


<style scoped>
button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>