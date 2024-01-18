<template>
  <v-sheet class="">
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

                <v-range-slider v-model="rango_sucursales" density="compact" strict step="1" min="0" max="10" clearable
                  thumb-label></v-range-slider>

                <v-card-text>Abre luego de:</v-card-text>
                <v-text-field v-model="filterParams.opening_hour" variant="solo" density="compact" type="time"
                  clearable></v-text-field>

                <v-card-text>Cierra antes de:</v-card-text>
                <v-text-field v-model="filterParams.closing_hour" variant="solo" density="compact" type="time"
                  clearable></v-text-field>

                <v-card-text>Divisas extranjeras</v-card-text>
                <v-select :items="foreignCurrencies" clearable chips density="compact" v-model="foreignCurrenciesValue"
                  label="Divisas" multiple persistent-hint></v-select>


              </v-form>
              <v-card-text>Bancos por página</v-card-text>

              <v-select :items="itemsPerPage" density="compact" v-model="filterParams.items_per_page"
                @update:menu="fetchBanks">
              </v-select>
            </v-container>
          </v-card>
        </v-col>
        <v-col width="auto">
          <v-row>
            <v-col v-for="bank in banks" :key="bank.bank_id" @mouseleave="overlay[bank.bank_id] = false"
              @mouseover="overlay[bank.bank_id] = true" cols="50" md="3" @click="bankRedirect(bank.bank_id)">
              <v-item-group>
                <v-card class='d-flex flex-column' elevation="5" height="200" link>
                  <v-sheet height="40%" min-height="40%" class="d-flex align-center">
                    <v-img fit :src="'http://localhost:8000' + bank.logo" />
                  </v-sheet>
                  <v-sheet max-heigth="300" height="500" width="auto" class="d-inline-flex">
                    <v-container class="h-auto font-weight-bold text-h6 text-wrap d-inline-block text-start">
                      {{ bank.bank_name }}
                    </v-container>

                  </v-sheet>

                  <v-overlay :id="bank.bank_id" v-model="overlay[bank.bank_id]" contained
                    class="d-flex align-center justify-center">
                    <v-btn color="primary" class="d-flex align-center justify-center"
                      @click="overlay[bank.bank_id] = false">
                      Más información
                    </v-btn>
                  </v-overlay>
                </v-card>
              </v-item-group>
            </v-col>

          </v-row>
        </v-col>
      </v-row>
    </v-responsive>
    <v-pagination :model-value='filterParams.page' v-model="filterParams.page" total-visible="5" @click="fetchBanks"
      :length="numberOfPages"></v-pagination>
  </v-sheet>
</template>

<script>
export default {
  props: ['search', 'loading'],
  data() {
    return {
      apiUrl: import.meta.env.VITE_API_URL,
      banks: [],
      itemsPerPage: [],
      foreignCurrenciesValue: [],
      numberOfPages: 1,
      overlay: [],
      filterParams: {
        bank_name: "",
        page: 1,
        min_sucursales: 0,
        max_sucursales: 10,
        opening_hour: '',
        closing_hour: '',
        currencies: [],
        items_per_page: 3

      },
      rango_sucursales: [0, 10],
      foreignCurrencies: [],

    };
  },
  mounted() {
    this.fetchCurrencies();
    this.fetchFilters();
    this.fetchBanks();
  },
  methods: {
    restartFilters() {
      this.filterParams = {
        bank_name: "",
        page: 1,
        min_sucursales: 0,
        max_sucursales: 10,
        opening_hour: '',
        closing_hour: '',
        currencies: [],
        items_per_page: 3
      },
      window.localStorage.setItem('filters',JSON.stringify(this.filterParams))
      window.location.reload();
    },
    fetchFilters() {
      const filters = window.localStorage.getItem('filters');
      // console.log(JSON.parse(filters))
      if (filters) {
        this.filterParams = JSON.parse(filters)
        this.$emit('sync', this.filterParams.bank_name)
        this.rango_sucursales = [this.filterParams.min_sucursales, this.filterParams.max_sucursales]
        if (this.filterParams.currencies != "") this.foreignCurrenciesValue = this.filterParams.currencies.split(',')
      }
    },
    async fetchBanks() {
      try {
        if (this.search || this.filterParams) {
          this.filterParams.currencies = this.foreignCurrenciesValue.join(',')
          this.filterParams.min_sucursales = this.rango_sucursales[0];
          this.filterParams.max_sucursales = this.rango_sucursales[1];
          this.filterParams.bank_name = this.search

          const filtertedEntries = Object.entries(this.filterParams).filter(([key, value]) => value !== "");
          const response = await this.$axios.get(`http://${this.apiUrl}/banks/filter/`, {
            params:
              this.filterParams

          }).then(res => {

            this.$router.push({ path: "/", query: Object.fromEntries(filtertedEntries) })
            // this.banks = response.data;
            this.banks = res.data.result;
            this.itemsPerPage = []
            for (var i = 0; i < res.data.branches_count_result.length; i++) {
              if(i < 12) this.itemsPerPage.push(i + 1);
              else break;
            }
            this.numberOfPages = res.data.total_pages;
            window.localStorage.setItem('filters', JSON.stringify(this.filterParams));

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
    fetchCurrencies() {
      this.$axios.get(`http://${this.apiUrl}/currency`).then(res => {
        this.foreignCurrencies = res.data.map(currency => currency.currency_code)
        // console.log(this.foreignCurrencies)
      })
    }
  },
};
</script>