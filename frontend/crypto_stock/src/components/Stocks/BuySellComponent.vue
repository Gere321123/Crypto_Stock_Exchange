<template>
  <section class="buy-sell">
    <h1>Buy/Sell Tokens</h1>
    <div>
      <!-- Filter and Search Controls -->
      <div class="filter-container">
        <input 
          v-model="searchQuery" 
          @input="filterStocks" 
          placeholder="Search company name..." 
          class="search-input"
        />
        <select v-model="sortOption" @change="sortStocks" class="sort-select">
          <option value="abc">Sort A-Z</option>
          <option value="zyx">Sort Z-A</option>
          <option value="newest">Newest to Oldest</option>
          <option value="oldest">Oldest to Newest</option>
          <option value="country">Sort by Country</option>
        </select>
      </div>

      <!-- Stock List -->
      <h3>Existing Stocks</h3>
      <ul class="company-list">
  <li 
    v-for="stock in filteredStocks" 
    :key="stock[0]" 
    @click.stop="goToCompanyDetail(stock[0])" 
    class="company-item"
  >
  <span>{{ stock[2] }}</span>
  <span>{{ stock[17] }} $</span>
    <button @click.stop="goToCompanyDetail(stock[0])" class="learn-more-button">
      Learn More
    </button>
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
      stocks: [],           // All stock data
      filteredStocks: [],   // Filtered and sorted data to display
      searchQuery: '',      // User input for search
      sortOption: 'abc',    // Default sort option
    };
  },
  mounted() {
    // Fetch stocks on mount
    this.fetchStocks();
  },
  methods: {
    // Fetch data from backend
    async fetchStocks() {
      try {
        const response = await fetch('http://localhost:5000/stocks');
        const data = await response.json();
        this.stocks = data.stocks;
        this.filteredStocks = [...this.stocks]; // Default view
      } catch (error) {
        console.error('Error fetching stocks:', error);
      }
    },

    // Filter stocks based on the search query
    filterStocks() {
      this.filteredStocks = this.stocks.filter(stock =>
        stock[2].toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      this.sortStocks(); // Re-apply sorting after filtering
    },

    // Sort stocks based on the selected option
    sortStocks() {
      const sortOption = this.sortOption;

      if (sortOption === 'abc') {
        this.filteredStocks.sort((a, b) => a[2].localeCompare(b[2])); // A-Z
      } else if (sortOption === 'zyx') {
        this.filteredStocks.sort((a, b) => b[2].localeCompare(a[2])); // Z-A
      } else if (sortOption === 'newest') {
        this.filteredStocks.sort((a, b) => new Date(b[18]) - new Date(a[18])); // Newest
      } else if (sortOption === 'oldest') {
        this.filteredStocks.sort((a, b) => new Date(a[18]) - new Date(b[18])); // Oldest
      } else if (sortOption === 'country') {
        this.filteredStocks.sort((a, b) => a[35].localeCompare(b[35])); // Sort by Country
      }
    },

    // Navigate to the company detail page
    goToCompanyDetail(companyId) {
      this.$router.push({ name: 'companyDetail', params: { id: companyId } });
    },
  }
}
</script>


<style scoped>
/* General Styling */
.buy-sell {
  text-align: center;
  color: #ffffff;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
}

/* Filter Controls */
.filter-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input,
.sort-select {
  padding: 10px;
  border: 2px solid #7e0dd5;
  border-radius: 8px;
  font-size: 16px;
  background-color: #29293d;
  color: #fff;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-input:focus,
.sort-select:focus {
  border-color: #9b43e6;
  outline: none;
  box-shadow: 0 0 8px rgba(126, 13, 213, 0.7);
}

.search-input {
  flex: 2;
}

.sort-select {
  flex: 1;
}

/* Stock List */
.company-list {
  list-style: none;
  padding: 0;
  margin: 0 auto;
  max-width: 800px;
}

.company-list li {
  background-color: #29293d;
  margin: 20px 0;
  padding: 20px 25px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.company-list li:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(126, 13, 213, 0.4);
}

/* Company Info Text */
.company-info {
  font-size: 18px;
  font-weight: bold;
  color: #e5e5e5;
  text-align: left;
}

/* Learn More Button */
.learn-more-button {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  background-color: #7e0dd5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.learn-more-button:hover {
  background-color: #9b43e6;
  box-shadow: 0 4px 10px rgba(126, 13, 213, 0.6);
}

/* Responsive Design */
@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    gap: 10px;
  }
  .search-input,
  .sort-select {
    width: 100%; /* Make both inputs take up full width */
    box-sizing: border-box;
  }
  .company-list li {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
}
</style>
