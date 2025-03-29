<template>
  <div class="chapter-form-container">
    <h2>{{ isEditing ? 'Edit Chapter' : 'Create New Chapter' }}</h2>

    <div class="form-container">
      <form @submit.prevent="saveChapter">
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="chapter.title" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="chapter.description" class="form-control" rows="3"></textarea>
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
  name: 'ChapterForm',
  props: {
    id: {
      type: [String, Number],
      required: false
    },
    subject_id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      chapter: {
        title: '',
        description: '',
        keywords: []
      },
      isEditing: false,
      keywordsInput: ''
    };
  },
  created() {
    if (this.id) {
      this.isEditing = true;
      this.fetchChapter();
    }
  },
  computed: {
    formattedKeywords() {
      return this.chapter.keywords.join(', ');
    }
  },
  watch: {
    keywordsInput(val) {
      this.chapter.keywords = val.split(',').map(keyword => keyword.trim()).filter(keyword => keyword);
    }
  },
  methods: {
    async fetchChapter() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/chapters/${this.id}`,{
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      });
        this.chapter = response.data;
      } catch (error) {
        console.error('Error fetching chapter:', error);
      }
    },
    async saveChapter() {
      const chapterData = {
        title: this.chapter.title,
        description: this.chapter.description
      };

      const url = this.isEditing
        ? `${process.env.VUE_APP_API_URL}/admin/chapters/${this.id}`
        : `${process.env.VUE_APP_API_URL}/admin/subject/${this.subject_id}/chapters`;

      try {
        const response = await axios({
          method: this.isEditing ? 'put' : 'post',
          url,
          data: chapterData,
          
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        
      }});
        
        console.log('Chapter saved:', response.data);
        this.$router.push('/admin');
      } catch (error) {
        console.error('Error saving chapter:', error);
      }
      },
      cancel() {
        this.$router.push('/admin');
      }
      }
};
</script>

<style scoped>
.chapter-form-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: rgb(37 34 50);
}

h2 {
  color: white;
  margin-bottom: 20px;
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
  gap: 10px;
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
