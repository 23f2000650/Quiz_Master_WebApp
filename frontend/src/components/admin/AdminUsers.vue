<template>
  <div class="admin-users container">
    <NavAdmin />
    <h1>Active Users Management</h1>

    <!-- Search Bar -->
    <div class="search-container">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search users by name or email..." 
        class="search-input"
      />
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-spinner">
      <p>Loading users...</p>
    </div>

    <!-- Users List -->
    <div v-else-if="filteredUsers.length" class="users-grid">
      <div v-for="user in filteredUsers" :key="user.id" class="user-card">
        <div class="user-info">
          <h3>{{ user.name }}</h3>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>DOB:</strong> {{ formatDate(user.dob) }}</p>
          <p><strong>Qualification:</strong> {{ user.qualification }}</p>
        </div>

        <div class="user-actions">
          <button 
            @click="downloadUserData(user.id)" 
            class="btn-download"
            :disabled="downloading[user.id]"
          >
            {{ downloading[user.id] ? 'Downloading...' : 'Download CSV' }}
          </button>

          <button 
            @click="confirmDeleteUser(user.id)" 
            class="btn-delete"
          >
            Delete User
          </button>
        </div>
      </div>
    </div>

    <!-- No Users Found -->
    <p v-else class="no-users">No users match your search.</p>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import NavAdmin from './NavAdmin.vue';

export default {
  name: 'AdminUsers',
  components: { NavAdmin },
  setup() {
    const users = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const downloading = ref({});
    const searchQuery = ref('');

    // Format Date
    const formatDate = (dateString) => {
      if (!dateString) return 'Not available';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    // Fetch Users
    const fetchUsers = async () => {
      try {
        loading.value = true;
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/users`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          }
        });
        users.value = response.data;
        loading.value = false;
      } catch (err) {
        error.value = 'Failed to fetch users. Please try again.';
        loading.value = false;
        console.error('Error fetching users:', err);
      }
    };

    // Filter Users Based on Search Query
    const filteredUsers = computed(() => {
      return users.value.filter(user =>
        user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    // Download User Data
    const downloadUserData = async (userId) => {
      try {
        downloading.value[userId] = true;

        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/download_csv/${userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          responseType: 'blob'
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `user_${userId}_data.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        error.value = 'Failed to download user data. Please try again.';
        console.error('Error downloading user data:', err);
      } finally {
        downloading.value[userId] = false;
      }
    };

    // Delete User
    const confirmDeleteUser = async (userId) => {
      if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        try {
          await axios.delete(`${process.env.VUE_APP_API_URL}/admin/users/${userId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            }
          });

          // Remove deleted user from the list
          users.value = users.value.filter(user => user.id !== userId);
        } catch (err) {
          error.value = 'Failed to delete user. Please try again.';
          console.error('Error deleting user:', err);
        }
      }
    };

    // Fetch users when the component is mounted
    onMounted(fetchUsers);

    return {
      users,
      loading,
      error,
      downloading,
      searchQuery,
      filteredUsers,
      formatDate,
      downloadUserData,
      confirmDeleteUser
    };
  }
};
</script>

<style scoped>
.admin-users {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #4a90e2;
  margin-bottom: 30px;
  font-size: 28px;
}

/* Search Bar */
.search-container {
  margin-bottom: 20px;
  text-align: center;
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #4a90e2;
  border-radius: 5px;
  background-color: #25233a;
  color: white;
}

/* User Grid */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

/* User Card */
.user-card {
  background: #25233a;
  border: 2px solid #4a90e2;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* User Info */
.user-info h3 {
  color: #4a90e2;
  margin-top: 0;
  margin-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 10px;
}

.user-info p {
  color: #e2e2e2;
  margin: 10px 0;
}

/* Actions */
.user-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn-download, .btn-delete {
  flex-grow: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.btn-download {
  background: #4CAF50;
  color: white;
}

.btn-download:hover {
  background: #45a049;
}

.btn-download:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.btn-delete {
  background: #e25353;
  color: white;
}

.btn-delete:hover {
  background: #d23939;
}

/* Loading & Error */
.loading-spinner, .no-users, .error-message {
  text-align: center;
  color: #4a90e2;
  margin-top: 50px;
}

.error-message {
  color: #e25353;
}
</style>
