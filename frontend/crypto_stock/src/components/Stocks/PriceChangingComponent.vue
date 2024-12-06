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
    <div class="canvas-container">
      <canvas ref="priceCanvas"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';

export default defineComponent({
  name: 'PriceChangingComponent',
  setup() {
    const priceCanvas = ref<HTMLCanvasElement | null>(null);
    const stockData = ref<number[]>([]); // Random stock data array
    const timePeriod = ref('24h'); // Default time period

    // Generate random stock data
    const generateRandomStockData = () => {
      const data = Array.from({ length: 1440 }, () =>
        Math.random() * 100 // Random numbers between 0 and 100
      );
      stockData.value = data;
      drawPriceChanges();
    };

    // Draw the price changes on the canvas
    const drawPriceChanges = () => {
      if (priceCanvas.value && stockData.value.length > 0) {
        const canvas = priceCanvas.value;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          // Set canvas dimensions dynamically
          const canvasWidth = canvas.clientWidth;
          const canvasHeight = canvas.clientHeight;
          canvas.width = canvasWidth;
          canvas.height = canvasHeight;

          // Clear the canvas
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Set background
          ctx.fillStyle = '#000';
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          // Set line styles
          ctx.strokeStyle = '#00ff00'; // Green line
          ctx.lineWidth = 2;

          // Draw stock data line
          ctx.beginPath();
          stockData.value.forEach((price, index) => {
            // Calculate X and Y coordinates
            const x = (index / (stockData.value.length - 1)) * canvas.width;
            const y = canvas.height - (price / 100) * canvas.height; // Scale price to canvas height

            if (index === 0) {
              ctx.moveTo(x, y); // Start point
            } else {
              ctx.lineTo(x, y); // Line to next point
            }
          });
          ctx.stroke(); // Render the line
        }
      }
    };

    // Handle time period change (currently regenerates random data)
    const changeTimePeriod = (newTimePeriod: string) => {
      timePeriod.value = newTimePeriod;
      generateRandomStockData();
    };

    onMounted(() => {
      generateRandomStockData(); // Generate initial data on mount
    });

    return {
      priceCanvas,
      changeTimePeriod,
    };
  },
});
</script>

<style scoped>
.price-changing-component {
  position: relative;
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
  top: 25px;
  left: 3%;
  color: white;
  font-size: 18px;
  font-weight: bold;
}
.canvas-container {
  width: 100%;
  position: relative;
}
.buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

canvas {
  margin-top: 5px;
  display: block;
  width: 100%;
}
</style>
