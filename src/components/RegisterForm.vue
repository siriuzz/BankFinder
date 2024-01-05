<template>
  <div class="d-flex align-center justify-center" style="height: 100vh">
    <v-sheet width="400" class="mx-auto">
      <v-card-title>Registrarse</v-card-title>
      <v-form ref="registerForm" :disabled="loading" @submit.prevent="register" validate-on="input lazy" v-model="valid">
        <v-text-field v-model="first_name" :rules='requiredRules' label="Nombre"></v-text-field>
        <v-text-field v-model="last_name" :rules='requiredRules' label="Apellido"></v-text-field>
        <v-text-field v-model="username" :rules='usernameRules' label="Nombre de Usuario"></v-text-field>
        <!-- <v-text-field v-model="email" :rules="emailRules" label="Correo electrónico"></v-text-field> -->

        <v-text-field v-model="password" :rules="passwordRules" label="Contraseña" type="password"></v-text-field>
        <v-text-field v-model="repeatPassword" :rules="repeatPasswordRules" label="Repetir contraseña"
          type="password"></v-text-field>

        <v-btn type="submit" color="primary" block class="mt-2" :loading="loading">Registrarse</v-btn>
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
      username: '',
      first_name: '',
      last_name: '',
      // email: '',
      password: '',
      repeatPassword: '',
      apiUrl: import.meta.env.VITE_API_URL,
      csrfToken: '',
      requiredRules: [
        value => {
          if (value) return true
          return 'Este campo es obligatorio.'
        },
      ],
      usernameRules: [
        value => {
          if (value) return true
          return 'Este campo es obligatorio.'
        },
        value => {
          if (value.length >= 3) return true
          return 'El nombre de usuario debe tener al menos 3 caracteres'
        }
      ],
      // emailRules: [
      //   value => {
      //     if (value) return true
      //     return 'Este campo es obligatorio'
      //   },
      //   value => {
      //     if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
      //     return 'Correo electrónico inválido'
      //   }
      // ],

      passwordRules: [
        value => {
          if (value) return true
          return 'Este campo es obligatorio.'
        },
        value => {
          if (value.length >= 8) return true
          return 'La contraseña debe contener al menos 8 caracteres'
        },
        value => {
          let hasNumber = false;
          let hasLetter = false;
          let hasSpecialChar = false;

          for (const char of value) {
            if (!isNaN(char)) {
              hasNumber = true;
            } else if (char.match(/[a-zA-Z]/)) {
              hasLetter = true;
            } else if (char.match(/[!@#$%^&*(),.?":{}|<>]/)) {
              hasSpecialChar = true;
            }

            if (hasNumber && hasLetter && hasSpecialChar) {
              return true;
            }
          }

          return 'La contraseña debe contener al menos un número, una letra y un simbolo';
        }
      ],
      repeatPasswordRules: [
        value => {
          if (value) return true
          return 'Este campo es obligatorio.'
        },
        value => {
          if (value === this.password) return true
          return 'Las contraseñas no coinciden'
        }
      ]

    };
  },
  mounted() {
    // this.fetchCsrfToken();
  },
  methods: {
    async register() {
      this.loading = true

      if (this.valid) {
        try {
          const response = await this.$axios.post(
            `http://${this.apiUrl}/auth/register`,
            {
              first_name:this.first_name,
              last_name:this.last_name,
              username: this.username,
              password: this.password,
            },
          );
          // localStorage.setItem('token', response.data.token);
          if (response.status == 200) {
            this.$router.push('/');
          }
        } catch (error) {
          console.error(error);
        }
      }
      this.loading = false

    }


  }
};
</script>
   