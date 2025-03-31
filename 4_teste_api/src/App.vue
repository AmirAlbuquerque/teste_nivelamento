<template>
  <header class="header">
    <TheHeader />
  </header>
  <Input class="input" />
  <button_item title="Buscar" />
</template>

<script>
import Input from "./components/Input.vue";
import TheHeader from "./components/TheHeader.vue";
import button_item from "./components/button.vue";

export default {
  name: "App",
  components: {
    TheHeader,
    Input,
    button_item,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: grey;
  height: 100vw;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 1px;
}

.input {
  padding: 50px 0 0 0;
}
</style>
