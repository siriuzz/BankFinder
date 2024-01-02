<template>
  <v-sheet>
    <!-- <v-sheet disabled v-on:change="fetchBanks()"> {{ search }} </v-sheet> -->
    <v-item-group selected-class="bg-primary">
      <v-row>
        <v-col v-for="bank in banks" :key="bank.bank_id" cols="12" md="3" @click="bankRedirect(bank.bank_id)">
          <v-list-item elevation="5" rounded>
            <v-card :class="['d-flex flex-column align-center']"  link>
              <v-img cover width="300" src="src\assets\test.jpg"  />
              <v-card-title>
                {{ bank.bank_name }}
              </v-card-title>
                Website: {{ bank.website }} <br>
                Contacto: {{ bank.contact_number }}
            </v-card>

          </v-list-item>
        </v-col>

      </v-row>
    </v-item-group>

  </v-sheet>
</template>

<script>

export default {
  props:['search','loading'],
  data() {
    return {
      apiUrl: import.meta.env.VITE_API_URL,
      banks:[]
    };
  },
  mounted() {
    this.fetchBanks();
  },
  methods: {
    async fetchBanks() {
      try {
        if(this.search){
          const response = await this.$axios.get(`http://${this.apiUrl}/banks/${this.search}`);
          this.banks = response.data.result;
          console.log(response);

        } else {
          const response = await this.$axios.get(`http://${this.apiUrl}/banks`);
          this.banks = response.data;
          console.log(response);
        }
      } catch (error) {
        console.error('Error fetching banks:', error);
      }
    },
    bankRedirect(id){
      return this.$router.push(`/bank?id=${id}`)
    }
  },
};
</script>