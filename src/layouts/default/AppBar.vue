<template>
  <v-app-bar :elevation="3">
    <v-app-bar-title>
      <v-icon icon="mdi-bank" />

      BankFinder
    </v-app-bar-title>
    <v-spacer></v-spacer>

    <v-btn button to="/login">
      Log in
    </v-btn>

    <v-btn button to="/register">
      Register
    </v-btn>

    <v-btn icon>
      <v-icon>mdi-dots-vertical</v-icon>
    </v-btn>
    <!-- <v-btn @click="is_logged=!is_logged">togge</v-btn> -->
    <v-btn v-if="checkIfLoggedIn" @click="logout()">
      Logout
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  data(){
    return {
      is_logged:true
    }
  },
  methods: {
    async checkIfLoggedIn() {
        try {
          const response = await this.$axios.get(
            `http://${import.meta.env.VITE_API_URL}/is-auth/`,
          );

          if(response.data.auth){
            this.is_logged=true
          } else this.is_logged=false
          // localStorage.setItem('token', response.data.token);
        } catch (error) {
          console.error(error);
        }
    },
    async logout(){
      try {
        const response = await this.$axios.get(
            `http://${import.meta.env.VITE_API_URL}/auth/logout/`
          );
          console.log(response);
      } catch (error) {
        
      }
    }
  },
  mounted(){
    this.checkIfLoggedIn()
  }
}
//
</script>
