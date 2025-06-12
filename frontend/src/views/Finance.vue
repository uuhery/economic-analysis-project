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

    <!-- Budget Tracking -->
    <section>
      <h3>📊 Budget Tracking</h3>
      <p class="description">Enter project phases with their budgeted and actual costs.</p>

      <div v-for="(item, index) in budgetItems" :key="index" style="margin-bottom: 12px;">
        <label>Phase {{ index + 1 }}:</label>
        <input v-model="item.phase" placeholder="e.g. Design Phase" />

        <label>Budgeted:</label>
        <input v-model.number="item.budgeted_amount" type="number" placeholder="e.g. 5000" />

        <label>Actual:</label>
        <input v-model.number="item.actual_amount" type="number" placeholder="e.g. 4800" />
      </div>

      <button @click="addBudgetItem">➕ Add Phase</button>
      <button @click="trackBudget">Track Budget</button>

      <div v-if="trackedBudget.length > 0" style="margin-top: 20px;">
        <h4>Tracked Results</h4>
        <table border="1" cellpadding="8">
          <thead>
            <tr>
              <th>Phase</th>
              <th>Budgeted</th>
              <th>Actual</th>
              <th>Variance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, i) in trackedBudget" :key="i">
              <td>{{ entry.phase }}</td>
              <td>{{ entry.budgeted_amount }}</td>
              <td>{{ entry.actual_amount }}</td>
              <td :style="{ color: entry.difference > 0 ? 'red' : (entry.difference < 0 ? 'green' : 'black') }">
                {{ entry.difference }}
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr style="font-weight: bold;">
              <td>Total</td>
              <td>{{ budgetTotals.budgeted }}</td>
              <td>{{ budgetTotals.actual }}</td>
              <td :style="{ color: budgetTotals.difference > 0 ? 'red' : (budgetTotals.difference < 0 ? 'green' : 'black') }">
                {{ budgetTotals.difference }}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </section>

    <!-- Variance Analysis -->
    <section>
      <h3>📉 Variance Analysis</h3>
      <p class="description">Analyze cost deviations for each project phase.</p>
      <button @click="analyzeVariance">📊 Analyze Variance</button>

      <table v-if="varianceResults.length > 0" border="1" cellpadding="8" style="margin-top: 16px;">
        <thead>
          <tr>
            <th>Phase</th>
            <th>Budgeted</th>
            <th>Actual</th>
            <th>Variance</th>
            <th>% Variance</th>
            <th>Analysis</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, i) in varianceResults" :key="i">
            <td>{{ entry.phase }}</td>
            <td>{{ entry.budgeted_amount }}</td>
            <td>{{ entry.actual_amount }}</td>
            <td>{{ entry.difference }}</td>
            <td>{{ entry.percent_variance }}%</td>
            <td :style="{ color: entry.analysis === 'Overspent' ? 'red' : entry.analysis === 'Underspent' ? 'green' : 'black' }">
              {{ entry.analysis }}
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Forecasting -->
    <section>
      <h3>🔮 Forecasting</h3>
      <p class="description">Predict next phase based on previous budget trends.</p>
      <button @click="forecast">🔁 Run Forecast</button>

      <div v-if="forecastResult" style="margin-top: 20px;">
        <p><strong>Phase:</strong> {{ forecastResult.forecast_phase }}</p>
        <p><strong>Forecasted Budget:</strong> {{ forecastResult.forecast_budgeted }}</p>
        <p><strong>Forecasted Actual:</strong> {{ forecastResult.forecast_actual }}</p>
        <p><strong>Budget Growth Rate:</strong> {{ forecastResult.budget_growth_rate }}%</p>
        <p><strong>Actual Growth Rate:</strong> {{ forecastResult.actual_growth_rate }}%</p>
      </div>
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
      },
      budgetItems: [
        { phase: "Design", budgeted_amount: 5000, actual_amount: 4800 }
      ],
      trackedBudget: [],
      budgetTotals: {
        budgeted: 0,
        actual: 0,
        difference: 0
      },
      varianceResults: [],
      forecastResult: null
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
    },
    addBudgetItem() {
    this.budgetItems.push({ phase: "", budgeted_amount: 0, actual_amount: 0 });
    },
    async trackBudget() {
      try {
        const res = await axios.post('/api/finance/budget-tracking', this.budgetItems);
        this.trackedBudget = res.data.tracked;

        // 汇总计算
        this.budgetTotals = this.trackedBudget.reduce((totals, item) => {
          totals.budgeted += item.budgeted_amount;
          totals.actual += item.actual_amount;
          totals.difference += item.difference;
          return totals;
        }, { budgeted: 0, actual: 0, difference: 0 });
      } catch (err) {
        alert("Budget tracking error: " + (err.response?.data?.detail || err.message));
      }
    },
    async analyzeVariance() {
      try {
        const res = await axios.post('/api/finance/variance-analysis', this.budgetItems);
        this.varianceResults = res.data.analysis;
      } catch (err) {
        alert("Variance analysis error: " + (err.response?.data?.detail || err.message));
      }
    },
    async forecast() {
      try {
        const res = await axios.post('/api/finance/forecast', this.budgetItems);
        this.forecastResult = res.data.forecast;
      } catch (err) {
        alert("Forecasting error: " + (err.response?.data?.detail || err.message));
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
