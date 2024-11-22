import { createConfig, http } from '@wagmi/vue';
import { bscTestnet } from '@wagmi/vue/chains'; // Import the BNB Testnet chain
import { injected, metaMask, walletConnect } from '@wagmi/vue/connectors';

const projectId = '0x988E411D1eE2476847241c3983312356daf749f0';

export const config = createConfig({
  connectors: [
    injected(),
    metaMask(),
    walletConnect({ projectId }),
  ],
  chains: [bscTestnet], // Use the BNB Testnet chain
  transports: {
    [bscTestnet.id]: http(), // Add transport for BNB Testnet
  },
});