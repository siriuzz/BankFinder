<template>
  <v-container>
    <v-col justify-content='center'>
      <v-row>
        <v-card elevation="5" width="100%">
          <v-sheet class="d-flex bg-secondary align-center">
            <v-card elevation="0" class="ma-3" outlined>

              <v-img wrap width="500" :src="'http://localhost:8000' + info.logo"></v-img>
            </v-card>
            <v-card-title class="text-h4 ">{{ info.bank_name }}</v-card-title>
          </v-sheet>
          <v-sheet class="justify-center d-flex">
            <v-sheet rounded="8"
              class="bg-secondary text-center rounded-pill d-flex justify-center justify-space-around  pa-5 mt-5 text"
              width="90%">
              <v-sheet class="bg-transparent">

                <p class="text-subtitle font-weight-bold">Página web:</p>
                <p> {{ info.website }}</p>
              </v-sheet>
              <v-sheet class="bg-transparent" v-if="currenciesExist">

                <p class="text-subtitle font-weight-bold">Divisas:</p>
                <p>
                  <v-chip v-for="currency_exchange in info.currency_exchanges">
                   {{ currency_exchange.currency.currency_code }}
                  </v-chip>

                </p>
              </v-sheet>
              <v-sheet class="bg-transparent">

                <p class="text-subtitle font-weight-bold">Número principal:</p>
                <p> {{ info.contact_number }}</p>
              </v-sheet>
            </v-sheet>

          </v-sheet>
          <v-sheet class="d-flex flex-column justify-space-between pa-5 ">

            <v-sheet>
              <calculator :exchanges="info.currency_exchanges" @click="showDialog = !showDialog" :is-enabled="!auth" />
              <login-dialog v-if="!auth" :open-dialog="showDialog" @update:open-dialog="protect" />
            </v-sheet>
          </v-sheet>
          <v-sheet class="d-flex">
            <branch-display v-if="showBranches" :branches="info.branches" />
          </v-sheet>

        </v-card>
      </v-row>
    </v-col>

  </v-container>
</template>
  
<script>
import Calculator from "../components/Calculator.vue";
import BranchDisplay from "../components/BranchDisplay.vue";
import LoginDialog from "../components/LoginDialog.vue"

export default {
  components: {
    Calculator,
    BranchDisplay,
    LoginDialog
  },
  data() {
    return {
      requestBankId: this.$route.query.id,
      info: {},
      showBranches: false,
      auth: false,
      showDialog: false,
      currenciesExist: false
    }
  },
  methods: {
    protect() {
      // console.log(this.showDialog)
      if (!this.auth) this.showDialog = !this.showDialog
    }
  },
  mounted() {
    this.$axios.get(`http://${import.meta.env.VITE_API_URL}/banks/${this.requestBankId}`)
      .then(res => {
        this.info = res.data
        if (this.info.branches.length > 0) {
          this.showBranches = true
        }
        if(this.info.currency_exchanges.length > 0) this.currenciesExist = true;
        // console.log(res)
      })
      .catch(err => {
        console.error(err);
      });
    this.$axios.get(`http://${import.meta.env.VITE_API_URL}/is-auth`).then(res => {
      // console.log(res)
      this.auth = res.data.auth
      // console.log(this.auth)
    })


  },
}
</script>