<template>
  <div class="transaction-section">
    <a v-if="company[6]" :href="company[9]" target="_blank" rel="noopener noreferrer">
      <img :src="company[6]" alt="Company Wallpaper" />
    </a>
    <br>
    <a v-if="company[2]" :href="company[9]" target="_blank" rel="noopener noreferrer" class="company-link">
      <h2>{{ company[2] }}</h2>
    </a>
    <div class="price-container">
      <div class="price-box">
        <p>In wBTC:   <span class="token-amount">{{ company[16].toFixed(8) }} wBTC</span></p>
      </div>
      <div class="price-box">
        <p>In USD: {{ parseFloat(company[17]).toFixed(5) }} $</p>
      </div>
    </div>
    <div class="price-container">
      <div class="price-box">
   <p>Market Cap: <span class="token-amount">{{ formatTokens(company[13]) }} $</span></p>
</div>
      <div class="price-box">
        <p>Available Tokens: <span class="token-amount">{{ formatTokens(company[14]) }}</span></p>
</div>

</div>
    <button @click="toggleBuy">Buy Tokens</button>
    <button @click="toggleSell">Sell Tokens</button>
    
    <!-- Buy Input -->
    <div v-if="showBuy">
      <label>BIT to spend:</label>
      <input v-model="ethAmount" type="number" @input="calculateTokens" placeholder="Enter BIT amount" />
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

    <Connect 
  ref="connectComponent"
  :showBuy="showBuy"
  :sendValue="showBuy ? ethAmount : tokensAmount"
  :address="company[1]"
  :network="company[34]"
/>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Connect from './Connect.vue';

export default defineComponent({
  name: 'TransactionSection',
  components: { Connect },
  props: {
    company: {
      type: Array as () => Array<any>, // Specify that `company` is an array
      required: true,
    },
  },
  setup(props) {
    const connectComponent = ref();

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
      toggleSell,
      calculateTokens,
      calculateEth,
      openWalletPopup,
      connectComponent,
    };
  },
  methods: {
    // Format the number with thousand separators and two decimal places
    formatTokens(value: number): string {
      const formattedValue = value.toFixed(2);

      const [integerPart, decimalPart] = formattedValue.split('.');

      const integerWithCommas = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

      return `${integerWithCommas}.${decimalPart}`;
    }
  }
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
  margin: 10px; /* Add some spacing from other elements */
  justify-content: center; /* Center the boxes horizontally */
  align-items: center; /* Align boxes vertically */
}
.price-box p {
  line-height: 1.5; /* Adjust line spacing for better readability */
}

.token-amount {
  margin: 10px; /* Add space between the text and the number */
  display: inline-block; /* Ensures spacing applies properly */
}
.price-box {
  background-color: #111111; /* Light gray background for contrast */
  border: 1px solid #313131; /* Light border for a subtle effect */
  border-radius: 5px; /* Rounded corners for a modern look */
  text-align: center; /* Center text inside the box */
  flex: 1; /* Ensure boxes have equal width */
  margin: 5px;
  padding: 3px;
  display: flex; /* Enables Flexbox */
  align-items: center; /* Vertically centers content */
  justify-content: center; /* Optionally, horizontally centers content */
  height: 100%; /* Ensure the box has a defined height for centering */
  position: relative; /* Allows fine-tuning if needed */
}
.company-link {
  text-decoration: none; /* Remove the underline and typical link styling */
  color: inherit;
}

.company-link h2 {
  margin: 0; /* Remove default margin */
  padding: 0; /* Optional: Remove padding if needed */
}

</style>
