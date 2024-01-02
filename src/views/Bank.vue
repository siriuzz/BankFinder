<template>
    <v-container fluid>
      <v-col style="justify-content: center;" >
        <v-row>
          <v-sheet justify="center">
            <h1>{{ this.info }}</h1>
          </v-sheet>
        </v-row>
       
        
       
        
      </v-col>
  
    </v-container>
  </template>
  
  <script>
  export default {
    data(){
        return {
            requestBankId:this.$route.query.id,
            info:{}
        }
    },
    mounted(){
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