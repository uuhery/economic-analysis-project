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

    <!-- === 功能点估算 === -->
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

    <!-- === 专家估算 === -->
    <section>
      <h3>Expert Estimation</h3>
      <label>Estimates (comma-separated):</label>
      <input v-model="expertInput" placeholder="100,120,110" />
      <button @click="calculateExpert">Estimate</button>
      <p v-if="result.expert !== null">Average Estimate: {{ result.expert }}</p>
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
      result: {
        cocomo: null,
        fp: null,
        expert: null
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
}
button {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
