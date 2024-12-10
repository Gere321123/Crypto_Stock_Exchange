<template>
  <div class="company-detail">
    <!-- Conditionally render child components when company is not empty -->
    <PriceChangingComponent v-if="company && Object.keys(company).length > 0" :company="company" />
    <TransactionSection v-if="company && Object.keys(company).length > 0" :company="company" />
    <!-- Show a loader or placeholder while data is being fetched -->
    <p v-else>Loading company details...</p>
  </div>
</template>

<script>
import PriceChangingComponent from './PriceChangingComponent.vue';
import TransactionSection from "./TransactionSection.vue";

export default {
  name: 'CompanyDetail',
  components: {
    PriceChangingComponent,
    TransactionSection,
  },
  data() {
    return {
      company: null, // Initialize as null to indicate no data loaded yet
      intervalId: null, // Holds the interval ID for clearing later
    };
  },
  created() {
    const companyId = this.$route.params.id;
    this.loadCompanyDetails(companyId);

    // Set interval to reload company details every minute (60000 ms)
    this.intervalId = setInterval(() => {
      this.loadCompanyDetails(companyId);
    }, 6000);
  },
  beforeDestroy() {
    // Clear the interval when the component is destroyed
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    async loadCompanyDetails(id) {
      try {
        const response = await fetch(`http://localhost:5000/stocks/${id}`);
        const data = await response.json();

        if (data.stock && Array.isArray(data.stock)) {
          this.company = data.stock;
        } else {
          console.error('Invalid stock data format:', data.stock);
          this.company = {}; // Set to an empty object for safety
        }
      } catch (error) {
        console.error('Error fetching company details:', error);
        this.company = {}; // Fallback to an empty object
      }
    },
  },
};
</script>



<style scoped>
.company-detail {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  color: #ffffff;
  flex-wrap: wrap; /* Allows wrapping when the screen is small */
}
</style>