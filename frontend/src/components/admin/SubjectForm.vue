<template>
    <div class="subject-form container">
      <h2>{{ isEditing ? 'Edit Subject' : 'Create New Subject' }}</h2>
      
      <div class="form-container">
        <form @submit.prevent="saveSubject">
          <div class="form-group">
            <label for="name">Subject Name:</label>
            <input type="text" id="name" v-model="subject.name" class="form-control" required />
          </div>
          
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" v-model="subject.description" class="form-control" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label for="credits">Credits:</label>
            <input type="number" id="credits" v-model="subject.credits" class="form-control" min="1" required />
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn">Save</button>
            <button type="button" @click="cancel" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>
  import axios from 'axios';
export default {
    name: 'SubjectForm',
    props: {
      id: {
        type: [String, Number],
        required: false
      }
    },
    data() {
      return {
        subject: {
          name: '',
          description: '',
          credits: null
        },
        isEditing: false
      };
    },
    created() {
      if (this.id) {
        this.isEditing = true;
        this.fetchSubject();
      }
    },
    methods: {
      async fetchSubject() {
        const url = `${process.env.VUE_APP_API_URL}/admin/subject/${this.id}`;
        try {
          const response = await axios.get(url,
            {
              headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`,
              },
            }
          );
          this.subject = response.data;
        } catch (error) {
          console.error('Error:', error);
        }
      },
      async saveSubject() {
        console.log('Saving subject:', this.subject);
        const userdata ={
          name: this.subject.name,
          description: this.subject.description,
          credits: this.subject.credits
        }
        
        const url = `${process.env.VUE_APP_API_URL}/admin/subject/${this.id ? this.id : 'new'}`;
        try {
          const response = await axios.post(url, userdata,
              {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem('token')}`
              // Do NOT add "Access-Control-Request-Method" manually
            },
            withCredentials: false, // Ensures credentials (cookies, auth) are included if needed
          });
          console.log('Response:', response.data);
          this.$router.push('/admin');
        } catch (error) {
          console.error('Error:', error);
        }
        
      },
      cancel() {
        this.$router.push('/admin');
      }
    }
}
</script>

<style scoped>
.subject-form {
    padding: 30px;
    max-width: 600px;
    margin: 50px auto;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    background: rgb(37 34 50);
    text-align: center;
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
    color: white;
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
</style>
