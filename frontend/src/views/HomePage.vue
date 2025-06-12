<template>
  <div class="home-container">
    <h2>📊 Project Summary Dashboard</h2>

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

export default {
  name: 'HomePage',
  data() {
    return {
      summary: {
        estimatedCost: localStorage.getItem("estimated_cost"),
        fpKloc: localStorage.getItem("fp_kloc"),
        expert: localStorage.getItem("expert_estimate"),
        delphi: localStorage.getItem("delphi_estimate"),
        regress: localStorage.getItem("regress_estimate"),
        npvFlows: localStorage.getItem("calculated_cash_flows"),
        sensitivity: localStorage.getItem("sensitivity_params"),
        monteCarloMean: localStorage.getItem("monte_carlo_mean"),
        scheduleResult: localStorage.getItem("schedule_result"),
        resourceResult: localStorage.getItem("resource_result")
      }
    };
  },
  computed: {
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
  methods: {
     async downloadPdf() {
    const container = document.querySelector('.pdf-container');
    const canvas = await html2canvas(container, { scale: 2 });

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');

    const pageWidth = 210; // A4 width in mm
    // const pageHeight = 297; // A4 height in mm
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pageWidth;
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save('project-summary.pdf');
  }
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


</style>
