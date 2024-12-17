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
  overflow: auto; /* Allows scrolling */
}

#app {
  display: flex;
  flex-direction: column;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #e1e1e1;
  background-color: #29293d;
  min-height: 100vh; /* Ensures the app takes at least the full viewport height */
  width: 100%; /* Full width */
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 10px; /* Width of the vertical scrollbar */
  height: 10px; /* Height of the horizontal scrollbar */
}

::-webkit-scrollbar-track {
  background: #2c2d30; /* Track background color */
  border-radius: 5px; /* Rounded corners for the track */
}

::-webkit-scrollbar-thumb {
  background: #555; /* Thumb color */
  border-radius: 5px; /* Rounded corners for the thumb */
}

::-webkit-scrollbar-thumb:hover {
  background: #888; /* Thumb color on hover */
}

/* Firefox scrollbar styling */
body {
  scrollbar-width: thin; /* Makes the scrollbar thinner */
  scrollbar-color: #555 #2c2d30; /* Thumb and track colors */
}
button{
  margin: 30px;
  padding: 12px 24px;
  font-size: 1em;
  color: #ffffff;
  background-color: #3a3b3e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #4a4b4e;
}
input {
  width: 10%;
  padding: 10px;
  margin: 10px 0;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Focused input styling */
input:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  outline: none;
}

/* Disabled input styling */
input:disabled {
  background-color: #f5f5f5;
  border-color: #e0e0e0;
  color: #a0a0a0;
  cursor: not-allowed;
}

/* Label styling */
label {
  display: block;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #d2d2d2;
}

/* Styling for error state */
input.error {
  border-color: #dc3545;
  box-shadow: 0 0 5px rgba(220, 53, 69, 0.5);
}

label.error {
  color: #dc3545;
}

/* Styling for success state */
input.success {
  border-color: #28a745;
  box-shadow: 0 0 5px rgba(40, 167, 69, 0.5);
}

label.success {
  color: #28a745;
}

/* Responsive design: inputs and labels adapt for smaller screens */
@media (max-width: 768px) {
  input {
    font-size: 14px;
  }

  label {
    font-size: 12px;
  }
}
</style>