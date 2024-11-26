<template>
  <div class="transaction-section">
    <a v-if="company[6]" :href="company[9]" target="_blank" rel="noopener noreferrer">
     <img :src="company[6]" alt="Company Wallpaper" />
    </a>
  <br>
    <a v-if="company[2]" :href="company[9]" target="_blank" rel="noopener noreferrer">
      <h2>{{ company[2] }}</h2>
    </a>
    <div class="price-container">
    <div class="price-box">
      <p>Price in BIT: {{ company[16] }} BIT</p>
    </div>
    <div class="price-box">
      <p>Price in USD: {{ company[17] }} $</p>
    </div>
    </div>

    <button @click="toggleBuy">Buy Tokens</button>
    <button @click="toggleSell">Sell Tokens</button>
    <button @click="getvalue">Value</button>
    <!-- Buy Input -->
    <div v-if="showBuy">
      <label>BIT to spend:</label>
      <input v-model="ethAmount" type="number" @input="calculateTokens" placeholder="Enter ETH amount" />
      <p>You will receive: {{ tokensToReceive }} tokens</p>
    </div>

    <!-- Sell Input -->
    <div v-if="showSell">
      <label>Tokens to sell:</label>
      <input v-model="tokensAmount" type="number" @input="calculateEth" placeholder="Enter tokens amount" />
      <p>You will receive: {{ ethToReceive }} BIT</p>
    </div>

    <!-- Connect Wallet Button -->
    <button v-if="showBuy || showSell" @click="openWalletPopup">Connect Wallet</button>

    <Connect ref="connectComponent" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useReadContract } from '@wagmi/vue'
import { abi } from '../../abi'
import { config } from '../../../config'
import Connect from './Connect.vue';

export default defineComponent({
  name: 'TransactionSection',
  components: { Connect },
  props: {
    company: {
      type: Object as () => Record<number, any>,
      required: true,
    },
  },
  setup(props) {
    console.log(props.company);
    const connectComponent = ref();
    const { data, isError, isLoading, error } = useReadContract({
    abi,
    address: '0x988E411D1eE2476847241c3983312356daf749f0',
    functionName: 'getValueOfOneTokenInWei',
    config: config
  });
  // Method to log the contract value
  const getvalue = async () => {
    try {
      console.log('Loading data...');
      while (isLoading.value) {
        await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for 100ms
      }

      if (isError.value) {
        console.error('Error reading contract:', error.value);
      } else if (data.value) {
        console.log('Value of one token in Wei:', data.value.toString());
      } else {
        console.log('No data available');
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };
    // Reactive refs for state
    const showBuy = ref(false);
    const showSell = ref(false);
    const ethAmount = ref(0);
    const tokensAmount = ref(0);
    const tokensToReceive = ref(0);
    const ethToReceive = ref(0);

    const toggleBuy = () => {
      showBuy.value = true;
      showSell.value = false;
      ethAmount.value = 0;
      tokensToReceive.value = 0;
    };

    const toggleSell = () => {
      showSell.value = true;
      showBuy.value = false;
      tokensAmount.value = 0;
      ethToReceive.value = 0;
    };

    const calculateTokens = () => {
      if (props.company[16]) {
        tokensToReceive.value = ethAmount.value / props.company[16];
      }
    };

    const calculateEth = () => {
      if (props.company[16]) {
        ethToReceive.value = tokensAmount.value * props.company[16];
      }
    };

    const openWalletPopup = () => {
      connectComponent.value?.openModal();
    };

    return {
      showBuy,
      showSell,
      ethAmount,
      tokensAmount,
      tokensToReceive,
      ethToReceive,
      toggleBuy,
      getvalue,
      toggleSell,
      calculateTokens,
      calculateEth,
      openWalletPopup,
      connectComponent,
    };
  },
});
</script>

<style scoped>
.transaction-section {
  flex: 1 1 25%;
  position: static; /* Avoids fixed positioning for better responsiveness */
  background-color: #191919;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 20px;
  box-sizing: border-box;
}
.transaction-section img {
  max-width: 100%; /* Prevents the image from growing wider than the container */
  max-height: 100%; /* Prevents the image from growing taller than the container */
  object-fit: contain; /* Ensures the image scales proportionally */
  display: block; /* Removes inline element spacing issues */
  margin: 0 auto; /* Centers the image horizontally */
}
button {
  margin: 5px;
  padding: 10px 15px;
  cursor: pointer;
}

input {
  margin-top: 10px;
  padding: 5px;
  width: 80%;
}
.price-container {
  display: flex; /* Align items in a row */
  gap: 10px; /* Add spacing between the boxes */
  margin-top: 20px; /* Add some spacing from other elements */
}

.price-box {
  background-color: #111111; /* Light gray background for contrast */
  border: 1px solid #313131; /* Light border for a subtle effect */
  border-radius: 5px; /* Rounded corners for a modern look */
  text-align: center; /* Center text inside the box */
  flex: 1; /* Ensure boxes have equal width */
  margin: 5px
}

</style>
