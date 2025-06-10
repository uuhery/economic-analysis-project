<template>
  <div id="app">
    <h1>Economic Analysis & Decision Tool</h1>
    <nav>
      <router-link to="/" exact>Home</router-link> |
      <router-link to="/estimation">Estimation</router-link> |
      <router-link to="/finance">Finance</router-link> |
      <router-link to="/risk">Risk</router-link> |
      <router-link to="/scheduling">Scheduling</router-link>
    </nav>
    <hr />
    <router-view />
  </div>
</template>

<style scoped>
nav {
  margin-bottom: 10px;
}
nav a {
  margin-right: 12px;
  text-decoration: none;
  color: #42b983;
  padding-bottom: 3px;
  border-bottom: 2px solid transparent;
  font-weight: normal;
  transition: all 0.2s ease;
}
.router-link-exact-active {
  color: #35495e;
  border-bottom: 2px solid #35495e;
  font-weight: bold;
}
</style>
