<template>
    <div class="search-bar-container">
      <input
        type="text"
        v-model="searchText"
        placeholder="Search by room name"
        @keyup.enter="onSearch"
      />
      <button @click="onSearch">Search</button>
    </div>
  </template>

  <script>
  export default {
    name: 'SearchBar',
    data() {
      return {
        searchText: ''
      };
    },
    methods: {
      onSearch() {
        this.$emit('search', this.searchText);
      }
    }
  };
  </script>

  <style scoped>
  .search-bar-container {
    display: flex;
    justify-content: center;
    margin-top: 50px;
    padding: 20px;
  }

  input[type="text"] {
    padding: 10px;
    font-size: 1em;
    width: 300px;
    border: 1px solid #ccc;
    border-radius: 4px 0 0 4px;
    outline: none;
  }

  button {
    padding: 10px 20px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-left: none;
    border-radius: 0 10px 10px 0;
    background-color: #000000;
    color: #fff;
    cursor: pointer;
    outline: none;
  }
  </style>
