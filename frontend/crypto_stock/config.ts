import { createConfig, http } from '@wagmi/vue';
import { injected, metaMask, walletConnect } from '@wagmi/vue/connectors';
import { sepolia } from '@wagmi/vue/chains'
const projectId = 'I did not create it yet';

export const wBTCAddress = "0x3632cdbaC976e471a874F4C384618d749E6Fba85"; // Example address, replace with the actual address

export const config = createConfig({
  connectors: [
    injected(),
    metaMask(),
    walletConnect({ projectId }),
  ],
  chains: [sepolia], // Add your custom chain here
  transports: {
    [sepolia.id]: http(sepolia.rpcUrls.default.http[0]), // Configure the transport
  },
});
