<template>
  <div style="margin: 40px">
    <h2>💰 Budget & Financial Analysis</h2>

    <!-- 结果展示卡片 -->
    <div class="result-cards">
      <div class="card">
        <h4>NPV</h4>
        <p>{{ results.npv !== null ? results.npv : '—' }}</p>
      </div>
      <div class="card">
        <h4>ROI</h4>
        <p>{{ results.roi !== null ? results.roi + '%' : '—' }}</p>
      </div>
      <div class="card">
        <h4>IRR</h4>
        <p>{{ results.irr !== null ? results.irr + '%' : '—' }}</p>
      </div>
      <div class="card">
        <h4>Payback</h4>
        <p>{{ results.payback !== null ? results.payback + ' yrs' : '—' }}</p>
      </div>
    </div>

    <div class="form-row-container">
  <section class="half-section">
    <!-- NPV -->
      <h3>NPV (Net Present Value)</h3>
      <p class="description">Calculate all metrics based on cash flows and estimated cost.</p>

      <label>Cash Flows (comma-separated):</label>
      <input
        v-model="cashFlowInput"
        placeholder="-1000000, 800000, 500000, 900000"
        title="Enter yearly cash flows separated by commas"
      />
      <button @click="fillFromEstimation">📥 Use Estimated Cost as Initial</button>

      <label>Discount Rate (%):</label>
      <input v-model.number="discountRate" type="number" placeholder="e.g. 10" />
      <button @click="calculateAllFinance">📊 Calculate Financial Metrics</button>
    </section>

    <!-- Budget Tracking -->
  <section class="half-section">
      <h3>📊 Budget Tracking</h3>
      <p class="description">Enter project phases with their budgeted and actual costs.</p>


      <div
        v-for="(item, index) in budgetItems"
        :key="index"
        class="budget-input-row"
      >

        <input v-model="item.phase" placeholder="Phase" />
        <input v-model.number="item.budgeted_amount" type="number" placeholder="Budgeted" />
        <input v-model.number="item.actual_amount" type="number" placeholder="Actual" />
      </div>


      <button @click="addBudgetItem">➕ Add Phase</button>
      <button @click="runFullBudgetAnalysis">📊 Run Budget Analysis</button>
      <button @click="fillSamplePhases">📥 Use Sample Phases</button>

    </section>
    </div>

<!-- 📊 图表卡片区：雷达图 + 折线图 + 预测图 -->
<div class="chart-grid">
  <div class="chart-card">
    <h4>🎯 Budget Radar</h4>
    <canvas id="budgetRadarChart" width="400" height="300"></canvas>
  </div>

  <div class="chart-card">
    <h4>📈 Variance Line Chart</h4>
    <canvas id="varianceComboChart" width="400" height="300"></canvas>
  </div>

  <div class="chart-card forecast-card" v-if="forecastResult">
<!--    <h4>🔮 Forecast Result</h4>-->
<!--    <p><strong>📌 Phase:</strong> {{ forecastResult.forecast_phase }}</p>-->

    <div class="forecast-donuts">
      <div>
<!--        <h5>Forecasted Budget</h5>-->
        <canvas id="budgetGrowthChart" width="180" height="180"></canvas>
      </div>
      <div>
<!--        <h5>Forecasted Actual</h5>-->
        <canvas id="actualGrowthChart" width="180" height="180"></canvas>
      </div>
    </div>
  </div>
</div>


    <!-- 📋 表格卡片区：预算跟踪 + 差异分析 -->
    <div class="table-grid">
      <div class="table-card" v-if="trackedBudget.length > 0">
        <h4>📊 Tracked Budget</h4>
        <table class="styled-table">
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
        </table>
      </div>

      <div class="table-card" v-if="varianceResults.length > 0">
        <h4>📉 Variance Analysis</h4>
        <table class="styled-table">
          <thead>
            <tr>
              <th>Phase</th>
              <th>Budgeted</th>
              <th>Actual</th>
              <th>Variance</th>
              <th>%</th>
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
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js'

export default {
  name: 'FinanceView',
  data() {
    return {
      cashFlowInput: '-1000000,800000,500000,900000',
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
        flows[0] = -this.estimatedCostFromPrevious;
        this.cashFlowInput = flows.join(',');
      }
    },
    parseCashFlows() {
      localStorage.setItem('calculated_cash_flows', this.cashFlowInput);
      return this.cashFlowInput.split(',').map(x => parseFloat(x.trim()));
    },
     async calculateAllFinance() {
      const flows = this.parseCashFlows();
      const discount = this.discountRate / 100;

      try {
        const [npvRes, roiRes, irrRes, paybackRes] = await Promise.all([
          axios.post('/api/finance/npv', {
            cash_flows: flows,
            discount_rate: discount
          }),
          axios.post('/api/finance/roi', {
            gain: flows.slice(1).reduce((a, b) => a + b, 0),
            cost: Math.abs(flows[0] || 0)
          }),
          axios.post('/api/finance/irr', { cash_flows: flows }),
          axios.post('/api/finance/payback', { cash_flows: flows })
        ]);

        this.results.npv = npvRes.data.npv;
        this.results.roi = roiRes.data.roi_percent;
        this.results.irr = irrRes.data.irr_percent;
        this.results.payback = paybackRes.data.payback_period;
      } catch (err) {
        alert("Error calculating financial metrics: " + (err.response?.data?.detail || err.message));
      }
    },
    useEstimationAsCost() {
      this.roiCost = this.estimatedCostFromPrevious;
    },
    fillSamplePhases() {
      this.budgetItems = [
        { phase: "Design", budgeted_amount: 5000, actual_amount: 4800 },
        { phase: "Implementation", budgeted_amount: 8000, actual_amount: 8200 },
        { phase: "Testing", budgeted_amount: 3000, actual_amount: 2700 },
        { phase: "Deployment", budgeted_amount: 2000, actual_amount: 2500 },
        { phase: "Maintenance", budgeted_amount: 4000, actual_amount: 3800 }
      ];
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
    async runFullBudgetAnalysis() {
      try {
        const [trackRes, varianceRes, forecastRes] = await Promise.all([
          axios.post('/api/finance/budget-tracking', this.budgetItems),
          axios.post('/api/finance/variance-analysis', this.budgetItems),
          axios.post('/api/finance/forecast', this.budgetItems)
        ]);

        this.trackedBudget = trackRes.data.tracked;
        this.varianceResults = varianceRes.data.analysis;
        this.forecastResult = forecastRes.data.forecast;

        this.budgetTotals = this.trackedBudget.reduce((totals, item) => {
          totals.budgeted += item.budgeted_amount;
          totals.actual += item.actual_amount;
          totals.difference += item.difference;
          return totals;
        }, { budgeted: 0, actual: 0, difference: 0 });

        await this.$nextTick();
        this.renderBudgetRadarChart();
        this.renderVarianceComboChart();
        this.drawForecastCharts();
      } catch (err) {
        alert("Budget analysis error: " + (err.response?.data?.detail || err.message));
      }
    },

    renderBudgetRadarChart() {
  const labels = this.trackedBudget.map(item => item.phase);
  const data = this.trackedBudget.map(item => item.budgeted_amount);

  const ctx = document.getElementById("budgetRadarChart");

  // ✅ 修复：重复调用时销毁旧图表
  if (this._radarChart) {
    this._radarChart.destroy();
  }

  this._radarChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Budget Allocation',
        data: data,
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        pointBackgroundColor: 'rgba(54, 162, 235, 1)'
      }]
    },
    options: {
      responsive: false,
      scales: {
        r: {
          angleLines: { display: true },
          suggestedMin: 0
        }
      }
    }
  });
},

    renderVarianceComboChart() {
  const labels = this.varianceResults.map(item => item.phase);
  const budgeted = this.varianceResults.map(item => item.budgeted_amount);
  const actual = this.varianceResults.map(item => item.actual_amount);
  const difference = this.varianceResults.map(item => item.difference);

  const ctx = document.getElementById("varianceComboChart");
  if (!ctx) return;

  if (this._varianceChart) {
    this._varianceChart.destroy();
  }

  this._varianceChart = new Chart(ctx, {
    type: 'line', // ✅ 只用折线图
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Budgeted',
          data: budgeted,
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: false,
          lineTension: 0.3,
          pointRadius: 4
        },
        {
          label: 'Actual',
          data: actual,
          borderColor: 'rgba(255, 159, 64, 1)',
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          fill: false,
          lineTension: 0.3,
          pointRadius: 4
        },
        {
          label: 'Variance',
          data: difference,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          fill: false,
          lineTension: 0.3,
          borderDash: [5, 5],
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: 'Budget vs Actual vs Variance (Line Chart)'
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          },
          scaleLabel: {
            display: true,
            labelString: 'Amount (¥)'
          }
        }]
      }
    }
  });
},

    async forecast() {
      try {
        const res = await axios.post('/api/finance/forecast', this.budgetItems);
        this.forecastResult = res.data.forecast;
      } catch (err) {
        alert("Forecasting error: " + (err.response?.data?.detail || err.message));
      }
    },


drawForecastCharts() {
  if (!this.forecastResult) return;

  const budgetRate = parseFloat(this.forecastResult.budget_growth_rate || 0);
  const actualRate = parseFloat(this.forecastResult.actual_growth_rate || 0);

  const budgetCtx = document.getElementById('budgetGrowthChart');
  const actualCtx = document.getElementById('actualGrowthChart');

  if (this._forecastBudgetChart) this._forecastBudgetChart.destroy();
  if (this._forecastActualChart) this._forecastActualChart.destroy();

  this._forecastBudgetChart = new Chart(budgetCtx, {
    type: 'doughnut',
    data: {
      labels: ['Growth', 'Remaining'],
      datasets: [{
        data: [budgetRate, 100 - budgetRate],
        backgroundColor: ['#42a5f5', '#e3f2fd']
      }]
    },
    options: {
      responsive: false,
      cutoutPercentage: 70,
      title: {
        display: true,
        text: 'Budget Growth %'
      }
    }
  });

  this._forecastActualChart = new Chart(actualCtx, {
    type: 'doughnut',
    data: {
      labels: ['Growth', 'Remaining'],
      datasets: [{
        data: [actualRate, 100 - actualRate],
        backgroundColor: ['#66bb6a', '#e8f5e9']
      }]
    },
    options: {
      responsive: false,
      cutoutPercentage: 70,
      title: {
        display: true,
        text: 'Actual Growth %'
      }
    }
  });
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

.result-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  justify-content: space-between;
}
.result-cards .card {
  flex: 1;
  background-color: #e9f3ff;
  border: 1px solid #cce0ff;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
}
.result-cards .card h4 {
  margin-bottom: 10px;
  font-size: 16px;
  color: #0056b3;
}
.result-cards .card p {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.chart-grid {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  gap: 24px;
  margin-bottom: 30px;
}

.chart-card {
  flex: 1;
  background-color: #ffffff;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
  border: 1px solid #d0e6ff;
  text-align: center;
}

.chart-card h4 {
  margin-bottom: 16px;
  color: #007BFF;
  font-size: 16px;
  font-weight: 600;
}

.table-grid {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  margin-top: 30px;
}

.table-card {
  flex: 1;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
  border: 1px solid #d0e6ff;
}

.table-card h4 {
  color: #007BFF;
  margin-bottom: 16px;
  font-size: 16px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.styled-table th, .styled-table td {
  padding: 8px 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.styled-table tbody tr:hover {
  background-color: #f5faff;
}

.styled-table th {
  background-color: #e9f3ff;
  color: #0056b3;
  font-weight: bold;
}
.budget-input-row {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 10px;
}

.budget-input-row input {
  flex: 1;
  min-width: 120px;
}

.budget-input-row button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 14px;
}

.forecast-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
}

.forecast-donuts {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  margin-top: 10px;
}

.forecast-donuts canvas {
  margin: auto;
}

.forecast-donuts h5 {
  margin-bottom: 6px;
  font-size: 14px;
  color: #007BFF;
}

.form-row-container {
  display: flex;
  gap: 24px;
  margin-bottom: 40px;
  flex-wrap: wrap; /* ✅ 可选，屏幕窄时自动换行 */
}

.half-section {
  flex: 1;
  min-width: 460px;
  padding: 20px;
  background-color: #f9fcff;
  border-radius: 12px;
  border: 1px solid #d6e9ff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.08);
}


</style>
