<template>
  <div class="d-flex align-center justify-center" style="height: 100vh">
    <v-sheet width="400" class="mx-auto">
      <v-card-title class="text-center text-h4 mb-5">Iniciar sesión</v-card-title>
      <v-form ref="loginForm" @submit.prevent="login" validate-on=" input submit lazy" v-model="valid" :disabled="loading">
        <v-text-field v-model="username" label="Nombre de Usuario" :rules="usernameRules" required></v-text-field>
        <v-text-field v-model="password" label="Contraseña" type="password" :rules="passwordRules"
          required></v-text-field>
        <v-btn :loading="loading" type="submit" color="primary" block class="mt-2">Iniciar Sesión</v-btn>
      </v-form>
    </v-sheet>
  </div>
</template>
 
<script>

export default {
  data() {
    return {
      valid: false,
      loading: false,
      loginFlag: false,
      username: '',
      password: '',
      apiUrl: import.meta.env.VITE_API_URL,
      csrfToken: '',
      incorrectCredentials: "",
      usernameRules: [
        value => {
          if (value) return true

          return 'Username is required.'
        },
        () => {
          if (this.incorrectCredentials != undefined && this.incorrectCredentials != '')
            return this.incorrectCredentials
        }
      ],
      passwordRules: [
        value => {
          if (value) return true
          return 'Password is required.'
        },
        () => {
          if (this.incorrectCredentials != undefined && this.incorrectCredentials != '')
            return this.incorrectCredentials
        }
      ]

    };
  },
  methods: {
    // async fetchCsrfToken() {
    //   try {
    //     const response = await this.$axios.get(`http://${this.apiUrl}/get_csrf_token/`);
    //     this.csrfToken = response.data.csrf_token;

    //     // Now you can use the CSRF token in your component
    //     console.log('CSRF Token:', this.csrfToken);
    //   } catch (error) {
    //     console.error('Error fetching CSRF token:', error);
    //   }
    // },

    async login() {
      // console.log(localStorage.getItem('csrftoken'))
      this.loading=true;
      if(this.loginFlag) this.valid = true;
      if (this.valid) {
        try {
          const response = await this.$axios.post(
            `http://${this.apiUrl}/auth/login`,
            {
              username: this.username,
              password: this.password
            },
            // {
            //     headers: {

            //       'Content-Type': 'application/json',
            //       'X-CSRFToken': this.csrfToken, // Include CSRF token in the headers
            //     },
            // }
          );
          if (response.status == 200) {
            // localStorage.setItem('token', response.data.token);
            // console.log('new token', response.data.csrftoken)
            this.$router.push('/');

          }
        } catch (error) {
          this.$refs.loginForm.resetValidation();
          console.error(error.response.data.result);
          this.incorrectCredentials = error.response.data.result
          this.$refs.loginForm.validate();
          this.loginFlag = true;
        }
      }

      this.loading=false;

    }


  }
};
</script>
 