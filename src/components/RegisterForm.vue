<template>
    <div class="d-flex align-center justify-center" style="height: 100vh">
      <v-sheet width="400" class="mx-auto">
        <v-card-title>Registrarse</v-card-title>
        <v-form fast-fail @submit.prevent="register">
          <v-text-field v-model="username" label="Nombre de Usuario"></v-text-field>
          <v-text-field v-model="email" label="Correo electrónico"></v-text-field>

          <v-text-field v-model="password" label="Contraseña" type="password"></v-text-field>
          <v-text-field v-model="repeatPassword" label="Repetir contraseña" type="password"></v-text-field>

          <v-btn type="submit" color="primary" block class="mt-2">Registrarse</v-btn>
        </v-form>
      </v-sheet>
    </div>
  </template>
   
  <script>
  export default {
    data() {
      return {
        username: '',
        email:'',
        password: '',
        repeatPassword: '',
        apiUrl: import.meta.env.VITE_API_URL,
        csrfToken: ''
  
      };
    },
    mounted() {
      // this.fetchCsrfToken();
    },
    methods: {
      
      async register() {
        try {
          
          const response = await this.$axios.post(
            `http://${this.apiUrl}/auth/register`,
            {
              username: this.username,
              password: this.password,
              email: this.email
            },
          );
          // localStorage.setItem('token', response.data.token);
          if(response.status == 200){
            this.$router.push('/login');
          }
        } catch (error) {
          console.error(error);
        }
      }
  
  
    }
  };
  </script>
   