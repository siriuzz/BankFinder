<template>
    <div>
        <h2>Bank List</h2>
        <ul>
            <li v-for="bank in banks" :key="bank.bank_id">
                {{ bank.bank_name }} - {{ bank.website }}
            </li>
        </ul>
    </div>
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
        const username = "username-django";
        const password = "password-django";
        const response = await this.$axios.get(`http://${this.apiUrl}/banks/`, {
    
          auth: {
            username: username,
            password: password,
          },
          headers: {
            'Accept': 'application/json',
          },
        });
        console.log(response);
        this.banks = response.data.results;
      } catch (error) {
        console.error('Error fetching banks:', error);
      }
    },
  },
};
</script>