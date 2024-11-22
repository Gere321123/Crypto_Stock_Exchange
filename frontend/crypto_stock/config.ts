import { createConfig, http } from '@wagmi/vue';
import { bscTestnet } from '@wagmi/vue/chains'; // Import the BNB Testnet chain
import { injected, metaMask, walletConnect } from '@wagmi/vue/connectors';

const projectId = 'I did not created yet';

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