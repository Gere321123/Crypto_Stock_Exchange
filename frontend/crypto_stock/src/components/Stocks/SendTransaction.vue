<script setup lang="ts">
  import { 
    useSendTransaction,
    useWaitForTransactionReceipt,
  } from '@wagmi/vue'
  import { parseEther } from 'viem'

  const { 
    data: hash, 
    error,
    isPending,
    sendTransaction 
  } = useSendTransaction()

  function submit(event: Event) {
    const formData = new FormData(event.target as HTMLFormElement)
    const to = formData.get('address') as `0x${string}`
    const value = formData.get('value') as string
    sendTransaction({ to, value: parseEther(value) })
  }

  const { isLoading: isConfirming, isSuccess: isConfirmed } = 
    useWaitForTransactionReceipt({ 
      hash, 
    }) 
</script>

<template>
  <form @submit.prevent="submit">
    <input name="address" placeholder="0x34A1D3fff3958843C43aD80F30b94c510645C316" required />
    <input name="value" placeholder="0" required />
    <button :disabled="isPending" type="submit">
      <span v-if="isPending">Sending...</span>
      <span v-else>Send</span>
    </button>
    <div v-if="hash">Transaction Hash: {{ hash }}</div>
    <div v-if="isConfirming">Waiting for confirmation...</div> 
    <div v-if="isConfirmed">Transaction Confirmed!</div> 
    <div v-if="error">
      Error: {{ error.message }}
    </div>
  </form>
</template>