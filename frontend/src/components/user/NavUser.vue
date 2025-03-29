<template>
    <div class="user-dashboard container">
      <nav class="navbar">
        <h2>User Panel</h2>
        <div class="nav-links">
            <button @click="$router.push('/dashboard')">Home</button>
            <button @click="$router.push('/user/quiz')">Quiz</button>
            <button @click="$router.push('/user/scores')">Score</button>
            <button @click="$router.push('/user/summary')">Summary</button>
            <button @click="logout()" class="btn-danger">Logout</button>
        </div>

    </nav>
    </div>
</template>

<script>
export default {
  name: 'NavUser',
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('user_id');
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  padding: 20px;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  padding: 15px;
  color: white;
}

.nav-links button {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  margin: 0 10px;
  cursor: pointer;
}

.search-bar {
  padding: 5px;
  font-size: 16px;
}

</style>