<template>
  <div>
    <button class="button" :title="title" @click="showAlert">
      {{ title }}
    </button>
  </div>
</template>

<script>
export default {
  name: "button_item",
  props: {
    title: {
      type: String,
    },
  },
  methods: {
    showAlert() {
      alert("Busca Iniciada");
    },
  },
};
</script>

<style>
.button {
  padding: 10px;
  width: 200px;
  border-style: solid;
  border-width: 1px;
  border-radius: 10px;
}

.button:hover {
  background: green;
  color: white;
  transform: scale;
  scale: 1.03;
}
</style>
