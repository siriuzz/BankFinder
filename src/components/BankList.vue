<template>
  <v-sheet>
    <v-list >
      <v-list-item v-for="bank in banks" :key="bank.bank_id" :title="bank.bank_name">
        Website: {{ bank.website }} <br>
        Contacto: {{ bank.contact_number }}

      </v-list-item>
    </v-list>
    
  </v-sheet>
</template>

<script>

export default {
  data() {
    return {
      banks: [],
      apiUrl: import.meta.env.VITE_API_URL,
    };
  },
  mounted() {
    this.fetchBanks();
  },
  methods: {
    async fetchBanks() {
      try {
        const response = await this.$axios.get(`http://${this.apiUrl}/banks/`);
        console.log(response);
        this.banks = response.data;
      } catch (error) {
        console.error('Error fetching banks:', error);
      }
    },
  },
};
</script>