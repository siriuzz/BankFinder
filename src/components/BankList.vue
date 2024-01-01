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
      console.log(this.$cookies.get('csrftoken'));
      try {
        const response = await this.$axios.get(`http://${this.apiUrl}/banks/`, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.$cookies.get('csrftoken'), // Include CSRF token in the headers
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