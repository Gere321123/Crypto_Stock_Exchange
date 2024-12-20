<script setup lang="ts">
import { ref, defineExpose } from 'vue';
import { useConnect, useChainId, useAccount, useDisconnect, useWriteContract } from '@wagmi/vue';
import { wBTCAddress } from '../../../config';

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
const canWithdraw = ref(false);
const withdrawalPercentage = ref(0);

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
    type: 'function',
    name: 'setCompanyCanWithdraw',
    stateMutability: 'nonpayable',
    inputs: [
      { name: '_companyCanWithdraw', type: 'bool' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'setcompanyWithdrawalPercentage',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'newcompanyWithdrawalPercentage', type: 'uint8' }
    ],
    outputs: []
  },
  {
    type: 'error',
    name: 'Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed',
    inputs: [],
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
];

// Approve the transaction
const approve = async () => {
  try {
    if (props.uplodemoney) {
      writeContract({ 
        address: wBTCAddress, 
        abi: contractAbi, 
        functionName: 'approve',
        args: [props.address, props.sendValue * 10 ** 18],
      });
    } 
  } catch (error) {
    console.error('Transaction error:', error);
  }
};

const send = async () => {
  try {
    if (props.loginasCompany) {
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
    } else {
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

const setCompanyWithdraw = async () => {
  try {
    writeContract({ 
      address: props.address, 
      abi: contractAbi, 
      functionName: 'setCompanyCanWithdraw',
      args: [canWithdraw.value],
    });
  } catch (error) {
    console.error('Transaction error:', error);
  }
};

const setWithdrawalPercentage = async () => {
  try {
    writeContract({ 
      address: props.address, 
      abi: contractAbi, 
      functionName: 'setcompanyWithdrawalPercentage',
      args: [withdrawalPercentage.value],
    });
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
        <button @click="send()">
          Send
        </button>

        <div v-if="!props.loginasCompany">
          <!-- Checkbox for setCompanyCanWithdraw -->
          <label>
            <input type="checkbox" v-model="canWithdraw" /> Enable Company Withdraw
          </label>
          <button @click="setCompanyWithdraw()">Set Withdraw Permission</button>

          <!-- Input for setcompanyWithdrawalPercentage -->
          <label>
            Withdrawal Percentage:
            <input 
              type="number" 
              v-model="withdrawalPercentage" 
              min="0" 
              max="100"
            />
          </label>
          <button @click="setWithdrawalPercentage()">Set Withdrawal Percentage</button>
        </div>

        <div v-if="error">
          {{ error.message }}
        </div>

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