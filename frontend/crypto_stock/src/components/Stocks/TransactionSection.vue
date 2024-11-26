<template>
  <div class="transaction-section">
    <button @click="toggleBuy">Buy Tokens</button>
    <button @click="toggleSell">Sell Tokens</button>
    <button @click="getvalue">Value</button>
    <!-- Buy Input -->
    <div v-if="showBuy">
      <label>ETH to spend:</label>
      <input v-model="ethAmount" type="number" @input="calculateTokens" placeholder="Enter ETH amount" />
      <p>You will receive: {{ tokensToReceive }} tokens</p>
    </div>

    <!-- Sell Input -->
    <div v-if="showSell">
      <label>Tokens to sell:</label>
      <input v-model="tokensAmount" type="number" @input="calculateEth" placeholder="Enter tokens amount" />
      <p>You will receive: {{ ethToReceive }} ETH</p>
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
  position: fixed;
  top: 75%;
  right: 0;
  width: 30%;
  background-color: #000000;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 10px 20px;
  box-sizing: border-box;
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
</style>
