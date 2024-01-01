<template>
  <div class="d-flex align-center justify-center" style="height: 100vh">
    <v-sheet width="400" class="mx-auto">
      <v-card-title>Iniciar sesión</v-card-title>
      <v-form fast-fail @submit.prevent="login">
        <v-text-field v-model="username" label="Nombre de Usuario"></v-text-field>
        <v-text-field v-model="password" label="Contraseña" type="password"></v-text-field>
        <v-btn type="submit" color="primary" block class="mt-2">Iniciar Sesión</v-btn>
      </v-form>
    </v-sheet>
  </div>
</template>
 
<script>

export default {
  data() {
    return {
      username: '',
      password: '',
      apiUrl: import.meta.env.VITE_API_URL,
      csrfToken: '',

    };
  },
  mounted() {
    this.fetchCsrfToken();
  },
  methods: {
    async fetchCsrfToken() {
      try {
        const response = await this.$axios.get(`http://${this.apiUrl}/get_csrf_token/`);
        this.csrfToken = response.data.csrf_token;

        // Now you can use the CSRF token in your component
        console.log('CSRF Token:', this.csrfToken);
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    },
    async login() {
      // console.log(localStorage.getItem('csrftoken'))
      try {
        const response = await this.$axios.post(
          `http://${this.apiUrl}/auth/login`,
          {
            username: this.username,
            password: this.password
          },
          {
              headers: {
  
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken, // Include CSRF token in the headers
              },
          }
        );
        if (response.status = 200) {
          // localStorage.setItem('token', response.data.token);
          console.log('new token', response.data.csrftoken)
          this.$router.push('/');

        }
      } catch (error) {
        console.error(error);
      }
    }


  }
};
</script>
 