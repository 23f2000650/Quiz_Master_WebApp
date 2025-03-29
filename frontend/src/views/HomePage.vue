<template>
    <div class="container">
        <nav class="navbar">
            <h2 class="logo">QuizMaster</h2>
            <div class="nav-buttons">
            <router-link to="/" class="btn">Home</router-link>
            <router-link to="/login" class="btn">Login</router-link>
            <router-link to="/register" class="btn">Sign Up</router-link>
            </div>
        </nav>
        
            <div class="landing">
            <h1>Welcome to QuizMaster</h1>
            <p class="intro">
                QuizMaster is the ultimate destination to test and enhance your knowledge.  
                Engage in thought-provoking quizzes across multiple topics, from science to history.  
                Compete with your friends and track your progress over time.  
                Challenge yourself with AI-powered quizzes that adapt to your skill level.  
                Sign up now to explore a world of interactive learning and endless fun!
            </p>
            </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "HomePage",
  };
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
  }
  
  .container {
    height: 100vh;
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    color: white;
  }
  
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
  
  .landing {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding-top: 60px;
  }
  
  h1 {
    font-size: 3rem;
    margin-bottom: 10px;
  }
  
  .intro {
    font-size: 1.2rem;
    max-width: 600px;
    text-align: center;
    opacity: 0.9;
    line-height: 1.6;
  }
  </style>
  