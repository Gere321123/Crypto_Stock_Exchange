<template>
  <div class="company-detail">
    <PriceChangingComponent :company="company" />
    <TransactionSection :company="company" />
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
      company: {}, // Holds the details of the selected company
      intervalId: null, // Holds the interval ID for clearing later
    };
  },
  created() {
    const companyId = this.$route.params.id;
    this.loadCompanyDetails(companyId);
    // Set interval to reload company details every minute (60000 ms)
    this.intervalId = setInterval(() => {
      this.loadCompanyDetails(companyId);
    }, 60000);
  },
  beforeDestroy() {
    // Clear the interval when the component is destroyed
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    // Method to fetch company details from the backend
    async loadCompanyDetails(id) {
      try {
        const response = await fetch(`http://localhost:5000/stocks/${id}`); // Use the desired ID directly
        const data = await response.json();
        this.company = data.stock; // Set the selected company details
      } catch (error) {
        console.error('Error fetching company details:', error);
      }
    }
  }
}
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