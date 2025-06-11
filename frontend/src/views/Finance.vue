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

    <!-- IRR -->
    <section>
      <h3>IRR (Internal Rate of Return)</h3>
      <button @click="calculateIRR">Calculate IRR</button>
      <p v-if="results.irr !== null">IRR: {{ results.irr }}%</p>
    </section>

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
        const res = await axios.post('/api/finance/npv', {
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
        const res = await axios.post('/api/finance/roi', {
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
        const res = await axios.post('/api/finance/irr', {
          cash_flows: this.parseCashFlows()
        });
        this.results.irr = res.data.irr_percent;
      } catch (err) {
        alert('IRR error: ' + (err.response?.data?.detail || err.message));
      }
    },
    async calculatePayback() {
      try {
        const res = await axios.post('/api/finance/payback', {
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
  padding: 20px;
  background-color: #f9fcff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
  border: 1px solid #d6e9ff;
}

/* 标题风格统一 */
h2, h3 {
  color: #007BFF;
  margin-bottom: 16px;
  font-weight: 600;
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

/* 标签和描述 */
label {
  display: block;
  margin-top: 10px;
  font-weight: 500;
  color: #333;
}

.description {
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

/* 输入框美化 */
input {
  width: 260px;
  padding: 6px 12px;
  margin-top: 4px;
  margin-bottom: 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  transition: border-color 0.2s ease;
}
input:focus {
  border-color: #007BFF;
  outline: none;
}

/* 按钮统一蓝色圆角样式 */
button {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  margin-right: 10px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #0056b3;
}

/* 输出结果样式 */
p {
  font-size: 15px;
  margin-top: 6px;
}

strong {
  color: #0056b3;
}

</style>
