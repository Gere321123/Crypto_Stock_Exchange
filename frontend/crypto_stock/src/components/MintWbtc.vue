<template>
  <div v-if="isOpen" class="modal">
    <h2>Mint Wrapped Bitcoin (WBTC)</h2>
    <button @click="mintToken" :disabled="loading">{{ loading ? 'Minting...' : 'Mint 0.01 WBTC' }}</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Modal Close Button -->
    <button @click="closeModal">Close</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useWriteContract } from '@wagmi/vue';
import { wBTCAddress } from '../../config';
const { writeContract } = useWriteContract();

const isOpen = ref(false);  // Controls modal visibility

// Method to open the modal
const openModal = () => {
  isOpen.value = true;
};

// Method to close the modal
const closeModal = () => {
  isOpen.value = false;
};

// ABI for the mint function
const wBTCAbi = [
  {
    inputs: [],
    name: "mint",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  }
];

const errorMessage = ref('');
const loading = ref(false); // To track the loading state during minting

const mintToken = async () => {
  loading.value = true; // Set loading state to true when minting starts
  try {
    await writeContract({
      address: wBTCAddress,
      abi: wBTCAbi,
      functionName: 'mint',
    });
    errorMessage.value = '';  // Clear any previous error
  } catch (error) {
    console.error('Error during minting:', error);
    errorMessage.value = 'An error occurred while minting.';
  } finally {
    loading.value = false; // Reset loading state once the minting process is complete
  }
};

// Expose the `openModal` function and `isOpen` state to the parent component
defineExpose({ openModal });
</script>

<style scoped>
.mint-container {
  text-align: center;
  padding: 20px;
  background-color: #333;
  border-radius: 8px;
  color: white;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #777;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.success-message {
  color: green;
  font-weight: bold;
}

.error-message {
  color: red;
  font-weight: bold;
}
</style>
