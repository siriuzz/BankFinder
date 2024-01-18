<template>
  <v-container fluid >
    <v-col style="justify-content: center;">
      <v-row class="d-flex flex-column justify-center">
        <v-sheet class="d-flex text-center">
          <v-container class="text-h3 font-weight-bold">Bienvenido a BankFinder!</v-container>
        </v-sheet>
      </v-row>
      <v-row class="d-flex justify-center">
        <v-sheet color="secondary" rounded width="75%" justify-content="center" clearable>
          <v-container class=" justify-center w-100">

            <v-text-field  clearable hide-details @click:prepend-inner="runFetchBanks" @input="runFetchBanks"  v-model="search"  label="Inserta el nombre de algun banco" variant="outlined" prepend-inner-icon="mdi-magnify" :loading="loading"></v-text-field>
          </v-container>
          
        </v-sheet>
        <v-sheet width="100%">

          <BankList :search="search" @sync="updateSearch" ref="fetchBanksRef"/>
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
    updateSearch(value){
      this.search=value
    },
    runFetchBanks(){
      this.$refs.fetchBanksRef.fetchBanks();
    }
  }
}
</script>
