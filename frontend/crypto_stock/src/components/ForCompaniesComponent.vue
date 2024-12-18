<template>
  <section class="for-companies">
    <h1>For Companies</h1>
    <p>
      🌟 Welcome to the test version of Crypto Stock!We are a team dedicated to helping companies raise capital through Wrapped Bitcoin (WBTC). 
      This innovative process enables businesses to bypass traditional financial systems, offering a decentralized way to 
      secure investments from a global pool of crypto investors.
    </p>
    <p>
      🤝 Are you a Legal expert, an Animator, a Businessperson, or do you know companies that might be 
      interested in this? If so, we'd love to hear from you! You can contact us via Telegram at 
      <a href="https://t.me/Brate113" target="_blank" class="styled-link">@Brate113</a>, or send us an 
      email at <a href="mailto:gergely.gere@gmail.com" class="styled-link">gergely.gere@gmail.com</a>.
    </p>
    <p>
      ❓ Have questions? Don't hesitate to reach out! We are a friendly team and always happy to help.
    </p>
    <p>
      🛠️ Since this is a test version, you can receive test coins to explore the platform. Get started with 
      some test Sepolia ETH or WBTC using the buttons below:
    </p>
    <p>
      🔑 To log in, use the credentials below to test the platform:
      <br>
      <strong>Username:</strong> Gebi
      <br>
      <strong>Password:</strong> asd
      <br>
      🙇 <strong>Please don't change the password because others may want to try it.</strong>
    </p>
    <p>
      🔗 <a href="/login" class="styled-link">Click here to log in</a>
    </p>
    <button
      class="get-started-button"
      @click="openLink"
    >
      💸 Get test Sepolia ETH
    </button>
    <button 
      class="get-started-button" 
      @click="handleGetStarted"
    >
      💰 Get test WBTC
    </button>
    <MintWbtc ref="connectComponent" />
  </section>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import MintWbtc from './MintWbtc.vue'; // Make sure this path is correct

export default defineComponent({
  name: 'ForCompaniesComponent',
  components: { MintWbtc },
  setup() {
    const connectComponent = ref();

    const handleGetStarted = () => {
      if (connectComponent.value) {
        connectComponent.value.openModal();
      } else {
        console.error("connectComponent is not defined or doesn't have openModal function.");
      }
    };

    return {
      handleGetStarted,
      connectComponent,
    };
  },
  methods: {
  openLink() {
    window.open('https://cloud.google.com/application/web3/faucet/ethereum/sepolia', '_blank');
  },
},
});
</script>

<style scoped>
.for-companies {
  display: flex;                /* Enable flexbox */
  flex-direction: column;       /* Stack children vertically */
  align-items: center;          /* Center children horizontally */
  color: #ffffff;              /* Text color */
  padding: 20px;               /* Padding */
  text-align: center;          /* Center text */
  margin-top: 2%;          /* Margin at the top */
  max-width: 700px;            /* Max width for the content */
  margin-left: auto;           /* Center horizontally */
  margin-right: auto;          /* Center horizontally */
}
.styled-link {
  color: #921ca2;
  text-decoration: none;
  font-weight: bold;
}

.styled-link:hover {
  text-decoration: underline;
  color: #c71ade;
}
h1 {
   font-size: 2.5em;
   margin-bottom: 20px;
 }

p {
  font-size: 1.2em;
  color: #b0b0b0;
  margin: 15px 0;
}

.get-started-button {
  margin-top: 30px;
  padding: 12px 24px;
  font-size: 1em;
  color: #ffffff;
  background-color: #3a3b3e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.get-started-button:hover {
  background-color: #4a4b4e;
}
</style>