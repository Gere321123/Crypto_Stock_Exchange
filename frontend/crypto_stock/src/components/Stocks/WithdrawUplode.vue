<script setup lang="ts">
import { ref, defineExpose } from 'vue';
import { useConnect, useChainId, useAccount, useDisconnect, useWriteContract } from '@wagmi/vue';
import {wBTCAddress} from '../../../config';
const { 
  error,
  writeContract 
} = useWriteContract();


const props = defineProps<{
  uplodemoney: boolean;
  loginasCompany: boolean;
  sendValue: number;
  address: `0x${string}`;
  network: string;
}>();

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

// ABI for interacting with the smart contract
const contractAbi = [
{
    type: 'function',
    name: 'withdrawCompany',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'withdrawValueinWei', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'uplodeMoney',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'wBTCAmount', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'withdowOwners',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'withdrawValueinWei', type: 'uint256' }
    ],
    outputs: []
  },
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

// Approve the transaction

const approve = async () => {
  try {
    if (props.uplodemoney) {
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
    if (props.loginasCompany){
    if (props.uplodemoney) {
    writeContract({ 
          address: props.address, 
          abi: contractAbi, 
          functionName: 'uplodeMoney',
          args: [props.sendValue * 10 ** 18],
        });
    } else {
      writeContract({ 
        address: props.address, 
        abi: contractAbi, 
        functionName: 'withdrawCompany',
        args: [props.sendValue * 10 ** 18],
      });

    }
  }else{
    writeContract({ 
        address: props.address, 
        abi: contractAbi, 
        functionName: 'withdowOwners',
        args: [props.sendValue * 10 ** 18],
      });
  }
  } catch (error) {
    console.error('Transaction error:', error);
  }
};

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
        <!-- Address and Value -->
        <p>Address: {{ address }}</p>
        <p>Value: {{ sendValue }}</p>

        <!-- Conditional Button Text -->
        <p>{{ uplodemoney ? 'Buy Tokens' : 'Sell Tokens' }}</p>
        
      <button v-if="props.uplodemoney && props.loginasCompany" @click="approve()">
      Approve
    </button>
      <button  @click="send()">
      Send
    </button>
  <div v-if="error">
    {{error.message}}
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

.modal-content {
  background: rgb(20, 20, 20);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>