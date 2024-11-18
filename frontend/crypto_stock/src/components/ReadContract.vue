<script setup lang="ts">
import { useReadContract } from '@wagmi/vue'

// Define the contract configuration
const wagmiContractConfig = {
  addressOrName: '0x34A1D3fff3958843C43aD80F30b94c510645C316',
  contractInterface: ['function balanceOf(address) view returns (uint256)']
}

const { 
  data: balance,
  error,
  isPending
} = useReadContract({
  ...wagmiContractConfig,
  functionName: 'balanceOf',
  args: ['0x03A71968491d55603FFe1b11A9e23eF013f75bCF'],
})
</script>

<template>
  <div v-if="isPending">Loading...</div>

  <div v-else-if="error">
    Error: {{ error.message }}
  </div>

  <div v-else>Balance: {{ balance?.toString() }}</div>
</template>
