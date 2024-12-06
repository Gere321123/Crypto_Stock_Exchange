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

    // Draw the price changes on the canvas with axes
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

      // Margins for all edges (left, right, top, bottom)
      const leftMargin = 30;
      const rightMargin = 30;
      const topMargin = 30;
      const bottomMargin = 30;

      // Clear the canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Set background
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw vertical lines for the left axis
      const maxPrice = 100; // Maximum price for scaling
      const minPrice = 0; // Minimum price
      const numVerticalLines = 5; // Number of value markers
      const verticalGap = (canvasHeight - topMargin - bottomMargin) / numVerticalLines;

      ctx.strokeStyle = '#555';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#fff';
      ctx.font = '12px Arial';

      for (let i = 0; i <= numVerticalLines; i++) {
        const y = canvasHeight - bottomMargin - i * verticalGap;
        const priceValue = ((i / numVerticalLines) * (maxPrice - minPrice)) + minPrice;

        // Draw grid line
        ctx.beginPath();
        ctx.moveTo(leftMargin, y);
        ctx.lineTo(canvasWidth - rightMargin, y);
        ctx.stroke();

        // Draw price label on the left side of the vertical line
        ctx.fillText(priceValue.toFixed(0), leftMargin - 25, y + 5); // Position label to the left
      }

      // Draw horizontal lines for the bottom axis (time markers)
      const numTimeMarkers = 6; // Number of time markers
      const timeGap = (canvasWidth - leftMargin - rightMargin) / (numTimeMarkers - 1);
      const timeLabels = ['0h', '4h', '8h', '12h', '16h', '24h']; // Example time labels

      for (let i = 0; i < numTimeMarkers; i++) {
        const x = leftMargin + i * timeGap;

        // Draw grid line
        ctx.beginPath();
        ctx.moveTo(x, topMargin);
        ctx.lineTo(x, canvasHeight - bottomMargin);
        ctx.stroke();

        // Draw time label with padding
        ctx.fillText(timeLabels[i], x - 10, canvasHeight - bottomMargin + 15); // Position with padding
      }

      // Draw stock data line
      ctx.strokeStyle = '#00ff00'; // Green line
      ctx.lineWidth = 2;

      ctx.beginPath();
      stockData.value.forEach((price, index) => {
        const x = leftMargin + (index / (stockData.value.length - 1)) * (canvas.width - leftMargin - rightMargin);
        const y = canvas.height - bottomMargin - (price / maxPrice) * (canvas.height - topMargin - bottomMargin);

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();
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
  padding: 10px;
}
</style>
