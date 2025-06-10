<template>
  <div>
    <h2>📈 Cost Estimation Panel</h2>

    <!-- === COCOMO === -->
    <section>
      <h3>COCOMO Estimation</h3>
      <p class="description">
        Estimate effort based on the number of delivered source lines of code (KLOC) and project mode.
      </p>
      <label>KLOC:</label>
      <input v-model="cocomo.loc" type="number" placeholder="e.g. 15" />      <label>Mode:</label>
      <select v-model="cocomo.mode">
        <option>organic</option>
        <option>semi-detached</option>
        <option>embedded</option>
      </select>
      <button @click="calculateCocomo">Estimate</button>
      <p v-if="result.cocomo !== null">Estimated Effort: {{ result.cocomo }} person-months</p>
    </section>

    <hr />

    <!-- === Function Point === -->
    <section>
      <h3>Function Point Estimation</h3>
      <p class="description">
        Estimate software size based on functional components such as inputs, outputs, and files.
      </p>
      <div v-for="(value, key) in fpInputs" :key="key">
        <label>{{ key.replaceAll('_', ' ') }}:</label>
        <input v-model.number="fpInputs[key]" type="number" min="0" />
      </div>
      <button @click="calculateFP">Estimate</button>
      <div v-if="result.fp">
        <p>Function Points: {{ result.fp.function_points }}</p>
        <p>Estimated Effort (hours): {{ result.fp.estimated_effort_hours }}</p>
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
      cocomo: { loc: 15, mode: 'organic' },
      fpInputs: {
        external_inputs: 0,
        external_outputs: 0,
        external_inquiries: 0,
        internal_files: 0,
        external_interfaces: 0
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
    async calculateCocomo() {
      const res = await axios.post('http://localhost:8000/api/estimation/cocomo', this.cocomo);
      this.result.cocomo = res.data.effort_person_months;
    },
    async calculateFP() {
      const res = await axios.post('http://localhost:8000/api/estimation/function_points', this.fpInputs);
      this.result.fp = res.data;
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
