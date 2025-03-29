<template>
  <div class="register-container form-container">
    <h2>Welcome to Quiz Master</h2>
    <h3>Register for a new account</h3>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="name">Full Name:</label>
        <input type="text" id="name" v-model="name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="qualification">Qualification:</label>
        <input type="text" id="qualification" v-model="qualification" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="dob">Date of Birth:</label>
        <input type="date" id="dob" v-model="dob" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" class="form-control" required />
        <p v-if="passwordMismatch" class="error-message">Passwords do not match!</p>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn">Register</button>
        <button type="button" class="btn btn-secondary" @click="goToLogin">Cancel</button>
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterComponent",
  data() {
    return {
      name: "",
      dob: "",
      email: "",
      qualification: "",
      password: "",
      confirmPassword: "",
      role: "user",
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    passwordMismatch() {
      return this.password !== this.confirmPassword && this.confirmPassword.length > 0;
    },
  },
  methods: {
    async register() {
      if (this.passwordMismatch) {
        this.errorMessage = "Passwords do not match!";
        return;
      }

      const userData = {
        name: this.name,
        dob: this.dob,
        email: this.email,
        qualification: this.qualification,
        password: this.password,
        role: this.role,
      };
      console.log("API URL:", process.env.VUE_APP_API_URL);

      const url = `${process.env.VUE_APP_API_URL}/user/register`;
      console.log(url);
      try {
      const response = await axios.post(url, userData, {
        headers: {
          "Content-Type": "application/json",
          // Do NOT add "Access-Control-Request-Method" manually
        },
        withCredentials: false, // Ensures credentials (cookies, auth) are included if needed
      })

        if (response.status === 200) {
          this.successMessage = "Registration successful!";
          this.$router.push("/login");
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Registration failed. Please try again.";
      }
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>


<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: rgb(67, 0, 90);
  padding: 30px 30px 30px;
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
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 12px;
  background: #6a0dad;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
  flex: 1;
  margin: 0 5px;
}

.btn:hover {
  background: #5a0ba0;
}

.btn-secondary {
  background: #a855f7;
}

.btn-secondary:hover {
  background: #8a2be2;
}

.error-message {
  color: red;
  font-size: 14px;
}

.success-message {
  color: green;
  font-size: 14px;
}
</style>
