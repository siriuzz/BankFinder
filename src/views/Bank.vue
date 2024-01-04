<template>
  <v-container fluid>
    <v-col style="justify-content: center;">
      <v-row>
        <v-card elevation="5" width="100%" justify="center">
          <v-sheet >

            <v-img cover width="500" :src="'http://localhost:8000'+info.logo"></v-img>
          </v-sheet>
          <v-card-title>{{ info.bank_name }}</v-card-title>
          <v-card-subtitle > {{ info.website }}</v-card-subtitle>
          <v-card-subtitle > {{ info.contact_number }}</v-card-subtitle>
          <v-sheet>
            <v-list>
              <v-list-item v-for="branch in info.branches">
                <v-list-item-title>{{ branch.branch_name }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-sheet>

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