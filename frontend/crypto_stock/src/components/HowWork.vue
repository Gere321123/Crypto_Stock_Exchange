<template>
  <section class="home">
    <div class="home-content">
      <h1>Welcome to Crypto Launchpad 🚀</h1>
      <p>
        We are building a platform where companies can create their own cryptocurrencies 🌐, backed by Wrapped Bitcoin (WBTC) 💰. These cryptocurrencies will be traded by investors and can fluctuate in value based on market conditions 📊. 
      </p>
      <p>
        The funds raised will be used by companies to grow their businesses 🌱. The raised capital will be held in a liquidity pool 💧, where companies will have limited access (e.g., up to 5%) 🏦. If their business generates profits, the companies must repay that amount 🔄.
      </p>
      <p>
        As business owners, we will also benefit from a portion of the liquidity pool 💸, forming the basis of our earnings 💼. 
      </p>
      <p>
        We are planning to expand internationally 🌍, offering businesses around the world an innovative way to raise capital, all while being mindful of legal regulations ⚖️.
      </p>
      <p>
        Join us in creating the future of decentralized finance! 🌟
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomeComponent'
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  color: #ffffff;
  padding: 20px;
  text-align: center;
  margin-top: 5%;
}

.home-content {
  max-width: 700px;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
  line-height: 1.6;
  color: #b0b0b0;
}

.explore-button {
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

.explore-button:hover {
  background-color: #4a4b4e;
}
</style>
