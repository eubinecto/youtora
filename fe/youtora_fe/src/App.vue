<template>
  <div id="app">
    <nav-bar>

    </nav-bar>

    <p>
      {tmp}
    </p>
  </div>
</template>

<script>
import navBar from "./components/navBar";
export default {
  name: 'App',
  components: {
    navBar
  },
  data() {
    return {
       // tmp = this.$store.state.videoQueryResult
    }
  }
}
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
