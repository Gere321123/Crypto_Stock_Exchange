<script setup lang="ts">
import { ref, defineExpose } from 'vue';
import { useConnect, useChainId, useAccount, useDisconnect, useWriteContract } from '@wagmi/vue';
import {wBTCAddress} from '../../config';
const { 
  error,
  writeContract 
} = useWriteContract();


const chainId = useChainId();
const { connectors, connect } = useConnect();
const { address } = useAccount();
const { disconnect } = useDisconnect();

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// wBTC Contract ABI
const wBTCAbi = [
  {
    inputs: [
      { internalType: "address", name: "spender", type: "address" },
      { internalType: "uint256", name: "amount", type: "uint256" },
    ],
    name: "approve",
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [],
    name: "mint",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
];



// Approve the transaction

const mint = async () => {
  try {
      writeContract({ 
        address: wBTCAddress, 
        abi: wBTCAbi, 
        functionName: 'mint',
      });
  } catch (error) {
    console.error('Transaction error:', error);
  }
}

// Expose openModal method to be called from parent component
defineExpose({ openModal });
</script>

<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2>Use Sepolia Testnet!</h2>

      <!-- Display Connect Options or Connected Info -->
      <div v-if="!address">
        <!-- Wallet Connect Buttons -->
        <button
          v-for="connector in connectors"
          :key="connector.id"
          @click="connect({ connector, chainId })"
        >
          {{ connector.name }}
        </button>
      </div>
      
      <div v-else>
        
      <button @click="mint()">
        Get test wBTC
    </button>
    <div v-if="error">
      error
    </div>
        <!--&& error.message.substring(73, 85) === '0x2e9d4e44' Disconnect Button -->
        <button @click="disconnect()">Disconnect</button>
      </div>

      <!-- Close Button -->
      <button @click="closeModal">Close</button>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.error-message{
  color: tomato
}
.modal-content {
  background: rgb(20, 20, 20);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>