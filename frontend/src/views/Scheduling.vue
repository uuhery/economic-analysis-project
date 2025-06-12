<template>
  <div>
    <h2>📅 Scheduling & Resource Optimization</h2>

    <!-- 任务排布优化 -->
    <section>
      <h3>Task Scheduling</h3>
      <div v-for="(task, i) in scheduleTasks" :key="i" class="param-block">
        <input v-model="task.name" placeholder="Task name" />
        <input v-model.number="task.duration" type="number" placeholder="Duration (e.g. 3)" />
        <input v-model.number="task.deadline" type="number" placeholder="Deadline (e.g. 10)" />
        <input v-model.number="task.priority" type="number" placeholder="Priority (1 = high)" />
        <input v-model.number="task.earliest_start" type="number" placeholder="Earliest Start (e.g. 0)" />
        <button @click="removeScheduleTask(i)" v-if="scheduleTasks.length > 1">Remove</button>
      </div>
      <div class="button-row">
        <button @click="loadSampleSchedule">Load Sample</button>
        <button @click="addScheduleTask">Add Task</button>
        <button @click="runSchedule">Run Optimization</button>
      </div>

      <div v-if="scheduleResult.length">
        <h4>Schedule Result:</h4>
        <ul>
          <li v-for="r in scheduleResult" :key="r.name">
            {{ r.name }} -
            <span v-if="r.skipped">Skipped: {{ r.reason || 'No feasible slot' }}</span>
            <span v-else>Start: {{ r.start }}, End: {{ r.end }}, Load: {{ r.resource_usage }}</span>
          </li>
        </ul>
      </div>

      <canvas v-if="scheduleResult.length" id="scheduleChart" class="chart-canvas"></canvas>

    </section>

    <!-- 资源平滑与均衡 -->
    <section>
      <h3>Resource Smoothing</h3>
      <div v-for="(task, i) in resourceTasks" :key="i" class="param-block">
        <input v-model="task.name" placeholder="Task name" />
        <input v-model.number="task.workload" type="number" placeholder="Workload (e.g. 30)" />
        <input v-model.number="task.flexibility" type="number" placeholder="Max Delay Tolerance (days)" />
        <button @click="removeResourceTask(i)" v-if="resourceTasks.length > 1">Remove</button>
      </div>
      <div>
        <label>Total Resources:</label>
        <input v-model.number="resourceInput.total_resources" type="number" />
        <label>Total Time Slots:</label>
        <input v-model.number="resourceInput.total_time" type="number" />
      </div>
      <div class="button-row">
        <button @click="loadSampleResources">Load Sample</button>
        <button @click="addResourceTask">Add Task</button>
        <button @click="runResourceBalance">Run Smoothing</button>
      </div>

      <div v-if="resourceResult.length">
        <h4>Allocation Result:</h4>
        <ul>
          <li v-for="r in resourceResult" :key="r.name">
            {{ r.name }} - Slots: {{ r.slots.join(', ') }} | Per Slot: {{ r.allocated_per_slot }}
          </li>
        </ul>
      </div>

      <canvas v-if="resourceResult.length" id="resourceChart" class="chart-canvas"></canvas>

    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from "chart.js";

export default {
  name: 'SchedulingView',
  data() {
    return {
      scheduleTasks: [{ name: '', duration: 0, deadline: 0, priority: 1, earliest_start: 0 }],
      scheduleResult: [],

      resourceTasks: [{ name: '', workload: 0, flexibility: 0 }],
      resourceInput: {
        total_resources: 100,
        total_time: 5
      },
      resourceResult: [],
      scheduleChart: null,
      resourceChart: null
    };
  },
  methods: {
    loadSampleSchedule() {
      this.scheduleTasks = [
        { name: 'Design', duration: 3, deadline: 10, priority: 2, earliest_start: 0 },
        { name: 'Development', duration: 5, deadline: 15, priority: 1, earliest_start: 3 },
        { name: 'Testing', duration: 2, deadline: 18, priority: 3, earliest_start: 10 },
        { name: 'Deployment', duration: 1, deadline: 20, priority: 2, earliest_start: 15 }
      ];
    },
    addScheduleTask() {
      this.scheduleTasks.push({ name: '', duration: 0, deadline: 0, priority: 1, earliest_start: 0 });
    },
    removeScheduleTask(i) {
      this.scheduleTasks.splice(i, 1);
    },
    async runSchedule() {
      try {
        const res = await axios.post('/api/scheduling/optimize', this.scheduleTasks);
        this.scheduleResult = res.data.schedule;
        this.$nextTick(() => this.drawScheduleChart());
        this.$nextTick(() => this.drawGanttChart(this.scheduleResult));
        localStorage.setItem('schedule_result', JSON.stringify(this.scheduleResult));
      } catch (err) {
        alert('Schedule error: ' + err.message);
      }
    },
    drawScheduleChart() {
      const tasks = this.scheduleResult.filter(t => !t.skipped);
      const labels = tasks.map(t => t.name);
      const starts = tasks.map(t => t.start);
      const durations = tasks.map(t => t.end - t.start);

      const ctx = document.getElementById('scheduleChart').getContext('2d');
      if (this.scheduleChart) this.scheduleChart.destroy(); // 避免重叠
      this.scheduleChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Start Time',
            data: starts,
            backgroundColor: '#90caf9'
          }, {
            label: 'Duration',
            data: durations,
            backgroundColor: '#42a5f5'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Task Scheduling (Start + Duration)',
              font: { size: 16 }
            }
          },
          scales: {
            x: {
              stacked: true,
              title: { display: true, text: 'Tasks' }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              title: { display: true, text: 'Time' }
            }
          }
        }
      });
    },

    addResourceTask() {
      this.resourceTasks.push({ name: '', workload: 0, flexibility: 0 });
    },
    removeResourceTask(i) {
      this.resourceTasks.splice(i, 1);
    },
    loadSampleResources() {
      this.resourceTasks = [
        { name: 'UI Implementation', workload: 30, flexibility: 2 },
        { name: 'Backend API', workload: 40, flexibility: 1 },
        { name: 'Database Setup', workload: 20, flexibility: 3 },
        { name: 'Integration', workload: 25, flexibility: 0 }
      ];
      this.resourceInput = {
        total_resources: 100,
        total_time: 5
      };
    },
    async runResourceBalance() {
      try {
        const res = await axios.post('/api/scheduling/smooth', {
          tasks: this.resourceTasks,
          ...this.resourceInput
        });
        this.resourceResult = res.data.allocation;
        localStorage.setItem('resource_result', JSON.stringify(this.resourceResult));
        this.$nextTick(() => this.drawResourceChart());
      } catch (err) {
        alert('Resource balance error: ' + err.message);
      }
    },
    drawResourceChart() {
      const labels = this.resourceResult.map(t => t.name);
      const slots = this.resourceResult.map(t => t.slots.length);
      const perSlot = this.resourceResult.map(t => t.allocated_per_slot);

      const ctx = document.getElementById('resourceChart').getContext('2d');
      if (this.resourceChart) this.resourceChart.destroy();
      this.resourceChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Total Time Slots',
            data: slots,
            backgroundColor: '#81c784'
          }, {
            label: 'Resources per Slot',
            data: perSlot,
            backgroundColor: '#388e3c'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Resource Allocation (Slots & Intensity)',
              font: { size: 16 }
            }
          },
          scales: {
            x: { stacked: true, title: { display: true, text: 'Tasks' } },
            y: { stacked: false, beginAtZero: true, title: { display: true, text: 'Value' } }
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
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.08);
  border: 1px solid #d6e9ff;
}

h2, h3, h4 {
  color: #007BFF;
  font-weight: 600;
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
  margin-bottom: 16px;
}

input {
  width: 200px;
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

label {
  display: inline-block;
  margin: 8px 10px 6px 0;
  font-weight: 500;
}

ul {
  list-style: disc;
  padding-left: 20px;
  color: #333;
}
li {
  margin: 4px 0;
}
</style>
