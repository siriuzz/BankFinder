<template>
  <v-container fluid>
    <v-col style="justify-content: center;">
      <v-row>
        <v-sheet justify="center">
          <h1>Bienvenido a BankFinder</h1>
        </v-sheet>
      </v-row>
      <v-row style="height: 30rem;">
        <v-sheet color="grey-lighten-5" width="100%"  justify-content="center"  clearable>
          <v-text-field clearable  @click:append-inner="runFetchBanks"  v-model="search" width="40%" label="Inserta el nombre de algun banco" variant="outlined" append-inner-icon="mdi-magnify" :loading="loading"></v-text-field>
          <BankList :search="search" ref="fetchBanksRef"/>

        </v-sheet>
        <v-sheet>
        </v-sheet>
      </v-row>
    </v-col>

  </v-container>
</template>

<script >
import BankList from '@/components/BankList.vue'
export default {
  data(){
    return{
      search:'',
      loading:false
    }
  },
  components: {
    BankList,
  },
  methods:{
    runFetchBanks(){
      this.$refs.fetchBanksRef.fetchBanks();
    }
  }
}
</script>
