<template>
  <div class="login-container form-container">
    <h2>Welcome to Quiz Master</h2>
    <h3>Login to your account</h3>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username/Email:</label>
        <input type="text" id="username" v-model="username" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" class="form-control" required />
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <div class="form-actions">
        <button type="submit" class="btn">Login</button>
      </div>
    </form>
    <p>Don't have an account? <router-link to="/register"><span class="registerbtn">Register Here</span></router-link></p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginComponent",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/login`, {
          email: this.username,
          password: this.password,
        });

        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("role", response.data.role);
        localStorage.setItem("user_id", response.data.user);
        console.log("Login successful",response.data.access_token,response.data.role);

        if (localStorage.getItem("role").includes("admin")) {
          this.$router.push("/admin");
        } else {
          this.$router.push("/dashboard");
        }
      } catch (error) {
        this.errorMessage = "Invalid username or password.";
      }
    },
  },
};
</script>

<style scoped>
.registerbtn {
  color: #de8106;
  font-weight: bold;
}

.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 30px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: rgb(67, 0, 90);
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #ffffff;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #a855f7;
  border-radius: 5px;
  font-size: 16px;
  transition: 0.3s;
}

.form-control:focus {
  border-color: #6a0dad;
  box-shadow: 0 0 5px rgba(106, 13, 173, 0.5);
  outline: none;
}

.form-actions {
  margin-top: 20px;
}

.btn {
  width: 100%;
  padding: 12px;
  background: #6a0dad;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

.btn:hover {
  background: #5a0ba0;
}

p {
  margin-top: 15px;
  font-size: 14px;
}

router-link {
  color: #6a0dad;
  text-decoration: none;
  font-weight: bold;
}

router-link:hover {
  text-decoration: underline;
}
</style>
