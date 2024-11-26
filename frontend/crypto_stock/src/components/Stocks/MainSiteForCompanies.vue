<template>
  <div class="main-site-for-companies">
    <ul>
      <!-- Display the passed company data -->
      <li>
        <img v-if="company[6]" :src="company[6]" alt="Company Wallpaper" />
        <img v-if="company[5]" :src="company[5]" alt="Company Picture" />
        <h2>{{ company[2] }}</h2>
        <p>{{ company[3] }}</p>
        <p>{{ company[4] }}</p>

        <!-- Display main image -->

        <!-- Display wallpaper image -->

        <!-- Display other pictures as a gallery -->
        <div v-if="company[7]">
          <h3>Other Pictures</h3>
          <div class="other-pictures">
            <img v-for="(url, index) in JSON.parse(company[7])" :key="index" :src="url" alt="Other Picture" />
          </div>
        </div>

        <!-- Display annual demand
        <div v-if="company.annual_demand">
          <h3>Annual Demand</h3>
          <ul>
            <li v-for="(demand, index) in JSON.parse(company.annual_demand)" :key="index">{{ demand }}</li>
          </ul>
        </div> -->

        <!-- Display additional fields -->
        <p>Website: <a :href="company[9]" target="_blank">{{ company[9] }}</a></p>
        <p>Number of Stock: {{ company[10] }}</p>
        <!-- <p>Virtual ETH: {{ company.virtualeth }}</p> -->
        <!-- <p>Username: {{ company.username }}</p> -->
        <p>Market Cap: {{ company[13] }}</p>
        <p>Available Coins: {{ company[14] }}</p>
        <!-- <p>Total Supply: {{ company.total_supply }}</p> -->
        <p>Price: {{ company[16] }}</p>
        <p>Start Date: {{ company[17] }}</p>
        <!-- <p>ETH Balance: {{ company.eth_balance }}</p> -->
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'MainSiteForCompanies',
  props: {
    company: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.main-site-for-companies {
  width: 50%;
  max-height: 900px;
  overflow-y: auto;
  background-color: #222;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #444;
}

img {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}

.other-pictures img {
  max-width: 100px;
  margin-right: 5px;
}
</style>

<style>
/* Ensure the main page itself is scrollable */
html, body {
  height: 100%;
  overflow: auto;
}
</style>