<template>
  <v-app-bar :elevation="3">
    <v-app-bar-nav-icon icon="mdi-bank" to="/" /> 
    <v-app-bar-title @click="this.$router.push('/')">

        BankFinder
    </v-app-bar-title>
    <v-spacer></v-spacer>

    <v-btn v-if="!this.is_logged" button to="/login">
      Log in
    </v-btn>

    <v-btn v-if="!this.is_logged" button to="/register" >
      Register
    </v-btn>
    <!-- <v-btn @click="is_logged=!is_logged">togge</v-btn> -->
    <v-btn v-if="this.is_logged" to="/profile">
      Perfil
    </v-btn>
    <v-btn v-if="this.is_logged" @click="logout()">
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
