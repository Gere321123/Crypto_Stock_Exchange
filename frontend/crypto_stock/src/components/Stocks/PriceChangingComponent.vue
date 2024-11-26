<template>
  <div class="price-changing-component">
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
    
    const drawPriceChanges = () => {
      if (priceCanvas.value) {
        const ctx = priceCanvas.value.getContext('2d');
        if (ctx) {
          ctx.clearRect(0, 0, priceCanvas.value.width, priceCanvas.value.height);
          ctx.fillStyle = '#000';
          ctx.fillRect(0, 0, priceCanvas.value.width, priceCanvas.value.height);
          ctx.fillStyle = '#fff';
          ctx.font = '20px Arial';
          ctx.fillText(`Price changes for ${props.company[2]}`, 50, 100);
        }
      }
    };

    onMounted(() => {
      drawPriceChanges();
    });

    watch(() => props.company, drawPriceChanges);

    return {
      showBuy,
      showSell,
      ethAmount,
      tokensAmount,
      tokensToReceive,
      ethToReceive,
      priceCanvas,
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
}

input {
  margin-top: 10px;
  padding: 5px;
  width: 80%;
}
</style>
