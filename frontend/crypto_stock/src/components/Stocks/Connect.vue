<script setup lang="ts">
import { ref, defineExpose } from 'vue';
import { useConnect, useChainId, useAccount, useDisconnect, useWriteContract } from '@wagmi/vue';

const { 
  error,
  writeContract 
} = useWriteContract();


const props = defineProps<{
  showBuy: boolean;
  sendValue: number;
  address: `0x${string}`;
  network: string;
}>();

const chainId = useChainId();
const { connectors, connect } = useConnect();
const { address } = useAccount();
const { disconnect } = useDisconnect();
const errorMessage = ref('');

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// ABI for interacting with the smart contract
const contractAbi = [
  // Function definitions
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

  // Custom error definitions
  {
    type: 'error',
    name: 'Coin__MustBeMoreThanZero',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__NotEnoughTokensAvailable',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__InsufficientTokens',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__NotAuthorized',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__BurnMoreThanTheTokensInTheMarcatCap',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__InsufficientWBTC',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__WBTCTransferFailed',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__FailedToSendWBTC',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__InsufficientWBTCInContract',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__FailedToReceiveWBTC',
    inputs: [],
  },
  {
    type: 'error',
    name: 'Coin__ERC20InsufficientAllowance',
    inputs: [],
  },
];

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
];

// Replace this with your actual wBTC contract address
const wBTCAddress = "0x3632cdbaC976e471a874F4C384618d749E6Fba85"; // Example address, replace with the actual address

// Approve the transaction

const approve = async () => {
  try {
    if (props.showBuy) {
      writeContract({ 
        address: wBTCAddress, 
        abi: wBTCAbi, 
        functionName: 'approve',
        args: [props.address, props.sendValue * 10 ** 18],
      });
    } 
  } catch (error) {
    console.error('Transaction error:', error);
  }
      }

const send = async () => {
  try {
    if (props.showBuy) {
    writeContract({ 
          address: props.address, 
          abi: contractAbi, 
          functionName: 'buyTokens',
          args: [props.sendValue * 10 ** 18],
        });
    } else {
      writeContract({ 
        address: props.address, 
        abi: contractAbi, 
        functionName: 'sellTokens',
        args: [props.sendValue * 10 ** 18],
      });

    }
  } catch (error) {
    console.error('Transaction error:', error);
  }
};
const handleError = (error: any) => {
  if (error.message.includes('Coin__ERC20InsufficientAllowance')) {
    errorMessage.value = 'You have not approved the transaction.';
  } else if (error.message.includes('Coin__NotEnoughTokensAvailable')) {
    errorMessage.value = 'Not enough tokens available.';
  } else if (error.message.includes('Coin__InsufficientTokens')) {
    errorMessage.value = 'Insufficient tokens.';
  } else if (error.message.includes('Coin__NotAuthorized')) {
    errorMessage.value = 'You are not authorized.';
  } else if (error.message.includes('Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed')) {
    errorMessage.value = 'Company is trying to withdraw more than allowed.';
  } else if (error.message.includes('Coin__BurnMoreThanTheTokensInTheMarcatCap')) {
    errorMessage.value = 'Burn amount exceeds market cap.';
  } else if (error.message.includes('Coin__InsufficientWBTC')) {
    errorMessage.value = 'Insufficient WBTC.';
  } else if (error.message.includes('Coin__WBTCTransferFailed')) {
    errorMessage.value = 'WBTC transfer failed.';
  } else if (error.message.includes('Coin__FailedToSendWBTC')) {
    errorMessage.value = 'Failed to send WBTC.';
  } else if (error.message.includes('Coin__InsufficientWBTCInContract')) {
    errorMessage.value = 'Insufficient WBTC in contract.';
  } else if (error.message.includes('Coin__FailedToReceiveWBTC')) {
    errorMessage.value = 'Failed to receive WBTC.';
  } else {
    errorMessage.value = 'An unknown error occurred.';
  }
};
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
        
      <button v-if="props.showBuy" @click="approve()">
      Approve
    </button>
      <button  @click="send()">
      Send
    </button>
    <div v-if="error && errorMessage">
          <p class="error-message">{{ errorMessage }}</p>
    </div>
    <div v-if="error && !errorMessage">
          <p class="error-message">Unknow error</p>
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