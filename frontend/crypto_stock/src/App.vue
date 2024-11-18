<template>
  <NavbarComponent/>
  <router-view></router-view> 
</template>

<script>
import NavbarComponent from './components/NavbarComponent.vue';
export default {
  name: 'App',
  components: {
    NavbarComponent,
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden; /* Prevents scrolling */
}

#app {
  display: flex;
  flex-direction: column;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #e1e1e1;
  background-color: rgb(35, 36, 39);
  height: 100vh; /* Full viewport height */
  width: 100vw; /* Full viewport width */
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

</style>