<template>
  <section class="for-companies">
    <h1>For Companies</h1>
    <p>
      Crypto Stock empowers companies to raise capital through Ethereum-based tokens, specifically 
      using Wrapped Bitcoin (WBTC). This innovative process enables businesses to bypass traditional 
      financial systems, offering a decentralized way to secure investments from a global pool of crypto investors.
    </p>
    <p>
      Join the decentralized finance revolution by leveraging cryptocurrency to fuel your company's growth 
      and unlock new opportunities for expansion, without the limitations of conventional fundraising methods.
    </p>
    <button class="get-started-button" @click="handleGetStarted">Get WBTC</button>
  </section>
</template>

<script>
export default {
  name: 'ForCompaniesComponent',
  data() {
    return {
      showTestText: false,  // Controls the visibility of the test text
     
    };
  },
  methods: {
    handleGetStarted() {
     
    }
  }
}
</script>

<style scoped>
.for-companies {
  display: flex;                /* Enable flexbox */
  flex-direction: column;       /* Stack children vertically */
  align-items: center;          /* Center children horizontally */
  min-height: 100vh;           /* Full viewport height */
  color: #ffffff;              /* Text color */
  padding: 20px;               /* Padding */
  text-align: center;          /* Center text */
  margin-top: 5%;          /* Margin at the top */
  max-width: 700px;            /* Max width for the content */
  margin-left: auto;           /* Center horizontally */
  margin-right: auto;          /* Center horizontally */
}

h1 {
   font-size: 2.5em;
   margin-bottom: 20px;
 }

p {
  font-size: 1.2em;
  color: #b0b0b0;
  margin: 15px 0;
}

.get-started-button {
  margin-top: 30px;
  padding: 12px 24px;
  font-size: 1em;
  color: #ffffff;
  background-color: #3a3b3e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.get-started-button:hover {
  background-color: #4a4b4e;
}
</style>