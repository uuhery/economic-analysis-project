<template>
  <div>
    <h2>📈 Cost Estimation Panel</h2>

    <!-- === COCOMO === -->
    <section>
      <h3>COCOMO Estimation</h3>
      <label>KLOC:</label>
      <input v-model="cocomo.loc" type="number" />
      <label>Mode:</label>
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
      <div v-for="(value, key) in fpInputs" :key="key">
        <label>{{ key }}:</label>
        <input v-model.number="fpInputs[key]" type="number" />
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
      <label>Estimates (comma-separated):</label>
      <input v-model="expertInput" placeholder="100,120,110" />
      <button @click="calculateExpert">Estimate</button>
      <p v-if="result.expert !== null">Average Estimate: {{ result.expert }}</p>
    </section>

    <hr />

    <!-- === Delphi === -->
    <section>
      <h3>Delphi Method</h3>
      <label>Rounds (semicolon + comma):</label>
      <input
          v-model="delphiInput"
          placeholder="100,110,120;105,108,112;106,107,109"
      />
      <button @click="calculateDelphi">Estimate</button>
      <div v-if="result.delphi">
        <p>Final Estimate: {{ result.delphi.final_estimate }}</p>
        <p>Std Deviation: {{ result.delphi.std_deviation }}</p>
        <p>Rounds Count: {{ result.delphi.rounds_count }}</p>
      </div>
    </section>

    <hr />

    <!-- === Regression === -->
    <section>
      <h3>Regression Model</h3>
      <label>Data (format: x1,y1;x2,y2):</label>
      <input
          v-model="regressionInput"
          placeholder="10,100;20,200;30,300"
      />
      <button @click="calculateRegression">Estimate</button>
      <div v-if="result.regression">
        <p>Intercept (a): {{ result.regression.intercept_a }}</p>
        <p>Slope (b): {{ result.regression.slope_b }}</p>
        <p>Sample Count: {{ result.regression.sample_count }}</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EstimationPanel',
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
      delphiInput: '',
      regressionInput: '',
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
    async calculateExpert() {
      const list = this.expertInput.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
      const res = await axios.post('http://localhost:8000/api/estimation/expert', { estimates: list });
      this.result.expert = res.data.average_estimate;
    },
    async calculateDelphi() {
      const rounds = this.delphiInput.split(';')
          .map(r => r.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x)))
          .filter(arr => arr.length > 0);
      const res = await axios.post('http://localhost:8000/api/estimation/delphi', { rounds });
      this.result.delphi = res.data;
    },
    async calculateRegression() {
      const data = this.regressionInput.split(';')
          .map(pair => pair.split(',').map(x => parseFloat(x.trim())))
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
