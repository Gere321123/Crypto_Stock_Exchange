import { Buffer } from 'buffer'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { WagmiPlugin } from '@wagmi/vue'
import router from './router'
import { createApp } from 'vue'

// `@coinbase-wallet/sdk` uses `Buffer`
globalThis.Buffer = Buffer

import App from './App.vue'
import './style.css'
import { config } from './wagmi'

const app = createApp(App)

app.use(WagmiPlugin, { config })
app.use(VueQueryPlugin, {})
app.use(router)

app.mount('#app')
