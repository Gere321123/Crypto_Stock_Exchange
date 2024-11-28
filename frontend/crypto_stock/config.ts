import { createConfig, http } from '@wagmi/vue';
import { injected, metaMask, walletConnect } from '@wagmi/vue/connectors';
import { Chain } from '@wagmi/core';

const projectId = 'I did not create it yet';

// Define your local chain
const localhost: Chain = {
  id: 31337, // Standard ID for local development chain
  name: 'Localhost',
  network: 'localhost',
  nativeCurrency: {
    name: 'Ether',
    symbol: 'ETH',
    decimals: 18,
  },
  rpcUrls: {
    default: { http: ['http://127.0.0.1:8545/'] }, // Local RPC URL
  },
  // Omitting blockExplorers as it is optional
};

export const config = createConfig({
  connectors: [
    injected(),
    metaMask(),
    walletConnect({ projectId }),
  ],
  chains: [localhost], // Add your custom chain here
  transports: {
    [localhost.id]: http(localhost.rpcUrls.default.http[0]), // Configure the transport
  },
});
