<template>
  <div class="input">
    <label for="nome">Informe a categoria:</label>
    <input type="text" id="nome" v-model="nome" />
  </div>
  <p>À buscar por: {{ nome }}</p>
</template>

<script>
export default {
  name: "UserInput",
  props: {
    msg: String,
  },
  data() {
    return {
      nome: "",
    };
  },
};
</script>

<style>
.input {
  display: flex;
  justify-content: center;
  gap: 30px;
}

#nome {
  width: 50%;
  border-style: solid;
  border-color: black;
  border-width: 2px;
}
</style>
