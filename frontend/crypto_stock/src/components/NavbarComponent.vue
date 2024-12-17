<template>
  <nav class="navbar">
    <div class="navbar-logo">Crypto Stock</div>

    <!-- Hamburger Icon -->
    <div class="hamburger" @click="toggleMenu">
      <div></div>
      <div></div>
      <div></div>
    </div>

    <!-- Navigation Links -->
    <ul class="navbar-links" :class="{ active: isMenuOpen }">
      <li><router-link to="/" @click="closeMenu">Home</router-link></li>
      <li><router-link to="/buy-sell" @click="closeMenu">Buy/Sell</router-link></li>
      <li><router-link to="/for-companies" @click="closeMenu">For Companies</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavbarComponent",
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
  },
};
</script>

<style scoped>
/* Main Navbar Styles */
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

/* Hamburger Menu */
.hamburger {
  display: none;
  flex-direction: column;
  cursor: pointer;
  gap: 5px;
}

.hamburger div {
  width: 25px;
  height: 3px;
  background-color: #ffffff;
  border-radius: 4px;
  transition: all 0.3s ease;
}

/* Navbar Links */
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

/* Responsive Styles */
@media screen and (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .navbar-links {
    display: none;
    flex-direction: column;
    background-color: #232427;
    position: absolute;
    top: 60px;
    right: 0;
    width: 100%;
    padding: 10px 0;
    text-align: center;
    gap: 15px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
    z-index: 10;
  }

  .navbar-links.active {
    display: flex;
  }

  .navbar-links li {
    margin: 0;
  }

  .navbar-links a {
    display: block;
    width: 100%;
    padding: 12px;
    color: #ffffff;
  }
}
</style>
