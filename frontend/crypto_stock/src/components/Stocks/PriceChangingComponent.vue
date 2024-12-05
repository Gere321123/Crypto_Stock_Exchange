<template>
  <div class="price-changing-component">
    <!-- USD label in top-left -->
    <div class="usd-label">USD</div>

    <!-- Time period buttons -->
    <div class="buttons">
      <button @click="changeTimePeriod('24h')">24h</button>
      <button @click="changeTimePeriod('5d')">5d</button>
      <button @click="changeTimePeriod('1m')">1m</button>
      <button @click="changeTimePeriod('3m')">3m</button>
      <button @click="changeTimePeriod('1y')">1y</button>
      <button @click="changeTimePeriod('5y')">5y</button>
    </div>

    <!-- Canvas for displaying the stock price chart -->
    <canvas ref="priceCanvas" width="500" height="700"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue';

export default defineComponent({
  name: 'PriceChangingComponent',
  props: {
    company: {
      type: Object as () => Record<number, any>,
      default: () => ({})
    }
  },
  setup(props) {
    // Reactive refs for state
    const showBuy = ref(false);
    const showSell = ref(false);
    const ethAmount = ref(0);
    const tokensAmount = ref(0);
    const tokensToReceive = ref(0);
    const ethToReceive = ref(0);
    const priceCanvas = ref<HTMLCanvasElement | null>(null);
    const stockData = ref<any>(null); // Store fetched stock data
    const timePeriod = ref('24h'); // Time period for stock data

    const fetchCompanyDetails = async (timeframe: string) => {
      try {
        const response = await fetch(`http://localhost:5000/stocks/${props.company[0]}?timeframe=${timeframe}`);
        const data = await response.json();
        stockData.value = data.stock; // Store the fetched stock data
        drawPriceChanges();
      } catch (error) {
        console.error('Error fetching company details:', error);
      }
    };

    const drawPriceChanges = () => {
      if (priceCanvas.value && stockData.value) {
        const ctx = priceCanvas.value.getContext('2d');
        if (ctx) {
          ctx.clearRect(0, 0, priceCanvas.value.width, priceCanvas.value.height);
          ctx.fillStyle = '#000';
          ctx.fillRect(0, 0, priceCanvas.value.width, priceCanvas.value.height);

          ctx.fillStyle = '#fff';
          ctx.font = '20px Arial';
          ctx.fillText(`Price changes for ${props.company[2]}`, 50, 100);

          // Draw stock data (for simplicity, let's assume stockData.value contains time and price data)
          if (stockData.value) {
            const data = stockData.value[timePeriod.value]; // Assume data is structured by time period
            data.forEach((point: any, index: number) => {
              const x = (index / data.length) * priceCanvas.value.width;
              const y = priceCanvas.value.height - (point.price / 100) * priceCanvas.value.height;
              ctx.fillRect(x, y, 2, 2); // Draw each point as a small square
            });
          }
        }
      }
    };

    // Handle time period change (button click)
    const changeTimePeriod = (newTimePeriod: string) => {
      timePeriod.value = newTimePeriod;
      fetchCompanyDetails(newTimePeriod); // Fetch data for the selected time period
    };

    onMounted(() => {
      fetchCompanyDetails('24h'); // Default fetch for 24 hours
    });

    watch(() => props.company, () => {
      fetchCompanyDetails(timePeriod.value); // Re-fetch data if company changes
    });

    return {
      showBuy,
      showSell,
      ethAmount,
      tokensAmount,
      tokensToReceive,
      ethToReceive,
      priceCanvas,
      changeTimePeriod,
    };
  }
});
</script>

<style scoped>
.price-changing-component {
  flex: 1 1 70%; /* Flex-grow, flex-shrink, and base width */
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #1f1f1f;
  padding: 20px;
  color: rgb(124, 124, 124);
  margin: 20px;
  box-sizing: border-box;
}

button {
  margin: 5px;
  padding: 10px 15px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #45a049;
}

.usd-label {
  position: absolute;
  top: 20px;
  left: 20px;
  color: white;
  font-size: 18px;
  font-weight: bold;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

canvas {
  margin-top: 20px;
}
</style>
