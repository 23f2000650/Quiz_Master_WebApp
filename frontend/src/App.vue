<template>
  <div id="app">
    <!-- Main Content -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

/* App Container */
#app {
  background: linear-gradient(135deg, #1f1c2c, #928dab);
  color: white;
  min-height: 120vh;
  text-align: center;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 50px;
  background: rgba(0, 0, 0, 0.3);
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  z-index: 1000;
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
}

.nav-buttons {
  display: flex;
  gap: 15px;
}

.btn {
  text-decoration: none;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  transition: 0.3s;
  font-size: 1rem;
  border: 2px solid white;
}

.btn:hover {
  background: white;
  color: black;
}

/* Content */
.content {
  padding-top: 80px;
}
</style>
