<template>
  <div class="company-detail">
    <MainSiteForCompanies :company="company" />
    <PriceChangingComponent :company="company" />
  </div>
</template>

<script>
import MainSiteForCompanies from './MainSiteForCompanies.vue';
import PriceChangingComponent from './PriceChangingComponent.vue';
import { useReadContract } from '@wagmi/vue'
import { abi } from '../abi'

export default {
  name: 'CompanyDetail',
  setup() {
    const result = useReadContract({
      abi,
      address: '0x988E411D1eE2476847241c3983312356daf749f0',
      functionName: 'getValueOfOneTokenInWei',
    })
    console.log(result);
  }
    ,
  components: {
    MainSiteForCompanies,
    PriceChangingComponent
  },
  data() {
    return {
      company: {} // Holds the details of the selected company
    };
  },
  created() {
    const companyId = this.$route.params.id;
    this.loadCompanyDetails(companyId);
  },
  methods: {
    // Method to fetch company details from the backend
    async loadCompanyDetails(id) {
      try {
        const response = await fetch(`http://localhost:5000/stocks/${id}`); // Use the desired ID directly
        const data = await response.json();
        this.company = data.company; // Set the selected company details
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
  color: #ffffff;
}
</style>