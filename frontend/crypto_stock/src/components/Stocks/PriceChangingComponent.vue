<template>
  <div class="price-changing-component">
    <!-- USD label in top-left -->
    
    <!-- Time period buttons -->
    <div class="buttons">
      <div class="usd-label">USD</div>
      <button @click="changeTimePeriod(0)">24h</button>
      <button @click="changeTimePeriod(1)">5d</button>
      <button @click="changeTimePeriod(2)">1m</button>
      <button @click="changeTimePeriod(3)">3m</button>
      <button @click="changeTimePeriod(4)">1y</button>
      <button @click="changeTimePeriod(5)">5y</button>
    </div>

    <!-- Canvas for displaying the stock price chart -->
    <div class="canvas-container">
      <canvas ref="priceCanvas"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, onBeforeUnmount } from 'vue';

export default defineComponent({
  name: 'PriceChangingComponent',
  props: {
    company: {
      type: Array as () => Array<any>, // Specify that `company` is an array
      required: true,
    },
  },
  setup(props) {
    const priceCanvas = ref<HTMLCanvasElement | null>(null);
    const stockData = ref<number[]>([]); // Placeholder for the stock data
    let refreshInterval: number | null = null; // To store the interval ID
    let canvasWidth = 0;
    let canvasHeight = 0;
    let grafIndex = 0;

    // Fetch stock data from company[20] dynamically
    const fetchStockData = () => {
      if (Array.isArray(props.company) && typeof props.company[20 + grafIndex] === 'string') {
        try {
          const arrayData = JSON.parse(props.company[20 + grafIndex]);
          stockData.value = Array.isArray(arrayData) ? arrayData : [];
          drawPriceChanges();
        } catch (error) {
          console.error('Invalid JSON string:', error);
        }
      } else {
        console.error('props.company[20 + grafIndex] is not available or invalid');
        stockData.value = []; // Default to an empty array
      }
    };

    // Initialize canvas dimensions once
    const initializeCanvas = () => {
      if (priceCanvas.value) {
        const canvas = priceCanvas.value;
        const parent = canvas.parentElement;
        if (parent) {
          canvasWidth = parent.clientWidth;
          canvasHeight = parent.clientHeight;
          canvas.width = canvasWidth;
          canvas.height = canvasHeight;
        }
      }
    };

    // Draw the price changes on the canvas with axes
    const drawPriceChanges = () => {
      if (priceCanvas.value && stockData.value.length > 0) {
        const canvas = priceCanvas.value;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          // Use the initialized dimensions
          canvas.width = canvasWidth;
          canvas.height = canvasHeight;

          // Margins for all edges (left, right, top, bottom)
          const leftMargin = 70;
          const rightMargin = 30;
          const topMargin = 30;
          const bottomMargin = 30;

          // Clear the canvas
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Set background
          ctx.fillStyle = '#000';
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          // Draw vertical lines for the left axis
          const maxPrice = Number(props.company[37 + (2* grafIndex)]); // Maximum price
          const minPrice = Number(props.company[36 + (2* grafIndex)]); // Minimum price
          const numVerticalLines = 5; // Number of value markers
          const verticalGap = (canvasHeight - topMargin - bottomMargin) / numVerticalLines;

          ctx.strokeStyle = '#555';
          ctx.lineWidth = 1;
          ctx.fillStyle = '#fff';
          ctx.font = '12px Arial';

          for (let i = 0; i <= numVerticalLines; i++) {
            const y = canvasHeight - bottomMargin - i * verticalGap;
            const priceValue =
              ((i / numVerticalLines) * (maxPrice - minPrice)) + minPrice;

            // Draw grid line
            ctx.beginPath();
            ctx.moveTo(leftMargin, y);
            ctx.lineTo(canvas.width - rightMargin, y);
            ctx.stroke();

            // Draw price label on the left side of the vertical line
            ctx.fillText(priceValue.toFixed(7), leftMargin - 63, y + 5); // Position label to the left
          }

          // Draw horizontal lines for the bottom axis (time markers)
          const numTimeMarkers = 6; // Number of time markers
          const timeGap =
            (canvas.width - leftMargin - rightMargin) / (numTimeMarkers - 1);
          let timeLabels = ['', '', '', '', '', ''];

          // this one can be bather but now its good :D

          if (grafIndex == 0){
            timeLabels = ['', '4h', '8h', '12h', '16h', '24h'];
          }
          if (grafIndex == 1){
            timeLabels = ['', '1d', '2d', '3d', '4d', '5d'];
          }
          for (let i = 0; i < numTimeMarkers; i++) {
            const x = leftMargin + i * timeGap;

            // Draw grid line
            ctx.beginPath();
            ctx.moveTo(x, topMargin);
            ctx.lineTo(x, canvas.height - bottomMargin);
            ctx.stroke();

            // Draw time label with padding
            ctx.fillText(
              timeLabels[i],
              x - 10,
              canvas.height - bottomMargin + 15
            ); // Position with padding
          }

          // Draw stock data points and lines
          ctx.strokeStyle = '#800080'; // Purple line
          ctx.lineWidth = 2;
          ctx.beginPath();
          let lastValidX: number | null = null;
          let lastValidY: number | null = null;

          stockData.value.forEach((price, index) => {
            const x =
              leftMargin +
              (index / (stockData.value.length - 1)) *
                (canvas.width - leftMargin - rightMargin);
            const y =
              canvas.height -
              bottomMargin -
              ((price - minPrice) / (maxPrice - minPrice)) *
                (canvas.height - topMargin - bottomMargin);

            if (price !== -1) {
              if (lastValidX !== null && lastValidY !== null) {
                // Draw a purple line
                ctx.strokeStyle = '#800080'; // Purple
                ctx.beginPath();
                ctx.moveTo(lastValidX, lastValidY);
                ctx.lineTo(x, y);
                ctx.stroke();
              }

              lastValidX = x;
              lastValidY = y;
            }
          });

          // Draw the last value as a darker purple point
          if (lastValidX !== null && lastValidY !== null) {
            ctx.fillStyle = '#4B0082'; // Dark purple
            ctx.beginPath();
            ctx.arc(lastValidX, lastValidY, 5, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }
    };

    // Handle time period change (currently refetches stock data)
    const changeTimePeriod = (newTimePeriod: number) => {
      grafIndex = newTimePeriod;
      fetchStockData();
    };

    // Automatically refresh stock data every minute
    const startAutoRefresh = () => {
      refreshInterval = window.setInterval(fetchStockData, 60000);
    };

    // Cleanup interval on component unmount
    const stopAutoRefresh = () => {
      if (refreshInterval !== null) {
        clearInterval(refreshInterval);
        refreshInterval = null;
      }
    };

    onMounted(() => {
      initializeCanvas(); // Initialize canvas dimensions on mount
      fetchStockData(); // Fetch initial data on mount
      startAutoRefresh(); // Start auto-refresh
    });

    onBeforeUnmount(() => {
      stopAutoRefresh(); // Stop auto-refresh on unmount
    });

    watch(() => props.company, fetchStockData); // React to company prop changes

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
  padding: 5px 7px;
  cursor: pointer;
  background-color: #610954;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 15px
}

button:hover {
  background-color: #8a0c77;
}

canvas {
  margin-top: 5px;
  display: block;
  width: 100%;
  padding: 10px;
  height: 100%; 
}

.canvas-container {
  width: 100%;
  position: relative;
  height: 100%;
}
.buttons {
  display: flex;
  justify-content: center;
  margin-top: 0px;
  flex-wrap: wrap; /* Ensure buttons wrap properly on mobile */
  gap: 10px; /* Optional: Add space between buttons */
  align-items: center; /* Vertically align the USD label and buttons */
}
.usd-label {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-right: 10px; /* Add space between USD and the first button */
}

@media (max-width: 600px) {
  .buttons {
    flex-direction: row; /* Keep the layout in a row on smaller screens */
    justify-content: center; /* Keep the buttons centered */
  }
  .buttons button {
    font-size: 14px; /* Optionally reduce button size on mobile */
  }
}
</style>
