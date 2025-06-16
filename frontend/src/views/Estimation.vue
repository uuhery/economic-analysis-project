<template>
  <div style="margin: 40px">
    <h2>📈 Cost Estimation Panel</h2>
    <div class="estimation-panels">

  <div v-if="comparisonRows.length > 0">
    <h3>📋 Estimation Comparison Summary</h3>
      <table border="1">
        <thead>
          <tr>
            <th>Model</th>
            <th>Effort (PM)</th>
            <th>Time (months)</th>
            <th>Team Size</th>
            <th>Total Cost</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in comparisonRows" :key="row.model">
            <td>{{ row.model }}</td>
            <td>{{ row.effort }}</td>
            <td>{{ row.time }}</td>
            <td>{{ row.team }}</td>
            <td>{{ row.cost }}</td>
            <td>{{ row.comment }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 图表展示 -->
    <div v-if="comparisonRows.length > 0" style="margin-top: 30px;">
      <h3>📊 Cost Estimation Chart</h3>
      <canvas id="comparisonChart" width="600" height="300"></canvas>
    </div>
    </div>

    <div class="estimation-panels">
<section>
  <h3>Function Point Estimation</h3>
  <p class="description">
    Estimate size via FP and then run COCOMO on converted KLOC.
  </p>

  <!-- 统一的两列网格容器 -->
  <div class="fp-grid">
    <!-- FP 输入 -->
    <div v-for="(value, key) in fpInputs" :key="key" class="fp-item">
      <label>{{ key.replace(/_/g, ' ') }}:</label>
      <input v-model.number="fpInputs[key]" type="number" min="0" />
    </div>

    <!-- FP 权重选择 -->
    <div v-for="(levels, key) in fpWeightOptions" :key="key" class="fp-item">
      <label>{{ key.replace(/_/g, ' ') }}:</label>
      <select v-model="fpSelections[key]">
        <option v-for="(val, label) in levels" :key="label" :value="label">
          {{ label }} ({{ val }})
        </option>
      </select>
    </div>
  </div>

  <div v-for="(v, k) in fpConfig.costDrivers" :key="k">
        <label>{{ k }}:</label>
        <input v-model.number="fpConfig.costDrivers[k]" type="number" step="0.01" min="0.01" />
      </div>

      <label>Language:</label>
      <select v-model="fpConfig.language">
        <option value="java">java</option>
        <option value="python">python</option>
        <option value="c++">c++</option>
        <option value="javascript">javascript</option>
        <option value="cobol">cobol</option>
      </select>

      <button @click="addCostDriver">+ Add Cost Driver</button>

      <button @click="calculateFP" style="margin-left: 10px">Estimate</button>

      <div v-if="result.fp">
        <p>Raw FP: {{ result.fp.raw_fp }}</p>
        <p>Adjusted FP: {{ result.fp.adjusted_fp }}</p>
        <p>KLOC: {{ result.fp.kloc }}</p>
      </div>
</section>

    <!-- === COCOMO === -->
    <section>
      <h3>COCOMO Estimation</h3>
      <p class="description">
        Estimate effort based on delivered KLOC, project mode and EAF.
      </p>
      <label>KLOC:</label>
      <input v-model.number="cocomo.loc" type="number" min="0" placeholder="e.g. 15" />

      <label>Mode:</label>
      <select v-model="cocomo.mode">
        <option value="organic">organic</option>
        <option value="semi-detached">semi-detached</option>
        <option value="embedded">embedded</option>
      </select>

      <div v-for="(value, key) in cocomo.costDrivers" :key="key">
        <label>{{ key }}:</label>
        <select v-model="cocomo.costDrivers[key]">
          <option value="Very Low">Very Low</option>
          <option value="Low">Low</option>
          <option value="Nominal">Nominal</option>
          <option value="High">High</option>
          <option value="Very High">Very High</option>
        </select>
      </div>

      <label>Cost per Person-Month:</label>
      <input v-model.number="cocomo.cost_per_pm" type="number" step="100" min="0" placeholder="e.g. 10000" />

      <button @click="calculateCocomo">Estimate</button>

      <div v-if="result.cocomo">
        <p>EAF: {{ result.cocomo.eaf }}</p>
        <p>Effort: {{ result.cocomo.effort_pm }} person-months</p>
        <p>Time: {{ result.cocomo.development_time_months }} months</p>
        <p>Team Size: {{ result.cocomo.team_size }} people</p>
        <p><strong>Total Cost:</strong> {{ result.cocomo.total_cost }} (currency)</p>
      </div>

    </section>
      </div>

        <div class="estimation-panels">

    <!-- === Expert === -->
    <section>
      <h3>Expert Judgment (Heuristic)</h3>
      <p class="description">Estimate project cost based on expert opinions with confidence weighting.</p>

      <div v-for="(expert, idx) in expertList" :key="idx" style="margin-bottom: 8px;">
        <input v-model="expert.name" placeholder="Expert Name" style="width: 100px;" />
        <input v-model.number="expert.estimate" type="number" placeholder="Estimate" style="width: 80px; margin-left: 8px;" />
        <input v-model.number="expert.confidence" type="number" step="0.01" min="0" max="1" placeholder="Confidence (0~1)" style="width: 120px; margin-left: 8px;" />
        <button @click="removeExpert(idx)">🗑️</button>
      </div>

      <button @click="addExpert">+ Add Expert</button>
      <button @click="calculateExpert">Estimate</button>

      <div v-if="result.expert !== null">
        <p><strong>Weighted Average:</strong> {{ result.expert.weighted_average }}</p>
        <p><strong>Standard Deviation:</strong> {{ result.expert.std_deviation }}</p>
        <p><strong>Estimate Range:</strong> {{ result.expert.min }} ~ {{ result.expert.max }}</p>
        <p><strong>Confidence Summary:</strong> {{ result.expert.avg_confidence }}</p>
      </div>
    </section>

    <!-- === Delphi === -->
    <section>
      <h3>Delphi Method (Heuristic)</h3>
      <p class="description">
        Enter expert estimates for each round. The system checks convergence after each round.
      </p>

      <!-- 各轮专家输入 -->
      <div v-for="(round, roundIdx) in delphiRounds" :key="roundIdx" style="margin-bottom: 12px;">
        <p><strong>Round {{ roundIdx + 1 }}</strong></p>
        <div v-for="(value, idx) in round" :key="idx" style="display: inline-block; margin-right: 6px;">
          <input v-model.number="delphiRounds[roundIdx][idx]" type="number" placeholder="Estimate" style="width: 80px;" />
        </div>
      </div>

      <button @click="addDelphiExpert">+ Add Expert to Current Round</button>
      <button @click="addDelphiRound" style="margin-left: 10px">➕ Add New Round</button>
      <button @click="calculateDelphi" style="margin-left: 10px">Estimate</button>

      <!-- 系统反馈 -->
      <div v-if="delphiResult">
        <h4>📊 System Feedback</h4>
        <ul>
          <li><strong>Final Estimate:</strong> {{ delphiResult.final_estimate }}</li>
          <li><strong>Rounds:</strong> {{ delphiResult.rounds_count }}</li>
          <li><strong>Standard Deviation:</strong> {{ delphiResult.std_deviation }}</li>
          <li><strong>Convergence:</strong> {{ delphiResult.convergence ? '✅ Yes' : '❌ No' }}</li>
        </ul>

        <h5>Estimate History</h5>
        <ul>
          <li v-for="r in delphiResult.estimate_history" :key="r.round">
            Round {{ r.round }} → Mean: {{ r.mean }}, Std: {{ r.std }}
          </li>
        </ul>

        <div v-if="!delphiResult.convergence">
          <p style="color: green;"><em>Suggest entering a new round with values near mean {{ delphiResult.estimate_history.at(-1).mean }}</em></p>
          <button @click="addDelphiFromSuggestion">Add Round Based on Last Mean</button>
        </div>

        <div v-else>
          <p style="color: blue;"><strong>🛑 Convergence reached. No more rounds needed.</strong></p>
        </div>
      </div>
    </section>
        </div>

    <!-- === Regression === -->
    <section>
      <h3>📈 Regression via File Upload</h3>

      <!-- 上传文件 -->
      <input type="file" @change="handleFileUpload" accept=".csv,.xlsx" />

      <!-- 选择列 & 输入预测 -->
      <div v-if="regressionColumns.length" style="margin-top: 12px;">
        <label>X (Independent Variable):</label>
        <select v-model="selectedX">
          <option v-for="col in regressionColumns" :key="col" :value="col">{{ col }}</option>
        </select>

        <label>Y (Dependent Variable):</label>
        <select v-model="selectedY">
          <option v-for="col in regressionColumns" :key="col" :value="col">{{ col }}</option>
        </select>

        <label>Predict X:</label>
        <input v-model.number="predictX" type="number" placeholder="e.g. 25" />

        <button @click="submitRegression">Run Regression</button>
      </div>

      <!-- 展示结果 -->
      <div v-if="regressionResult" style="margin-top: 16px;">
        <h4>📊 Regression Result</h4>
        <p><strong>Formula:</strong> {{ regressionResult.regression_formula }}</p>
        <p><strong>Prediction:</strong> y({{ predictX }}) = {{ regressionResult.predict_y }}</p>
        <p><strong>R²:</strong> {{ regressionResult.r_squared }}</p>
        <p><strong>Samples:</strong> {{ regressionResult.sample_count }}</p>
      </div>
    </section>

  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js'

export default {
  name: 'EstimationView',
  data() {
    return {
      fpInputs: {
        external_inputs: 50,
        external_outputs: 40,
        external_inquiries: 60,
        internal_files: 20,
        external_interfaces: 30
      },
      fpConfig: {
        language: 'java',
        costDrivers: {
        },
      },
      fpWeightOptions: {
        external_inputs: { Simple: 3, Average: 4, High: 6 },
        external_outputs: { Simple: 4, Average: 5, High: 7 },
        external_inquiries: { Simple: 3, Average: 4, High: 6 },
        internal_files: { Simple: 7, Average: 10, High: 15 },
        external_interfaces: { Simple: 5, Average: 7, High: 10 }
      },
      fpSelections: {
        external_inputs: 'Average',
        external_outputs: 'Average',
        external_inquiries: 'Average',
        internal_files: 'Average',
        external_interfaces: 'Average'
      },
      cocomo: {
        loc: 40,
        mode: 'organic',
        cost_per_pm: 10000,
        costDrivers: {
          RELY: 'Nominal',
          CPLX: 'Nominal',
          ACAP: 'Nominal',
          PCAP: 'Nominal',
          AEXP: 'Nominal',
          TOOL: 'Nominal'
        }
      },
      expertInput: '',
      expertList: [
        { name: 'Alice', estimate: 1300000, confidence: 0.9 },
        { name: 'Bob', estimate: 1450000, confidence: 0.7 },
        { name: 'Carol', estimate: 1400000, confidence: 0.8 }
      ],
      delphiRounds: [
        [1500000, 1340000, 1289000]
      ],
      delphiThreshold: 5.0,  // 收敛阈值
      delphiResult: null,
      delphiConverged: false,
      regressionFile: null,
      regressionColumns: [],
      selectedX: '',
      selectedY: '',
      predictX: null,
      regressionResult: null,
      result: {
        cocomo: null,
        fp: null,
        expert: null,
        delphi: null,
        regression: null
      },
      chartInstance: null,
      comparisonRows: []
    }
  },
  methods: {
    getFpWeightsFromSelections() {
      const weights = {}
      for (const key in this.fpSelections) {
        const level = this.fpSelections[key]
        weights[key] = this.fpWeightOptions[key][level]
      }
      return weights
    },
    async calculateFP() {
      try {
        const payload = {
          fp_inputs: this.fpInputs,
          fp_weights: this.getFpWeightsFromSelections(),  // ← 新增字段
          language: this.fpConfig.language,
          cost_drivers: this.fpConfig.costDrivers,
        }

        const res = await axios.post(
            '/api/estimation/function_points',
            payload
        )
        // axios.post('http://localhost:8000/estimation/function_points')

        this.result.fp = res.data
        localStorage.setItem('fp_kloc', res.data.kloc.toString());
        this.generateComparisonRows();
      } catch (err) {
        console.error(err)
        alert(err.response?.data?.detail || err.message)
      }
    },
    addCostDriver() {
      const key = prompt('Enter new cost driver key:')
      if (key) this.$set(this.fpConfig.costDrivers, key, 1.0)
    },
    async calculateCocomo() {
      try {
        const payload = {
          loc: this.cocomo.loc,
          mode: this.cocomo.mode,
          cost_drivers: this.cocomo.costDrivers,
          cost_per_pm: this.cocomo.cost_per_pm
        }
        const res = await axios.post(
            '/api/estimation/cocomo',
            payload
        )
        this.result.cocomo = res.data
        localStorage.setItem("estimated_cost", res.data.total_cost.toString())
        this.generateComparisonRows();
      } catch (err) {
        console.error(err)
        alert(err.response?.data?.detail || err.message)
      }
    },
    addExpert() {
      this.expertList.push({ name: '', estimate: 0, confidence: 1.0 });
    },
    removeExpert(index) {
      this.expertList.splice(index, 1);
    },
    async calculateExpert() {
      const filtered = this.expertList.filter(x =>
        !isNaN(x.estimate) && !isNaN(x.confidence) && x.confidence >= 0 && x.confidence <= 1
      );

      if (filtered.length === 0) {
        alert("Please input at least one valid expert entry.");
        return;
      }

      const res = await axios.post("/api/estimation/expert", {
        experts: filtered
      });

      this.result.expert = res.data;
      localStorage.setItem('expert_estimate', res.data.weighted_average.toString());
      this.generateComparisonRows();
    },
    addDelphiExpert() {
      if (this.delphiRounds.length === 0) {
        this.delphiRounds.push([]);
      }

      const lastIndex = this.delphiRounds.length - 1;
      const newRound = [...this.delphiRounds[lastIndex], 0];  // 拷贝原有数组 + 添加一个新值

      // 替换整轮，确保 Vue 能检测到更新
      this.$set(this.delphiRounds, lastIndex, newRound);
    },
    addDelphiRound() {
      this.delphiRounds.push([]);
    },
    addDelphiFromSuggestion() {
      const lastMean = this.delphiResult.estimate_history.at(-1).mean;
      const expertCount = this.delphiRounds[this.delphiRounds.length - 1].length || 3;
      const newRound = Array(expertCount).fill(Number((lastMean).toFixed(1)));
      this.delphiRounds.push(newRound);
    },
    async calculateDelphi() {
      const cleanRounds = this.delphiRounds.map(r => r.filter(x => !isNaN(x)));
      if (cleanRounds.length === 0 || cleanRounds.at(-1).length === 0) {
        alert("Please input at least one round of estimates.");
        return;
      }

      try {
        const res = await axios.post('/api/estimation/delphi', {
          rounds: cleanRounds,
          convergence_threshold: this.delphiThreshold
        });
        this.delphiResult = res.data;
        this.result.delphi = res.data;
        localStorage.setItem('delphi_estimate', res.data.final_estimate.toString());
        this.delphiConverged = res.data.convergence;
        this.generateComparisonRows();
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.detail || err.message);
      }
    },
    // 读取文件，提取列名（模拟预处理，只展示文件名）
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.regressionFile = file;

      // 简化模拟：假设服务端会读取列名，但也可以本地读取 CSV
      // 为了体验流畅，这里直接手动输入测试列名
      const filename = file.name.toLowerCase();
      if (filename.endsWith('.csv') || filename.endsWith('.xlsx')) {
        // 👇可以改为发送到后端获得真实列名，这里用默认
        this.regressionColumns = ['KLOC', 'Cost', 'Effort', 'Function Points']; // 示例列名
        this.selectedX = this.regressionColumns[0];
        this.selectedY = this.regressionColumns[1];
      } else {
        alert("Only CSV or XLSX supported.");
      }
    },

    // 发送到 FastAPI 接口
    async submitRegression() {
      if (!this.regressionFile || !this.selectedX || !this.selectedY || this.predictX === null) {
        alert("Please complete file, column selections and input.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.regressionFile);
      formData.append("x_column", this.selectedX);
      formData.append("y_column", this.selectedY);
      formData.append("predict_x", this.predictX);

      try {
        const res = await fetch("/api/estimation/regression", {
          method: "POST",
          body: formData
        });
        if (!res.ok) throw new Error("Server error");
        const data = await res.json();
        this.regressionResult = data;
        localStorage.setItem('regress_estimate', this.regressionResult.predict_y.toString());

        this.generateComparisonRows();
      } catch (err) {
        console.error(err);
        alert("Regression failed: " + err.message);
      }
    },
    generateComparisonRows() {
      const rows = [];

      if (this.result.cocomo) {
        rows.push({
          model: 'COCOMO',
          effort: this.result.cocomo.effort_pm,
          time: this.result.cocomo.development_time_months,
          team: this.result.cocomo.team_size,
          cost: this.result.cocomo.total_cost,
          comment: 'Classic engineering model'
        });
      }

      if (this.result.fp) {
        rows.push({
          model: 'Function Point',
          effort: '—',
          time: '—',
          team: '—',
          cost: `Converted: ${this.result.fp.kloc} KLOC`,
          comment: 'Size-based estimation'
        });
      }

      if (this.result.expert !== null) {
        rows.push({
          model: 'Expert Judgment',
          effort: '—',
          time: '—',
          team: '—',
          cost: this.result.expert.weighted_average,
          comment: 'Average of expert inputs'
        });
      }

      if (this.result.delphi) {
        rows.push({
          model: 'Delphi Method',
          effort: '—',
          time: '—',
          team: '—',
          cost: this.result.delphi.final_estimate,
          comment: `SD: ${this.result.delphi.std_deviation}`
        });
      }

      if (this.regressionResult) {
        rows.push({
          model: 'Regression Model',
          effort: '—',
          time: '—',
          team: '—',
          cost: this.regressionResult.predict_y,
          comment: `y(x=${this.predictX})`
        });
      }

      this.comparisonRows = rows;
      this.renderComparisonChart();
    },

    renderComparisonChart() {
      const ctx = document.getElementById("comparisonChart");
      if (!ctx) return;

      // 🔥 只过滤出非 Function Point 的模型
      const filteredRows = this.comparisonRows.filter(r => r.model !== 'Function Point');

      const labels = filteredRows.map(r => r.model);
      const costs = filteredRows.map(r => {
        const value = Number(r.cost);
        return isNaN(value) ? 0 : value;
      });

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Estimated Cost",
            data: costs,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {beginAtZero: true}
          }
        }
      });
    }

  }
}
</script>

<style scoped>
/* === 全局布局 === */
section {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f9fcff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
  border: 1px solid #d6e9ff;
}

h2, h3, h4, h5 {
  color: #007BFF;
  margin-bottom: 16px;
  font-weight: 600;
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

/* === 表单输入样式 === */
label {
  display: inline-block;
  min-width: 160px;
  font-weight: 500;
  margin-bottom: 6px;
}

input, select {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  margin-right: 10px;
  transition: border-color 0.2s ease;
}
input:focus, select:focus {
  border-color: #007BFF;
  outline: none;
}

/* === 按钮样式 === */
button {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 10px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #0056b3;
}

/* === 表格样式 === */
table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #cce5ff;
  box-shadow: 0 2px 6px rgba(0, 123, 255, 0.08);
  margin-top: 12px;
}
th, td {
  padding: 10px;
  text-align: center;
  border: 1px solid #d4ecff;
}
th {
  background-color: #e7f3ff;
  color: #0056b3;
  font-weight: 600;
}

/* === Delphi 建议部分 === */
em {
  color: #28a745;
  font-weight: 500;
}

ul {
  list-style: none;
  padding-left: 0;
}
li {
  margin-bottom: 6px;
}

/* === 文件上传提示样式 === */
input[type="file"] {
  border: 1px dashed #007BFF;
  padding: 6px;
  border-radius: 6px;
  background-color: #f0faff;
  cursor: pointer;
}

.fp-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 两列布局 */
  gap: 20px 32px; /* 行距、列距 */
  margin-top: 10px;
}

.fp-item {
  display: flex;
  flex-direction: column;
}

.fp-item label {
  font-weight: 500;
  margin-bottom: 6px;
  color: #333;
}

.fp-item input,
.fp-item select {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
  transition: border-color 0.2s ease;
}
.fp-item input:focus,
.fp-item select:focus {
  border-color: #007BFF;
  outline: none;
}

.estimation-panels {
  display: flex;
  gap: 50px; /* 两卡片间距 */
  margin-bottom: 30px;
  /*flex-wrap: wrap; !* 小屏自动换行 *!*/
}

.panel {
  flex: 1;
  min-width: 400px; /* 可根据屏幕适配调整 */
  background-color: #f9fcff;
  border-radius: 12px;
  border: 1px solid #d6e9ff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.08);
  padding: 20px;
}


</style>
