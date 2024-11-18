<template>
  <section class="home">
    <div class="home-content">
      <h1>Welcome to Crypto Stock</h1>
      <p>
        This platform allows companies to raise capital using Ethereum. Unlike traditional stocks, 
        where shares are bought with dollars, here companies can issue tokens backed by Ethereum. 
        These tokens represent a stake in the company, helping businesses grow and innovate 
        with the support of crypto investors.
      </p>
      <p>
        Join us in building a new era of decentralized funding, where growth and innovation 
        know no borders.
      </p>
      <button class="explore-button">Explore Companies</button>
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
  min-height: 100vh;
  color: #ffffff;
  padding: 20px;
  text-align: center;

  margin-top: 130px;
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
