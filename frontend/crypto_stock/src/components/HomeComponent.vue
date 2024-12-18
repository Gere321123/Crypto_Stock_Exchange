<template>
  <section class="home">
    <div class="home-content">
      <h1>Welcome to Crypto Stock 🚀</h1>
      <p>
        This platform allows companies to raise capital by issuing shares in Wrapped Bitcoin 💰, instead of using traditional fiat currencies 💵. In contrast to the usual stock market where shares are purchased with dollars 💸, here companies can create tokens backed by Wrapped Bitcoin 🔗. These tokens serve as a digital asset that represents ownership in the company 🏢, providing businesses with an innovative way to raise funds 🚀. By leveraging the power of blockchain technology 🌐, companies can tap into a global network of crypto investors 🌍, enabling growth and fostering innovation without the barriers of conventional finance 📈.
      </p>
      <p>
        Join us in building a new era of decentralized funding 🤝, where growth and innovation know no borders 🌏.
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
