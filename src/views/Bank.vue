<template>
  <v-container fluid>
    <v-col style="justify-content: center;">
      <v-row>
        <v-card elevation="5" width="100%" justify="center">
          <v-sheet height="300">

            <v-img cover src="src\assets\test.jpg"></v-img>
          </v-sheet>
          <v-card-title>{{ info.bank_name }}</v-card-title>
          <v-card-subtitle > {{ info.website }}</v-card-subtitle>
          <v-card-subtitle > {{ info.contact_number }}</v-card-subtitle>

        </v-card>
      </v-row>
    </v-col>

  </v-container>
</template>
  
<script>
export default {
  data() {
    return {
      requestBankId: this.$route.query.id,
      info: {}
    }
  },
  mounted() {
    this.$axios.get(`http://${import.meta.env.VITE_API_URL}/banks/${this.requestBankId}`)
      .then(res => {
        this.info = res.data
        console.log(res)
      })
      .catch(err => {
        console.error(err);
      })
  }
}
</script>