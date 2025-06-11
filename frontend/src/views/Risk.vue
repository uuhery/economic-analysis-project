<template>
  <div>
    <h2>Risk Analysis Dashboard</h2>

    <!-- 敏感性分析 -->
    <section>
      <h3>Sensitivity Analysis</h3>
      <input v-model.number="sensitivity.baseValue" placeholder="Base Value" />
      <input v-model="sensitivity.rangeStr" placeholder="Variable Range (comma-separated)" />
      <input v-model.number="sensitivity.multiplier" placeholder="Multiplier" />
      <button @click="runSensitivity">Run</button>
      <p v-if="sensitivity.result.length">Impact: {{ sensitivity.result }}</p>
      <canvas v-if="sensitivity.result.length" id="sensitivityChart" class="chart-canvas"></canvas>
    </section>

    <hr />

    <!-- 决策树分析 -->
    <section>
      <h3>Decision Tree</h3>
      <div v-for="(p, index) in decisionTree.paths" :key="index">
        <input v-model.number="p.probability" placeholder="Probability" />
        <input v-model.number="p.value" placeholder="Value" />
        <button @click="removePath(index)">Remove</button>
      </div>
      <button @click="addPath">Add Path</button>
      <button @click="runDecisionTree">Run</button>
      <p v-if="decisionTree.result !== null">Expected Value: {{ decisionTree.result }}</p>
    </section>

    <hr />

    <!-- 蒙特卡洛模拟 -->
    <section>
      <h3>Monte Carlo Simulation</h3>
      <input v-model.number="monteCarlo.base" placeholder="Base" />
      <input v-model.number="monteCarlo.stdDev" placeholder="Standard Deviation" />
      <input v-model.number="monteCarlo.iterations" placeholder="Iterations" />
      <button @click="runMonteCarlo">Run</button>
      <div v-if="monteCarlo.result">
        <p>Mean: {{ monteCarlo.result.mean }}</p>
        <p>Min: {{ monteCarlo.result.min }}</p>
        <p>Max: {{ monteCarlo.result.max }}</p>
        <p>Std Dev: {{ monteCarlo.result.std_dev }}</p>
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
        baseValue: 100,
        rangeStr: '90,100,110',
        multiplier: 1.0,
        result: []
      },
      decisionTree: {
        paths: [{ probability: 0.5, value: 1000 }, { probability: 0.5, value: -500 }],
        result: null
      },
      monteCarlo: {
        base: 1000,
        stdDev: 200,
        iterations: 1000,
        result: null
      }
    };
  },
  methods: {
    async runSensitivity() {
      const range = this.sensitivity.rangeStr.split(',').map(Number);
      try {
        const res = await axios.post('/api/risk/sensitivity', {
          base_value: this.sensitivity.baseValue,
          variable_range: range,
          multiplier: this.sensitivity.multiplier
        });
        this.sensitivity.result = res.data.impact;
        this.$nextTick(() => {
          const ctx = document.getElementById('sensitivityChart').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: res.data.labels,  // 例如 ['90', '100', '110']
              datasets: [{
                label: 'Impact',
                data: res.data.impact,
              }]
            },
            options: { responsive: true, scales: { y: { beginAtZero: true } } }
          });
        });
      } catch (err) {
        alert("Error in sensitivity: " + err.message);
      }
    },

    addPath() {
      this.decisionTree.paths.push({ probability: 0.0, value: 0 });
    },
    removePath(index) {
      this.decisionTree.paths.splice(index, 1);
    },
    async runDecisionTree() {
      try {
        const res = await axios.post('/api/risk/decision-tree', this.decisionTree.paths);
        this.decisionTree.result = res.data.expected_value;
      } catch (err) {
        alert("Error in decision tree: " + err.message);
      }
    },

    async runMonteCarlo() {
      try {
        const res = await axios.post('/api/risk/monte-carlo', {
          base: this.monteCarlo.base,
          std_dev: this.monteCarlo.stdDev,
          iterations: this.monteCarlo.iterations
        });
        this.monteCarlo.result = res.data;
      } catch (err) {
        alert("Error in Monte Carlo: " + err.message);
      }
    }
  }
};
</script>

<style scoped>
section {
  margin-bottom: 24px;
}
input {
  margin: 4px;
}
.chart-canvas {
  width: 800px !important;
  height: 450px !important;
  display: block;
  margin: 0 auto;
}


</style>
