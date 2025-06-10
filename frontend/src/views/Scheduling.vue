<template>
  <div>
    <h2>Scheduling & Resource Optimization</h2>

    <!-- 任务排布优化 -->
    <section>
      <h3>Task Scheduling</h3>
      <div v-for="(task, i) in scheduleTasks" :key="i">
        <input v-model="task.name" placeholder="Task name" />
        <input v-model.number="task.duration" placeholder="Duration" type="number" />
        <input v-model.number="task.deadline" placeholder="Deadline" type="number" />
        <button @click="removeScheduleTask(i)">Remove</button>
      </div>
      <button @click="addScheduleTask">Add Task</button>
      <button @click="runSchedule">Run Optimization</button>

      <div v-if="scheduleResult.length">
        <h4>Schedule Result:</h4>
        <ul>
          <li v-for="r in scheduleResult" :key="r.name">
            {{ r.name }}:
            <span v-if="r.skipped">Skipped</span>
            <span v-else>Start: {{ r.start }}, End: {{ r.end }}</span>
          </li>
        </ul>
      </div>
    </section>

    <hr />

    <!-- 资源平滑与均衡 -->
    <section>
      <h3>Resource Smoothing</h3>
      <div v-for="(task, i) in resourceTasks" :key="i">
        <input v-model="task.name" placeholder="Task name" />
        <input v-model.number="task.workload" placeholder="Workload" type="number" />
        <button @click="removeResourceTask(i)">Remove</button>
      </div>
      <button @click="addResourceTask">Add Task</button>
      <div>
        <label>Total Resources:</label>
        <input v-model.number="resourceInput.total_resources" type="number" />
        <label>Total Time Slots:</label>
        <input v-model.number="resourceInput.total_time" type="number" />
      </div>
      <button @click="runResourceBalance">Run Smoothing</button>

      <div v-if="resourceResult.length">
        <h4>Allocation Result:</h4>
        <ul>
          <li v-for="r in resourceResult" :key="r.name">
            {{ r.name }} - Time Slots: {{ r.slots }}, Per Slot: {{ r.allocated_per_slot }}
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SchedulingView',
  data() {
    return {
      scheduleTasks: [{ name: '', duration: 0, deadline: 0 }],
      scheduleResult: [],

      resourceTasks: [{ name: '', workload: 0 }],
      resourceInput: {
        total_resources: 100,
        total_time: 5
      },
      resourceResult: []
    };
  },
  methods: {
    addScheduleTask() {
      this.scheduleTasks.push({ name: '', duration: 0, deadline: 0 });
    },
    removeScheduleTask(i) {
      this.scheduleTasks.splice(i, 1);
    },
    async runSchedule() {
      try {
        const res = await axios.post('http://localhost:8000/api/scheduling/optimize', this.scheduleTasks);
        this.scheduleResult = res.data.schedule;
      } catch (err) {
        alert('Schedule error: ' + err.message);
      }
    },

    addResourceTask() {
      this.resourceTasks.push({ name: '', workload: 0 });
    },
    removeResourceTask(i) {
      this.resourceTasks.splice(i, 1);
    },
    async runResourceBalance() {
      try {
        const res = await axios.post('http://localhost:8000/api/scheduling/smooth', {
          tasks: this.resourceTasks,
          ...this.resourceInput
        });
        this.resourceResult = res.data.allocation;
      } catch (err) {
        alert('Resource balance error: ' + err.message);
      }
    }
  }
};
</script>

<style scoped>
section {
  margin-bottom: 32px;
}
input {
  margin: 4px;
}
</style>