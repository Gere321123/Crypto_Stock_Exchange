<template>
  <nav class="navbar">
    <div class="navbar-logo">Crypto Stock</div>
    <ul class="navbar-links">
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/buy-sell">Buy/Sell</router-link></li>
      <li><router-link to="/for-companies">For Companies</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavbarComponent'
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #232427;
  padding: 20px 40px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.navbar-logo {
  font-size: 1.5em;
  font-weight: bold;
  color: #ffffff;
  cursor: pointer;
}

.navbar-links {
  list-style-type: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.navbar-links li {
  font-size: 1em;
}

.navbar-links a {
  color: #b0b0b0;
  text-decoration: none;
  padding: 8px 16px;
  transition: color 0.3s, background-color 0.3s;
  border-radius: 4px;
}

.navbar-links a:hover {
  color: #ffffff;
  background-color: #3a3b3e;
}
</style>