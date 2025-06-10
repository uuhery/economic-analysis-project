<template>
  <div>
    <h2>NPV Calculator</h2>
    <div>
      <label>Cash Flows (comma-separated):</label>
      <input v-model="cashFlowInput" placeholder="-1000,300,400,500" />
    </div>
    <div>
      <label>Discount Rate (%):</label>
      <input v-model="rateInput" type="number" />
    </div>
    <button @click="calculate">Calculate</button>
    <p v-if="result !== null">NPV: {{ result }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NPVView',
  data() {
    return {
      cashFlowInput: '',
      rateInput: 10,
      result: null
    }
  },
  methods: {
    async calculate() {
      const flows = this.cashFlowInput.split(',').map(x => parseFloat(x.trim()));
      const rate = parseFloat(this.rateInput) / 100;

      try {
        const res = await axios.post('http://localhost:8000/api/finance/npv', {
          cash_flows: flows,
          discount_rate: rate
        });
        this.result = res.data.npv;
      } catch (err) {
        alert("Error: " + (err.response?.data?.error || err.message));
      }
    }
  }
}
</script>
