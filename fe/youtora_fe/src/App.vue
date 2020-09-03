<template>
  <div id="app">
    <nav-bar/>
    <video-list/>
    <Foot/>
  </div>
</template>

<script>
import navBar from "./components/navBar";
import videoList from "./components/videoList";
import Foot from "./components/footer";

export default {
  name: 'App',
  components: {
    navBar,
    videoList,
    Foot
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
