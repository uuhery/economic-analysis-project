<template>
  <div>
    <h2>Risk Analysis Dashboard</h2>

        <!-- 敏感性分析 -->
    <section>
      <h3>Sensitivity Analysis</h3>

      <label>Cash Flows:</label>
      <input
        v-model="sensitivity.baseContext.cash_flows_str"
        placeholder="e.g. -1000,300,400,500"
      />
      <button @click="loadCachedCashFlows">Use Previous Cash Flows</button>

      <p class="description">Specify key uncertain parameters to evaluate how changes affect project NPV.</p>

      <div v-for="(param, index) in sensitivity.params" :key="index" class="param-block">
        <label>Parameter Name:</label>
        <select v-model="param.name">
          <option disabled value="">-- Select Parameter --</option>
          <option value="loc">Lines of Code (KLOC)</option>
          <option value="cost_per_pm">Cost per Person-Month</option>
          <option value="fp_kloc">Function Points per KLOC</option>
          <option value="discount_rate">Discount Rate (%)</option>
          <option value="market_growth">Market Growth (%)</option>
          <option value="project_delay_cost">Project Delay Cost</option>
          <option value="staff_productivity">Staff Productivity</option>
          <option value="initial_cost">Initial Cost</option>
        </select>



        <label>Min:</label>
        <input type="number" v-model.number="param.min" placeholder="e.g. 0.05" />

        <label>Max:</label>
        <input type="number" v-model.number="param.max" placeholder="e.g. 0.15" />

        <label>Distribution:</label>
        <select v-model="param.distribution">
          <option disabled value="">-- Distribution --</option>
          <option value="uniform">Uniform</option>
          <option value="triangular">Triangular</option>
          <option value="normal">Normal</option>
        </select>

        <button @click="removeParam(index)">Remove</button>
      </div>

      <div class="button-row">
        <button @click="addParam">Add Parameter</button>
        <button @click="loadSampleSensitivity">Load Example</button>
        <button @click="runSensitivity">Run</button>
      </div>

      <canvas v-if="sensitivity.chartData.length" id="sensitivityChart" class="chart-canvas"></canvas>
    </section>

    <!-- 决策树分析 -->
    <section>
      <h3>Decision Tree</h3>
      <p class="description">Model choices and outcomes using probability-weighted expected value paths.</p>

      <div v-for="(p, index) in decisionTree.paths" :key="index" class="param-block">
        <label>Path {{ index + 1 }} Probability (0~1):</label>
        <input v-model.number="p.probability" placeholder="e.g. 0.6" />

        <label>Expected Value:</label>
        <input v-model.number="p.value" placeholder="e.g. 100000" />

        <button @click="removePath(index)" v-if="decisionTree.paths.length > 1">Remove</button>
      </div>

      <div class="button-row">
        <button @click="addPath">Add Path</button>
        <button @click="loadSampleDecisionTree">Load Example</button>
        <button @click="runDecisionTree">Run</button>
      </div>

      <p v-if="decisionTree.result !== null"><strong>Expected Value:</strong> {{ decisionTree.result }}</p>
    </section>



    <!-- 蒙特卡洛模拟 -->
    <section>
      <h3>Monte Carlo Simulation</h3>
      <p class="description">Simulate many possible outcomes under uncertainty using distribution-based sampling.</p>

      <label>Base NPV Estimate:</label>
      <input v-model.number="monteCarlo.base" placeholder="e.g. 1000" />

      <label>Standard Deviation:</label>
      <input v-model.number="monteCarlo.stdDev" placeholder="e.g. 200" />

      <label>Distribution Type:</label>
      <select v-model="monteCarlo.distribution">
        <option value="normal">Normal (Gaussian)</option>
        <option value="triangular">Triangular</option>
      </select>

      <label>Number of Iterations:</label>
      <input v-model.number="monteCarlo.iterations" placeholder="e.g. 1000" />

      <div class="button-row">
        <button @click="loadSampleMonteCarlo">Load Example</button>
        <button @click="runMonteCarlo">Run</button>
      </div>

      <div v-if="monteCarlo.result">
        <p><strong>Mean:</strong> {{ monteCarlo.result.mean }}</p>
        <p><strong>Std Dev:</strong> {{ monteCarlo.result.std_dev }}</p>
        <p><strong>Loss Probability:</strong> {{ monteCarlo.result.loss_probability }}</p>
        <p><strong>High Return Probability:</strong> {{ monteCarlo.result.high_return_probability }}</p>
        <canvas id="monteCarloChart" class="chart-canvas"></canvas>
      </div>
    </section>


  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js';

export default {
  name: 'RiskView',
  data() {
    return {
      sensitivity: {
        baseContext: {
          cash_flows: [],
          cash_flows_str: ''  // ← 必须补上这个！
        },
        params: [
          { name: '', min: 0, max: 0, distribution: 'uniform' }
        ],
        chartData: [],
        _chartInstance: null  // 👈 添加这行
      },
      decisionTree: {
        paths: [{ probability: 0.5, value: 1000 }, { probability: 0.5, value: -500 }],
        result: null
      },
      monteCarlo: {
        base: 1000,
        stdDev: 250,
        distribution: 'normal',
        iterations: 1000,
        result: null
      }
    };
  },
  methods: {
    loadCachedCashFlows() {
      const cached = localStorage.getItem("calculated_cash_flows");
      if (cached) {
        this.sensitivity.baseContext.cash_flows_str = cached;
      } else {
        alert("No cached cash flows found.");
      }
    },
    addParam() {
      this.sensitivity.params.push({ name: '', min: 0, max: 0, distribution: 'uniform' });
    },
    removeParam(index) {
      this.sensitivity.params.splice(index, 1);
    },
    loadSampleSensitivity() {
      this.sensitivity.baseContext.cash_flows_str = "-1000, 300, 400, 500";  // 🟦 示例现金流

      this.sensitivity.params = [
        { name: "loc", min: 10, max: 40, distribution: "uniform" },
        { name: "cost_per_pm", min: 8000, max: 15000, distribution: "triangular" },
        { name: "fp_kloc", min: 12, max: 30, distribution: "triangular" },
        { name: "discount_rate", min: 0.04, max: 0.12, distribution: "uniform" },
        { name: "market_growth", min: 0.01, max: 0.1, distribution: "triangular" },
        { name: "project_delay_cost", min: 10000, max: 60000, distribution: "uniform" },
        { name: "staff_productivity", min: 0.8, max: 1.2, distribution: "triangular" }
      ];
    },

    async runSensitivity() {
      // 转换字符串现金流为数字数组
      const cashFlowStr = this.sensitivity.baseContext.cash_flows_str || '';
      const cashFlows = cashFlowStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));

      if (cashFlows.length === 0) {
        alert("Please provide valid cash flows.");
        return;
      }

      const payload = {
        base_context: {
          cash_flows: cashFlows,
          // 自动注入敏感参数的中位值作为 base_context 默认
          ...Object.fromEntries(
            this.sensitivity.params.map(p => [p.name, (p.min + p.max) / 2])
          )
        },
        params: this.sensitivity.params
      };

      try {
        const res = await axios.post('/api/risk/sensitivity', payload);
        this.sensitivity.chartData = res.data;
        this.$nextTick(() => {
          const filtered = res.data.filter(p => p.param === "discount_rate");
          if (!filtered.length) {
            alert("No result for discount_rate");
            return;
          }
          const result = filtered[0];
          const ctx = document.getElementById('sensitivityChart').getContext('2d');
          if (this.sensitivity._chartInstance) {
            this.sensitivity._chartInstance.destroy();
          }
          this.sensitivity._chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ['Min NPV', 'Mean NPV', 'Max NPV', 'Std Dev'],
              datasets: [{
                label: 'Discount Rate Sensitivity',
                data: [result.min_npv, result.mean_npv, result.max_npv, result.std_npv],
                backgroundColor: ['#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9']
              }]
            },
            options: {
              responsive: true,
              indexAxis: 'y',
              scales: {
                x: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: 'NPV Value'
                  }
                },
                y: {
                  title: {
                    display: true,
                    text: 'Metric'
                  }
                }
              },
              plugins: {
                title: {
                  display: true,
                  text: 'NPV Breakdown: Impact of Discount Rate',
                  font: {size: 18}
                },
                legend: {display: false}
              }
            }
          });
          localStorage.setItem('sensitivity_params', JSON.stringify(this.sensitivity.params));
          localStorage.setItem('sensitivity_chart_data', JSON.stringify(this.sensitivity.chartData));

        })
      } catch (err) {
        alert("Error in sensitivity: " + err.message);
      }
    },
    loadSampleDecisionTree() {
      this.decisionTree.paths = [
        { probability: 0.7, value: 100000 },
        { probability: 0.3, value: -30000 }
      ];
    },
    addPath() {
      this.decisionTree.paths.push({ probability: 0.0, value: 0 });
    },
    removePath(index) {
      this.decisionTree.paths.splice(index, 1);
    },
    async runDecisionTree() {
      const sumProb = this.decisionTree.paths.reduce((s, p) => s + p.probability, 0);
      if (Math.abs(sumProb - 1.0) > 0.01) {
        alert("Sum of probabilities must be approximately 1.0 (current: " + sumProb.toFixed(2) + ")");
        return;
      }
      try {
        const res = await axios.post('/api/risk/decision-tree', this.decisionTree.paths);
        this.decisionTree.result = res.data.expected_value;
      } catch (err) {
        alert("Error in decision tree: " + err.message);
      }
    },

    loadSampleMonteCarlo() {
      this.monteCarlo.base = 1000;
      this.monteCarlo.stdDev = 250;
      this.monteCarlo.distribution = 'normal';
      this.monteCarlo.iterations = 1000;
    },
    async runMonteCarlo() {
      try {
        const res = await axios.post('/api/risk/monte-carlo', {
          base: this.monteCarlo.base,
          std_dev: this.monteCarlo.stdDev,
          distribution: this.monteCarlo.distribution,
          iterations: this.monteCarlo.iterations
        });
        this.monteCarlo.result = res.data;
        localStorage.setItem('monte_carlo_mean', res.data.mean.toString());
        this.$nextTick(() => {
          const ctx = document.getElementById('monteCarloChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: res.data.npv_distribution.map((_, i) => i),
              datasets: [{
                label: 'Simulated NPV',
                data: res.data.npv_distribution
              }]
            },
            options: {
              responsive: true,
              scales: { y: { beginAtZero: true } }
            }
          });
        });
      } catch (err) {
        alert("Monte Carlo error: " + err.message);
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
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.08);
  border: 1px solid #d6e9ff;
}

/* 标题风格 */
h2, h3 {
  color: #007BFF;
  margin-bottom: 16px;
  font-weight: 600;
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

/* 输入框 */
input {
  width: 220px;
  padding: 6px 10px;
  margin: 6px 10px 6px 0;
  border-radius: 6px;
  border: 1px solid #ccc;
  transition: border-color 0.2s ease;
}
input:focus {
  border-color: #007BFF;
  outline: none;
}

/* 按钮样式 */
button {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  margin: 6px 8px 6px 0;
  font-weight: 500;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #0056b3;
}

/* 图表容器 */
.chart-canvas {
  width: 100% !important;
  max-width: 800px;
  height: 420px !important;
  display: block;
  margin: 20px auto 0;
}

/* 段落与文本输出 */
p {
  font-size: 15px;
  color: #333;
  margin: 10px 0 0;
}
strong {
  color: #0056b3;
}

.param-block {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px 0;
  border-radius: 8px;
  background: #fefefe;
}

.param-block label {
  display: inline-block;
  width: 140px;
  font-weight: 500;
  margin: 4px 0;
}

.button-row button {
  margin-right: 10px;
}


</style>
