<template>
  <div id="app">
    <header class="app-header">
      <h1>📊 EcoPilot</h1>
      <p class="subtitle">Smart Estimation · Informed Decisions · Optimal Planning</p>
    </header>

    <nav>
      <router-link to="/" exact>Home</router-link> |
      <router-link to="/estimation">Estimation</router-link> |
      <router-link to="/finance">Finance</router-link> |
      <router-link to="/risk">Risk</router-link> |
      <router-link to="/scheduling">Scheduling</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style scoped>

nav {
  display: flex;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 12px 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}

nav a {
  margin: 0 10px;
  padding: 8px 16px;
  text-decoration: none;
  color: #007BFF;
  background-color: transparent;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 16px;
}

nav a:hover {
  background-color: rgba(0, 123, 255, 0.1);
  box-shadow: inset 0 0 5px rgba(0, 123, 255, 0.2);
}

.router-link-exact-active {
  background-color: #007BFF;
  color: white !important;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.25);
  border-radius: 6px;
}

.app-header {
  text-align: center;
  margin: 30px 0 20px;
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

.app-header h1 {
  font-size: 36px;
  color: #007BFF;
  margin: 0;
  font-weight: 700;
  letter-spacing: 1px;
}

.app-header .subtitle {
  font-size: 16px;
  color: #555;
  margin-top: 8px;
  font-weight: 400;
  font-style: italic;
}

</style>
