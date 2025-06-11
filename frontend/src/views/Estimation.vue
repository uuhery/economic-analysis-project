<template>
  <div>
    <h2>📈 Cost Estimation Panel</h2>

    <div v-if="getComparisonRows().length > 0">
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
          <tr v-for="row in getComparisonRows()" :key="row.model">
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

    <hr />
    <!-- === Function Point === -->
    <section>
      <h3>Function Point Estimation</h3>
      <p class="description">
        Estimate size via FP and then run COCOMO on converted KLOC.
      </p>

      <!-- FP 输入 -->
      <div v-for="(value, key) in fpInputs" :key="key">
        <label>{{ key.replace(/_/g, ' ') }}:</label>
        <input v-model.number="fpInputs[key]" type="number" min="0" />
      </div>

      <h4>Function Complexity Level (3-level)</h4>
      <div v-for="(levels, key) in fpWeightOptions" :key="key">
        <label>{{ key.replace(/_/g, ' ') }}:</label>
        <select v-model="fpSelections[key]">
          <option v-for="(val, label) in levels" :key="label" :value="label">
            {{ label }} ({{ val }})
          </option>
        </select>
      </div>


      <!-- 简单展示 cost_drivers，按需增删属性 -->
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

      <button @click="calculateFP">Estimate</button>

      <div v-if="result.fp">
        <p>Raw FP: {{ result.fp.raw_fp }}</p>
        <p>Adjusted FP: {{ result.fp.adjusted_fp }}</p>
        <p>KLOC: {{ result.fp.kloc }}</p>
      </div>
    </section>

    <hr />

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

    <hr />

    <!-- === Expert === -->
    <section>
      <h3>Expert Estimation</h3>
      <p class="description">
        Input multiple expert estimates. The system calculates their average.
      </p>
      <div v-for="(v, idx) in expertList" :key="idx" style="margin-bottom: 4px;">
        <input v-model.number="expertList[idx]" type="number" placeholder="Estimate value" />
        <button @click="removeExpert(idx)">🗑️</button>
      </div>
      <button @click="addExpert">Add Estimate</button>
      <button @click="calculateExpert">Estimate</button>
      <p v-if="result.expert !== null">Average Estimate: {{ result.expert }}</p>
    </section>

    <hr />

    <!-- === Delphi === -->
    <section>
      <h3>Delphi Method</h3>
      <p class="description">
        Enter expert estimates in multiple rounds. Each round represents anonymous feedback iteration.
      </p>

      <div v-for="(round, roundIdx) in delphiRounds" :key="roundIdx" style="margin-bottom: 8px;">
        <p>Round {{ roundIdx + 1 }}</p>
        <div v-for="(v, vIdx) in round" :key="vIdx" style="display: inline-block; margin-right: 4px;">
          <input v-model.number="delphiRounds[roundIdx][vIdx]" type="number" style="width: 60px;" />
        </div>
        <button @click="removeDelphiRound(roundIdx)">🗑️</button>
      </div>

      <button @click="addDelphiRound">Add Round</button>
      <button @click="calculateDelphi">Estimate</button>

      <div v-if="result.delphi">
        <p>Final Estimate: {{ result.delphi.final_estimate }}</p>
        <p>Standard Deviation: {{ result.delphi.std_deviation }}</p>
        <p>Rounds Count: {{ result.delphi.rounds_count }}</p>
      </div>
    </section>

    <hr />

    <!-- === Regression === -->
    <section>
      <h3>Regression Model</h3>
      <p class="description">
        Enter data pairs (x, y) for linear regression analysis. Each point represents one observation.
      </p>

      <div v-for="(pair, idx) in regressionPairs" :key="idx" style="margin-bottom: 4px;">
        <input v-model.number="regressionPairs[idx][0]" placeholder="x" style="width: 60px;" />
        <input v-model.number="regressionPairs[idx][1]" placeholder="y" style="width: 60px; margin-left: 10px;" />
        <button @click="removeRegression(idx)">🗑️</button>
      </div>
      <button @click="addRegression">Add Pair</button>
      <button @click="calculateRegression">Estimate</button>
      <div v-if="result.regression">
        <p>Intercept (a): {{ result.regression.intercept_a }}</p>
        <p>Slope (b): {{ result.regression.slope_b }}</p>
        <p>Sample Count: {{ result.regression.sample_count }}</p>
        <p>Predicted Y (x=100): {{ result.regression.example_prediction_x100 }}</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EstimationView',
  data() {
    return {
      fpInputs: {
        external_inputs: 0,
        external_outputs: 0,
        external_inquiries: 0,
        internal_files: 0,
        external_interfaces: 0
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
        loc: 15,
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
      expertList: [100, 120, 110],
      delphiInput: '',
      delphiRounds: [
        [100, 110, 120],
        [105, 108, 112],
        [106, 107, 109]
      ],
      regressionInput: '',
      regressionPairs: [
        [10, 100],
        [20, 200],
        [30, 300]
      ],
      result: {
        cocomo: null,
        fp: null,
        expert: null,
        delphi: null,
        regression: null
      }
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
            'http://localhost:8000/api/estimation/function_points',
            payload
        )
        this.result.fp = res.data
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
            'http://localhost:8000/api/estimation/cocomo',
            payload
        )
        this.result.cocomo = res.data
        localStorage.setItem("estimated_cost", res.data.total_cost.toString())
      } catch (err) {
        console.error(err)
        alert(err.response?.data?.detail || err.message)
      }
    },
    addExpert() { this.expertList.push(0); },
    removeExpert(index) { this.expertList.splice(index, 1); },
    async calculateExpert() {
      const valid = this.expertList.filter(x => !isNaN(x));
      const res = await axios.post('http://localhost:8000/api/estimation/expert', {
        estimates: valid
      });
      this.result.expert = res.data.average_estimate;
    },
    // methods:
    addDelphiRound() {
      this.delphiRounds.push([0, 0, 0]);
    },
    removeDelphiRound(idx) {
      this.delphiRounds.splice(idx, 1);
    },
    async calculateDelphi() {
      const rounds = this.delphiRounds.map(r =>
          r.filter(x => !isNaN(x))
      ).filter(r => r.length > 0);

      const res = await axios.post('http://localhost:8000/api/estimation/delphi', {
        rounds
      });
      this.result.delphi = res.data;
    },
    // methods:
    addRegression() {
      this.regressionPairs.push([0, 0]);
    },
    removeRegression(idx) {
      this.regressionPairs.splice(idx, 1);
    },
    async calculateRegression() {
      const data = this.regressionPairs
          .filter(pair => pair.length === 2 && pair.every(x => !isNaN(x)));
      const res = await axios.post('http://localhost:8000/api/estimation/regression', { data });
      this.result.regression = res.data;
    },
    getComparisonRows() {
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
          cost: this.result.expert,
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

      if (this.result.regression) {
        rows.push({
          model: 'Regression Model',
          effort: '—',
          time: '—',
          team: '—',
          cost: this.result.regression.example_prediction_x100,
          comment: `y(x=100)`
        });
      }

      return rows;
    }
  }
}
</script>

<style scoped>
section {
  margin-bottom: 40px;
}
label {
  display: inline-block;
  width: 200px;
}
input, select {
  margin-bottom: 10px;
  margin-right: 10px;
}
button {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
