<template>
    <p class="error-message">{{ message }}</p>
  </template>
  
  <script setup>
  defineProps({ message: String });
  </script>
  
  <style scoped>
  .error-message {
    color: red;
    font-size: 14px;
    margin-top: 10px;
  }
  </style>
  