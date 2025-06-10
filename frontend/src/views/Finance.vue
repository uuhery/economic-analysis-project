<template>
  <div>
    <h2>💰 Budget & Financial Analysis</h2>

    <!-- NPV -->
    <section>
      <h3>NPV (Net Present Value)</h3>
      <p class="description">Calculate discounted cash flows over time. You may use cost estimation results as the initial investment.</p>

      <label>Cash Flows (comma-separated):</label>
      <input v-model="cashFlowInput" placeholder="-1000,300,400,500" />
      <button @click="fillFromEstimation">📥 Use Estimated Cost as Initial</button>

      <label>Discount Rate (%):</label>
      <input v-model.number="discountRate" type="number" placeholder="e.g. 10" />
      <button @click="calculateNPV">Calculate NPV</button>
      <p v-if="results.npv !== null"><strong>NPV:</strong> {{ results.npv }}</p>
    </section>

    <hr />

    <!-- ROI -->
    <section>
      <h3>ROI (Return on Investment)</h3>
      <p class="description">ROI = Total Gain / Total Cost. You may use cost estimation as the base cost.</p>

      <label>Total Gain:</label>
      <input v-model.number="roiGain" type="number" />
      <label>Total Cost:</label>
      <input v-model.number="roiCost" type="number" />
      <button @click="useEstimationAsCost">📥 Use Estimated Cost</button>
      <button @click="calculateROI">Calculate ROI</button>
      <p v-if="results.roi !== null"><strong>ROI:</strong> {{ results.roi }}%</p>
    </section>

    <hr />

    <!-- IRR -->
    <section>
      <h3>IRR (Internal Rate of Return)</h3>
      <button @click="calculateIRR">Calculate IRR</button>
      <p v-if="results.irr !== null">IRR: {{ results.irr }}%</p>
    </section>

    <hr />

    <!-- Payback Period -->
    <section>
      <h3>Payback Period</h3>
      <button @click="calculatePayback">Calculate Payback Period</button>
      <p v-if="results.payback !== null">Payback Period: {{ results.payback }} years</p>
      <p v-if="results.payback === null">Investment never recovered</p>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FinanceView',
  data() {
    return {
      cashFlowInput: '-1000,300,400,500',
      estimatedCostFromPrevious: parseFloat(localStorage.getItem("estimated_cost") || "1000"),
      discountRate: 10,
      roiGain: 1500,
      roiCost: 1000,
      results: {
        npv: null,
        roi: null,
        irr: null,
        payback: null
      }
    };
  },
  methods: {
    fillFromEstimation() {
      const flows = this.parseCashFlows();
      if (!isNaN(this.estimatedCostFromPrevious)) {
        flows[0] = -this.estimatedCostFromPrevious; // 替换初始投入
        this.cashFlowInput = flows.join(',');
      }
    },
    parseCashFlows() {
      return this.cashFlowInput.split(',').map(x => parseFloat(x.trim()));
    },
    async calculateNPV() {
      try {
        const res = await axios.post('http://localhost:8000/api/finance/npv', {
          cash_flows: this.parseCashFlows(),
          discount_rate: this.discountRate / 100
        });
        this.results.npv = res.data.npv;
      } catch (err) {
        alert('NPV error: ' + (err.response?.data?.detail || err.message));
      }
    },
    useEstimationAsCost() {
      this.roiCost = this.estimatedCostFromPrevious;
    },
    async calculateROI() {
      try {
        const res = await axios.post('http://localhost:8000/api/finance/roi', {
          gain: this.roiGain,
          cost: this.roiCost
        });
        this.results.roi = res.data.roi_percent;
      } catch (err) {
        alert('ROI error: ' + (err.response?.data?.detail || err.message));
      }
    },
    async calculateIRR() {
      try {
        const res = await axios.post('http://localhost:8000/api/finance/irr', {
          cash_flows: this.parseCashFlows()
        });
        this.results.irr = res.data.irr_percent;
      } catch (err) {
        alert('IRR error: ' + (err.response?.data?.detail || err.message));
      }
    },
    async calculatePayback() {
      try {
        const res = await axios.post('http://localhost:8000/api/finance/payback', {
          cash_flows: this.parseCashFlows()
        });
        this.results.payback = res.data.payback_period;
      } catch (err) {
        alert('Payback error: ' + (err.response?.data?.detail || err.message));
      }
    }
  }
};
</script>

<style scoped>
section {
  margin-bottom: 40px;
}
label {
  display: block;
  margin-top: 10px;
}
input {
  margin-bottom: 10px;
  width: 200px;
}
button {
  margin-top: 10px;
}
</style>
