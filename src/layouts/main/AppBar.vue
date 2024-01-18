<template>
  <v-app-bar :elevation="3" color="primary">
    <v-btn size="large" prepend-icon="mdi-bank" exact @click="goHome" variant="text" :ripple="false" ><v-app-bar-title class="font-weight-bold">BankFinder</v-app-bar-title></v-btn>
    <!-- <v-app-bar-nav-icon icon="mdi-bank"   /> 
    <v-app-bar-title @click="this.$router.push('/')">

        BankFinder
    </v-app-bar-title> -->
    <v-spacer></v-spacer>

    <v-btn prepend-icon="mdi-login" v-if="!this.is_logged" button to="/login">
      Iniciar sesión
    </v-btn>

    <v-btn prepend-icon="mdi-account-plus" v-if="!this.is_logged" button to="/register" >
      Crear cuenta
    </v-btn>
    <!-- <v-btn @click="is_logged=!is_logged">togge</v-btn> -->
    <v-btn prepend-icon="mdi-account" variant="outlined" v-if="this.is_logged" class="mr-3" to="/profile">
      Perfil
    </v-btn>
    <v-btn prepend-icon="mdi-logout" v-if="this.is_logged" variant='outlined' @click="logout()">
      Logout
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      is_logged: true
    }
  },
  methods: {
    goHome(){
      console.log(this.$router.currentRoute)
      if(this.$router.currentRoute == "/") return window.location.reload();
      this.$router.push('/');
    },
    async checkIfLoggedIn() {
      try {
        const response = await this.$axios.get(
          `http://${import.meta.env.VITE_API_URL}/is-auth/`,
        );

        if (response.data.auth) {
          this.is_logged = true
        } else this.is_logged = false
        // localStorage.setItem('token', response.data.token);
      } catch (error) {
        console.error(error);
      }
    },
    async logout() {
      try {
        await this.$axios.get(
          `http://${import.meta.env.VITE_API_URL}/auth/logout/`
        );

        this.$router.push('/')
        window.location.reload();

      } catch (error) {

      }
    }
  },
  mounted() {
    this.checkIfLoggedIn()
  }
}
//
</script>
