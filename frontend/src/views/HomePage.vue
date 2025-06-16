<template>
  <div class="home-container">
<!--    <h2>📊 Project Summary Dashboard</h2>-->
    <!-- 在原有 .pdf-container 之上新增数据概览卡片和图表 -->
<div class="overview-container">
  <div class="stat-row">
    <div class="card stat-card">
      <h3>📊 Average</h3>
      <p>¥{{ averageEstimate }}</p>
    </div>
    <div class="card stat-card">
      <h3>📈 Highest</h3>
      <p>¥{{ maxEstimate }}</p>
    </div>
    <div class="card stat-card">
      <h3>📉 Lowest</h3>
      <p>¥{{ minEstimate }}</p>
    </div>
  </div>

  <div class="chart-row">
    <canvas id="pieChart"></canvas>
    <canvas id="lineChart"></canvas>
  </div>
</div>


    <p class="description">The following data is automatically collected from each module for final analysis and report export.</p>


    <div class="button-row">
      <button @click="downloadPdf">📥 Export PDF Report</button>
    </div>
    <div class="pdf-container">
      <div class="card">
      <h3>💼 Estimation Summary</h3>
      <ul>
        <li><strong>COCOMO Estimated Cost:</strong> ¥{{ summary.estimatedCost || '—' }}</li>
        <li><strong>Function Point (KLOC):</strong> {{ summary.fpKloc || '—' }}</li>
        <li><strong>Expert Judgment Estimate:</strong> ¥{{ summary.expert || '—' }}</li>
        <li><strong>Delphi Final Estimate:</strong> ¥{{ summary.delphi || '—' }}</li>
        <li><strong>Regression Estimate:</strong> ¥{{ summary.regress || '—' }}</li>

      </ul>
    </div>

    <div class="card">
      <h3>💰 Financial Analysis</h3>
      <ul>
        <li><strong>Cash Flow Inputs:</strong> {{ summary.npvFlows || '—' }}</li>
      </ul>
    </div>

    <div class="card">
      <h3>⚠️ Risk Assessment</h3>
      <ul>
        <li><strong>Sensitivity Parameters:</strong> {{ parsedParams || '—' }}</li>
        <li><strong>Monte Carlo Mean NPV:</strong> ¥{{ summary.monteCarloMean || '—' }}</li>
      </ul>
    </div>

    <div class="card">
      <h3>📅 Scheduling & Resources</h3>
      <ul>
        <li><strong>Task Schedule Entries:</strong> {{ parsedSchedule.length || '—' }}</li>
        <li><strong>Resource Allocations:</strong> {{ parsedResources.length || '—' }}</li>
      </ul>
    </div>
  </div>
  </div>
</template>

<script>
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { Chart } from 'chart.js';


export default {
  name: 'HomePage',
  data() {
  let scheduleResultRaw = localStorage.getItem("schedule_result");
  let resourceResultRaw = localStorage.getItem("resource_result");
  let npvFlowsRaw = localStorage.getItem("calculated_cash_flows");
  let sensitivityRaw = localStorage.getItem("sensitivity_params");

  let defaultSchedule = [
    { task: "Design", start: "T0", end: "T1" },
    { task: "Develop", start: "T1", end: "T3" },
    { task: "Test", start: "T3", end: "T4" }
  ];
  let defaultResource = [
    { role: "Frontend Dev", hours: 160 },
    { role: "Backend Dev", hours: 180 }
  ];

  return {
    summary: {
      estimatedCost: parseFloat(localStorage.getItem("estimated_cost")) || 125000,
      fpKloc: parseFloat(localStorage.getItem("fp_kloc")) || 18.5,
      expert: parseFloat(localStorage.getItem("expert_estimate")) || 135000,
      delphi: parseFloat(localStorage.getItem("delphi_estimate")) || 128000,
      regress: parseFloat(localStorage.getItem("regress_estimate")) || 122000,
      npvFlows: (() => {
        try {
          return JSON.parse(npvFlowsRaw) || [-1685493.52,800000,500000,900000];
        } catch {
          return [-1685493.52,800000,500000,900000];
        }
      })(),
      sensitivity: sensitivityRaw || JSON.stringify([
        { name: "Discount Rate", min: 0.05, max: 0.15 },
        { name: "Development Time", min: 4, max: 12 }
      ]),
      monteCarloMean: parseFloat(localStorage.getItem("monte_carlo_mean")) || 23750,
      scheduleResult: (() => {
        try {
          return scheduleResultRaw || JSON.stringify(defaultSchedule);
        } catch {
          return JSON.stringify(defaultSchedule);
        }
      })(),
      resourceResult: (() => {
        try {
          return resourceResultRaw || JSON.stringify(defaultResource);
        } catch {
          return JSON.stringify(defaultResource);
        }
      })()
    }
  };
},
  computed: {
    estimateValues() {
      return [
        this.summary.estimatedCost,
        this.summary.expert,
        this.summary.delphi,
        this.summary.regress
      ].filter(v => !isNaN(v));
    },
    averageEstimate() {
      const values = this.estimateValues;
      if (!values.length) return '—';
      return Math.round(values.reduce((a, b) => a + b, 0) / values.length);
    },
    maxEstimate() {
      const values = this.estimateValues;
      if (!values.length) return '—';
      return Math.max(...values);
    },
    minEstimate() {
      const values = this.estimateValues;
      if (!values.length) return '—';
      return Math.min(...values);
    },
    parsedParams() {
      try {
        const parsed = JSON.parse(this.summary.sensitivity);
        return parsed?.map(p => p.name).join(', ') || '—';
      } catch (e) {
        return '—';
      }
    },
    parsedSchedule() {
      try {
        return JSON.parse(this.summary.scheduleResult) || [];
      } catch {
        return [];
      }
    },
    parsedResources() {
      try {
        return JSON.parse(this.summary.resourceResult) || [];
      } catch {
        return [];
      }
    }
  },
mounted() {
  this.$nextTick(() => {
    const pieCanvas = document.getElementById('pieChart');
    const lineCanvas = document.getElementById('lineChart');

    if (!pieCanvas || !lineCanvas) {
      console.warn('Chart DOM not ready');
      return;
    }

    console.log("✅ Pie Chart Data:", [
      this.summary.estimatedCost,
      this.summary.expert,
      this.summary.delphi,
      this.summary.regress
    ]);

    console.log("✅ Line Chart Cash Flows:", this.summary.npvFlows);

    this.renderPieChart();
    this.renderLineChart();
  });
},
  methods: {
    async downloadPdf() {
      const container = document.querySelector('.pdf-container');
      const canvas = await html2canvas(container, { scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = 210;
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pageWidth;
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save('project-summary.pdf');
    },
renderPieChart() {
  if (!this.summary) return;

  const ctx = document.getElementById('pieChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['COCOMO', 'Expert', 'Delphi', 'Regression'],
      datasets: [{
        data: [
          this.summary.estimatedCost,
          this.summary.expert,
          this.summary.delphi,
          this.summary.regress
        ],
        backgroundColor: ['#3498db', '#e67e22', '#9b59b6', '#2ecc71']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
},

renderLineChart() {
  if (!this.summary || !Array.isArray(this.summary.npvFlows)) return;

  const ctx = document.getElementById('lineChart');
  if (!ctx) return;

  const flows = this.summary.npvFlows;
  if (!flows.length) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: flows.map((_, i) => `T${i}`),
      datasets: [{
        label: 'Cash Flow',
        data: flows,
        fill: false,
        borderColor: '#2c3e50',
        tension: 0.2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
},
}
};

</script>

<style scoped>
.home-container {
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.description {
  margin-bottom: 20px;
  font-style: italic;
  color: #666;
}

.card {
  background: #f9f9f9;
  padding: 16px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.card li {
  padding: 4px 0;
}

.button-row {
  text-align: left;
  margin-top: 20px;
}

button {
  background-color: #007BFF;
  color: white;
  padding: 8px 16px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.pdf-container {
  background: white;
  padding: 32px;
}

.overview-container {
  margin-bottom: 32px;
}
.chart-row {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  margin-top: 16px;
}
canvas {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.stat-row {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  flex: 1;
  text-align: center;
  padding: 20px;
}

.stat-card p {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

.chart-row {
  display: flex;
  gap: 24px;
  flex-wrap: nowrap;
}

.chart-row canvas {
  flex: 1;
  min-width: 0;
  height: 300px!important;
}

</style>
