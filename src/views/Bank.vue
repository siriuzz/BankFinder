<template>
  <v-container fluid>
    <v-col style="justify-content: center;">
      <v-row>
        <v-card elevation="5" width="100%" justify="center">
          <v-sheet >

            <v-img cover width="500" :src="'http://localhost:8000'+info.logo"></v-img>
          </v-sheet>
          <v-card-title class="text-h4">{{ info.bank_name }}</v-card-title>
          <v-card-text class="text-h6 pb-0 pt-5">Página web: {{ info.website }}</v-card-text>
          <v-card-text class="text-h6">Número principal: {{ info.contact_number }}</v-card-text>
          <branch-display :branches="info.branches"/>
          <calculator :exchanges="info.currency_exchanges"/>

        </v-card>
      </v-row>
    </v-col>

  </v-container>
</template>
  
<script>
import Calculator from "../components/Calculator.vue";
import BranchDisplay from "../components/BranchDisplay.vue";

export default {
  components:{
    Calculator,
    BranchDisplay
  },
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