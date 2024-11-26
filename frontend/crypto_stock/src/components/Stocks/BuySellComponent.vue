<template>
  <section class="buy-sell">
    <h1>Buy/Sell Tokens</h1>
    <div>
      <h3>Existing Stocks</h3>
      <ul class="company-list">
        <li v-for="stock in stocks" :key="stock[0]">
          {{ stock[2] }} - {{ stock[3] }} - ${{ stock[16] }}
          <button @click="goToCompanyDetail(stock[0])" class="learn-more-button">Learn More</button>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
export default {
  name: 'BuySellComponent',
  data() {
    return {
      stocks: []  // This will hold the stock data fetched from the backend
    };
  },
  mounted() {
    // Fetch the stock data when the component is mounted
    this.fetchStocks();
  },
  methods: {
    // Method to fetch stock data from the backend
    async fetchStocks() {
      try {
        const response = await fetch('http://localhost:5000/stocks');
        const data = await response.json();
        this.stocks = data.stocks; 
      } catch (error) {
        console.error('Error fetching stocks:', error);
      }
    },
    // Method to navigate to the company details page
    goToCompanyDetail(companyId) {
      this.$router.push({ name: 'companyDetail', params: { id: companyId } });
    }
  }
}
</script>

<style scoped>
.buy-sell {
  text-align: center;
  color: #ffffff;
}

.company-list {
  list-style: none;
  padding: 0;
}

.company-list li {
  background-color: #333;
  margin: 20px 0;
  padding: 20px;
  border-radius: 5px;
}

.learn-more-button {
  margin: 10px;
  padding: 10px 20px;
  color: #fff;
  background-color: #3a3b3e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.learn-more-button:hover {
  background-color: #7e0dd5;
}
</style>