<template>
  <v-sheet class="pb-10">
    <!-- <v-sheet disabled v-on:change="fetchBanks()"> {{ search }} </v-sheet> -->
    <v-responsive>

      <v-row class="pa-2" height="200">
        <v-col cols="12" md="2">
          <v-card class="">
            <v-container>
              <v-form @submit.prevent>
                <v-btn class="mb-2 bg-light-blue-5" @click="fetchBanks">Aplicar filtros</v-btn>
                <v-btn class="mb-2 bg-light-blue-5" @click="restartFilters">Reiniciar filtros</v-btn>

                <v-card-text>Cantidad de sucursales</v-card-text>
                
                <v-range-slider v-model="rango_sucursales" density="compact" strict step="1" min="0" max="10"  thumb-label></v-range-slider>
  
                <v-card-text>Hora de apertura</v-card-text>
                <v-text-field v-model="filterParams.opening_hour" variant="solo" density="compact" type="time"
                  clearable></v-text-field>
  
                <v-card-text>Hora de cierre</v-card-text>
                <v-text-field v-model="filterParams.closing_hour" variant="solo" density="compact"
                  type="time"></v-text-field>
  
                <v-card-text>Divisas extranjeras</v-card-text>
                <v-select :items="foreignCurrencies" item-title="name" item-value="value" clearable chips
                  density="compact" v-model="foreignCurrenciesValue" label="Divisas" multiple persistent-hint></v-select>
  
  
              </v-form>
              <v-card-text>Bancos por página</v-card-text>

              <v-select :items="itemsPerPage" density="compact" v-model="filterParams.items_per_page" @select ="fetchBanks">
              </v-select>
            </v-container>
          </v-card>
        </v-col>
        <v-col width="auto">
          <v-row>
            <v-col v-for="bank in banks" :key="bank.bank_id" cols="50" md="3" @click="bankRedirect(bank.bank_id)">
              <v-item-group>
                <v-card class='d-flex flex-column pa-5' elevation="5" height="220" link>
                  
                  <v-sheet height="40%" class="d-flex align-center">
                    <v-img fit :src="'http://localhost:8000' + bank.logo" />
                    
                  </v-sheet>
                  <v-card-title>
                    {{ bank.bank_name }}
                  </v-card-title>
                  Website: {{ bank.website }} <br>
                  Contacto: {{ bank.contact_number }}
                </v-card>
  
              </v-item-group>
            </v-col>
  
          </v-row>
        </v-col>
      </v-row>
    </v-responsive>
    <v-pagination model-value="1" v-model="filterParams.page" @click="fetchBanks" :length="numberOfPages"></v-pagination>
    </v-sheet>
</template>

<script>
import router from '@/router';


export default {
  props: ['search', 'loading'],
  data() {
    return {
      apiUrl: import.meta.env.VITE_API_URL,
      banks: [],
      itemsPerPage:[],
      rango_sucursales: [0,10],
      foreignCurrenciesValue:[],
      numberOfPages:1,
      filterParams: {
        bank_name: "",
        page: 1,
        min_sucursales:0,
        max_sucursales:0,
        opening_hour: '',
        closing_hour: '',
        currencies: [],
        items_per_page:3

      },
      foreignCurrencies: [],

    };
  },
  mounted() {
    this.fetchBanks();
    this.fetchCurrencies()
  },
  methods: {
    restartFilters(){
      window.location.reload();
    },  
    async fetchBanks() {
      try {
        if (this.search || this.filterParams) {
          this.filterParams.currencies = this.foreignCurrenciesValue.join(',')
          this.filterParams.min_sucursales = this.rango_sucursales[0];
          this.filterParams.max_sucursales = this.rango_sucursales[1];
          this.filterParams.bank_name = this.search

          const filtertedEntries = Object.entries(this.filterParams).filter(([key,value]) => value !== "");
          const response = await this.$axios.get(`http://${this.apiUrl}/banks/filter/`, {
            params:
              this.filterParams

          }).then(res => {

            this.$router.push({ path: "/", query: Object.fromEntries(filtertedEntries) })
            // this.banks = response.data;
            this.banks = res.data.result;
            this.itemsPerPage=[]
            for(var i = 0; i < res.data.branches_count_result.length; i++){
              this.itemsPerPage.push(i+1);
            }
            this.numberOfPages = res.data.total_pages;

            console.log(res)
          }).catch(err => {
            console.log(err);
          });

        } else {
          this.$router.push("/")
          const response = await this.$axios.get(`http://${this.apiUrl}/banks`);
          this.banks = response.data
          console.log(response);
          
        }
      } catch (error) {
        console.error('Error fetching banks:', error);
      }
    },
    bankRedirect(id) {
      return this.$router.push(`/bank?id=${id}`)
    },
    fetchCurrencies(){
      this.$axios.get(`http://${this.apiUrl}/currency`).then(res=>{
        this.foreignCurrencies = res.data.map(currency=>currency.currency_code)
        // console.log(this.foreignCurrencies)
      })
    }
  },
};
</script>