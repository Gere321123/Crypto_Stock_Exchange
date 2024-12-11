import { http, createConfig, createStorage } from '@wagmi/vue'
import { mainnet, optimism, sepolia } from '@wagmi/vue/chains'
import { coinbaseWallet, walletConnect } from '@wagmi/vue/connectors'
import { type Chain } from 'viem'

const localhost: Chain = {
  id: 31337, // Standard ID for local development chain
  name: 'Localhost',
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
  chains: [mainnet, sepolia, optimism, localhost], // Add localhost chain here
  connectors: [
    walletConnect({
      projectId: import.meta.env.VITE_WC_PROJECT_ID || '', // Ensure this is defined
    }),
    coinbaseWallet({ appName: 'Vite Vue Playground', darkMode: true }),
  ],
  storage: createStorage({ storage: localStorage, key: 'vite-vue' }),
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
    [optimism.id]: http(),
    [localhost.id]: http(), // Ensure localhost transport is added
  },
})

declare module '@wagmi/vue' {
  interface Register {
    config: typeof config
  }
}
