<script setup lang="ts">
import { ref, defineExpose, watch } from 'vue';
import { useConnect, useChainId, useAccount, useDisconnect, useWriteContract, useWaitForTransactionReceipt } from '@wagmi/vue';
import { keccak256, toUtf8Bytes, Contract } from "ethers";
const { 
  data: hash,
  error,
  isPending,
  writeContract 
} = useWriteContract()
const props = defineProps<{
  showBuy: boolean;
  sendValue: number;
  address: `0x${string}`;
  network: string;
}>();

const chainId = useChainId();
const { connectors, connect } = useConnect();
const { address, connector } = useAccount();
const { disconnect } = useDisconnect();

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// ABI for interacting with the smart contract
const contractAbi = [
  {
    type: 'function',
    name: 'buyTokens',
    stateMutability: 'nonpayable',
    inputs: [{ name: 'wBTCAmount', type: 'uint256' }],
    outputs: [],
  },
  {
    type: 'function',
    name: 'sellTokens',
    stateMutability: 'nonpayable',
    inputs: [{ name: '_tokenAmount', type: 'uint256' }],
    outputs: [],
  },
];
// Define the wBTC contract ABI and address
const wBTCAbi = [
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  // Include other necessary ABI entries for wBTC contract interactions
];

// Replace this with your actual contract address
const wBTCAddress = "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707"; // Example address, replace with the actual address

// Get the provider from wagmi
// const provider = useProvider();

// Create the wBTC contract instance
// const wBTC = new Contract(wBTCAddress, wBTCAbi, provider);
const send = function() {
  const errorSignatures = [
  "Coin__MustBeMoreThanZero()",
  "Coin__NotEnoughTokensAvailable()",
  "Coin__InsufficientTokens()",
  "Coin__NotAuthorized()",
  "Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed()",
  "Coin__BurnMoreThanTheTokensInTheMarcatCap()",
  "Coin__InsufficientWBTC()",
  "Coin__WBTCTransferFailed()",
  "Coin__FailedToSendWBTC()",
  "Coin__InsufficientWBTCInContract()",
  "Coin__FailedToReceiveWBTC()",
];

// Compute and log each error's Keccak256 hash
errorSignatures.forEach((signature) => {
  const hash = keccak256(toUtf8Bytes(signature));
  console.log(`${signature}: ${hash}`);
});
  if (props.showBuy){
    // const approveTx = await wBTC.approve(contractAddress, approvalAmount);
    // await approveTx.wait();
  writeContract({
    address: props.address, 
    abi: contractAbi, 
    functionName: 'buyTokens',
    args: [props.sendValue * 10 ** 18],
    chainId: 31337 as any,
  })
  }else{
    writeContract({
    address: props.address, 
    abi: contractAbi, 
    functionName: 'sellTokens',
    args: [props.sendValue * 10 ** 18],
    chainId: 31337 as any,
  })
  }
};

const { isLoading: isConfirming, isSuccess: isConfirmed } =
  useWaitForTransactionReceipt({
    hash,
  })
// Expose openModal method to be called from parent component
defineExpose({ openModal });
</script>

<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2>Connect Wallet</h2>

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
        <!-- Address and Value -->
        <p>Address: {{ address }}</p>
        <p>Value: {{ sendValue }}</p>

        <!-- Conditional Button Text -->
        <p>{{ showBuy ? 'Buy Tokens' : 'Sell Tokens' }}</p>

          <button :disabled="isPending" @click="send()">
      <span v-if="isPending">Sending...</span>
      <span v-else>Send</span>
    </button>
    <div v-if="hash">Transaction Hash: {{ hash }}</div>
    <div v-if="isConfirming">Waiting for confirmation...</div>
    <div v-if="isConfirmed">Transaction Confirmed!</div>
    <div v-if="error">
      Error: {{ error.message }}
    </div>

        <!-- Disconnect Button -->
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

.modal-content {
  background: rgb(20, 20, 20);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
