<template>
  <div class="analytics-view">
    <!-- Header with Period Selector and Export -->
    <div class="analytics-header">
      <div class="header-left">
        <h1 class="analytics-title">Operational Analytics & Financial Reports</h1>
      </div>
      <div class="header-right">
        <div class="period-selector">
          <button 
            v-for="period in periods" 
            :key="period.value"
            :class="['period-btn', { active: selectedPeriod === period.value }]"
            @click="selectedPeriod = period.value"
          >
            {{ period.label }}
          </button>
        </div>
        <button class="export-btn">
          <span class="btn-icon">📥</span>
          Export Report
          <span class="btn-icon">▼</span>
        </button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <!-- Total Operational Cost -->
      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Total Operational Cost</span>
          <span class="kpi-badge kpi-badge-danger">+{{ stats.costChange }}%</span>
        </div>
        <h3 class="kpi-value">${{ formatNumber(stats.totalCost) }}</h3>
        <div class="cost-breakdown">
          <div class="cost-bar">
            <div class="cost-segment cost-fuel" :style="{ width: stats.fuelPercentage + '%' }"></div>
            <div class="cost-segment cost-maintenance" :style="{ width: stats.maintenancePercentage + '%' }"></div>
          </div>
          <div class="cost-legend">
            <div class="legend-item">
              <span class="legend-dot legend-fuel"></span>
              <span class="legend-text">Fuel: <strong>${{ formatNumber(stats.fuelCost) }}</strong></span>
            </div>
            <div class="legend-item">
              <span class="legend-dot legend-maintenance"></span>
              <span class="legend-text">Maintenance: <strong>${{ formatNumber(stats.maintenanceCost) }}</strong></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Average Vehicle ROI -->
      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Average Vehicle ROI</span>
          <span v-if="stats.avgROI !== 0" class="kpi-badge" :class="stats.avgROI >= 0 ? 'kpi-badge-success' : 'kpi-badge-danger'">
            {{ stats.avgROI >= 0 ? '+' : '' }}{{ stats.roiChange }}%
          </span>
        </div>
        <h3 class="kpi-value" :class="{ 'text-danger': stats.avgROI < 0 }">
          {{ stats.avgROI !== 0 ? stats.avgROI + '%' : '—' }}
        </h3>
        <p class="kpi-description" v-if="stats.avgROI !== 0">
          Return on investment based on acquisition cost. 
          <span v-if="stats.avgROI >= 0">Performance is {{ stats.roiAboveAverage }}% above sector average.</span>
          <span v-else>Vehicles are operating at a loss. Review operational costs.</span>
        </p>
        <p class="kpi-description" v-else>No ROI data available. Complete trips with distance to calculate ROI.</p>
        <div class="roi-details" v-if="stats.avgROI !== 0 && stats.highestROI.name !== '—'">
          <div class="roi-box">
            <p class="roi-box-label">Highest ROI</p>
            <p class="roi-box-value" :class="stats.highestROI.value >= 0 ? 'roi-success' : 'roi-danger'">
              {{ stats.highestROI.name }} ({{ stats.highestROI.value.toFixed(1) }}%)
            </p>
          </div>
          <div class="roi-box">
            <p class="roi-box-label">Lowest ROI</p>
            <p class="roi-box-value" :class="stats.lowestROI.value >= 0 ? 'roi-success' : 'roi-danger'">
              {{ stats.lowestROI.name }} ({{ stats.lowestROI.value.toFixed(1) }}%)
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <!-- Fuel Efficiency Chart -->
      <div class="chart-card chart-large">
        <div class="chart-header">
          <h4 class="chart-title">Fuel Efficiency Trends (km/L)</h4>
          <div class="chart-legend">
            <div class="legend-item">
              <span class="legend-line legend-actual"></span>
              <span>Actual km/L</span>
            </div>
            <div class="legend-item">
              <span class="legend-line legend-target"></span>
              <span class="legend-text-muted">Target</span>
            </div>
          </div>
        </div>
        <div v-if="fuelEfficiencyChartData" class="chart-container">
          <Line :data="fuelEfficiencyChartData" :options="lineChartOptions" />
        </div>
        <div v-else class="chart-placeholder">
          <p class="chart-placeholder-text">No fuel efficiency data available</p>
          <p class="chart-placeholder-subtext">Complete trips with fuel expenses to view efficiency trends</p>
        </div>
      </div>

      <!-- Cost Distribution Chart -->
      <div class="chart-card">
        <h4 class="chart-title">Cost Distribution</h4>
        <div v-if="costDistributionChartData" class="doughnut-chart">
          <Doughnut :data="costDistributionChartData" :options="doughnutChartOptions" />
        </div>
        <div v-else class="chart-placeholder">
          <p class="chart-placeholder-text">No cost data available</p>
        </div>
        <div class="distribution-legend">
          <div class="distribution-item">
            <div class="distribution-row">
              <div class="distribution-left">
                <span class="distribution-dot dot-primary"></span>
                <span class="distribution-label">Fuel</span>
              </div>
              <span class="distribution-value">{{ stats.fuelPercentage.toFixed(0) }}%</span>
            </div>
          </div>
          <div class="distribution-item">
            <div class="distribution-row">
              <div class="distribution-left">
                <span class="distribution-dot dot-success"></span>
                <span class="distribution-label">Maintenance</span>
              </div>
              <span class="distribution-value">{{ stats.maintenancePercentage.toFixed(0) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Financial Performance Table -->
    <div class="table-card">
      <div class="table-header">
        <div class="table-header-left">
          <h4 class="table-title">Financial Performance by Asset</h4>
          <p class="table-subtitle">Detailed ROI and cost breakdown for the current fleet.</p>
        </div>
        <div class="table-header-right">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" v-model="searchQuery" placeholder="Search vehicle..." class="search-input" />
          </div>
          <div class="filter-dropdown">
            <button class="filter-btn" @click="showFilterMenu = !showFilterMenu">
              <span class="btn-icon">⚙</span>
              Filter
              <span class="btn-icon">{{ showFilterMenu ? '▲' : '▼' }}</span>
            </button>
            <div v-if="showFilterMenu" class="filter-menu">
              <button 
                class="filter-menu-item"
                :class="{ active: selectedROIFilter === 'all' }"
                @click="selectedROIFilter = 'all'; showFilterMenu = false"
              >
                All Vehicles
              </button>
              <button 
                class="filter-menu-item"
                :class="{ active: selectedROIFilter === 'high' }"
                @click="selectedROIFilter = 'high'; showFilterMenu = false"
              >
                Excellent (≥15%)
              </button>
              <button 
                class="filter-menu-item"
                :class="{ active: selectedROIFilter === 'stable' }"
                @click="selectedROIFilter = 'stable'; showFilterMenu = false"
              >
                Good (8-15%)
              </button>
              <button 
                class="filter-menu-item"
                :class="{ active: selectedROIFilter === 'warning' }"
                @click="selectedROIFilter = 'warning'; showFilterMenu = false"
              >
                Fair (3-8%)
              </button>
              <button 
                class="filter-menu-item"
                :class="{ active: selectedROIFilter === 'critical' }"
                @click="selectedROIFilter = 'critical'; showFilterMenu = false"
              >
                Poor (<3%)
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="table-wrapper">
        <table class="analytics-table">
          <thead>
            <tr>
              <th>Vehicle ID</th>
              <th>Total Distance</th>
              <th>Fuel Efficiency</th>
              <th>Fuel Cost</th>
              <th>Maintenance</th>
              <th>Revenue</th>
              <th>ROI Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredVehicles.length === 0">
              <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-color-secondary);">
                No vehicle performance data available. Complete trips with distance to see financial performance.
              </td>
            </tr>
            <tr v-for="vehicle in filteredVehicles" :key="vehicle.id" class="table-row-clickable" @click="handleVehicleClick(vehicle.id)">
              <td class="font-medium">{{ vehicle.name }}</td>
              <td>{{ formatNumber(vehicle.distance) }} km</td>
              <td>
                <span v-if="vehicle.fuelEfficiency > 0">{{ vehicle.fuelEfficiency.toFixed(2) }} km/L</span>
                <span v-else class="text-muted">—</span>
              </td>
              <td>${{ formatNumber(vehicle.fuelCost) }}</td>
              <td :class="{ 'text-danger': vehicle.maintenanceCost > 2000 }">
                ${{ formatNumber(vehicle.maintenanceCost) }}
              </td>
              <td class="font-semibold">${{ formatNumber(vehicle.revenue) }}</td>
              <td>
                <span class="roi-badge" :class="`roi-badge-${vehicle.roiStatus}`">
                  <span class="roi-dot"></span>
                  {{ vehicle.roi }}% {{ vehicle.roiLabel }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer">
        <span class="table-footer-text">Showing {{ filteredVehicles.length }} of {{ vehiclePerformance.length }} assets</span>
        <div class="pagination" v-if="vehiclePerformance.length > 10">
          <button class="pagination-btn">‹</button>
          <button class="pagination-btn active">1</button>
          <button class="pagination-btn">2</button>
          <button class="pagination-btn">3</button>
          <button class="pagination-btn">›</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../core/api';
import { Line, Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const router = useRouter();
const searchQuery = ref('');
const selectedPeriod = ref('q3');
const showFilterMenu = ref(false);
const selectedROIFilter = ref('all');

const periods = [
  { label: 'Last 30 Days', value: '30d' },
  { label: 'Q3 2023', value: 'q3' }
];

const stats = ref({
  totalCost: 0,
  fuelCost: 0,
  maintenanceCost: 0,
  fuelPercentage: 0,
  maintenancePercentage: 0,
  costChange: 0,
  avgROI: 0,
  roiChange: 0,
  roiAboveAverage: 0,
  highestROI: { name: '—', value: 0 },
  lowestROI: { name: '—', value: 0 }
});

const vehiclePerformance = ref<any[]>([]);

// Chart data
const fuelEfficiencyChartData = ref<any>(null);
const costDistributionChartData = ref<any>(null);

// Chart options
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top' as const,
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'km/L'
      }
    }
  }
};

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          return context.label + ': $' + context.parsed.toLocaleString();
        }
      }
    }
  }
};

const filteredVehicles = computed(() => {
  let filtered = vehiclePerformance.value;
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(v => 
      v.name.toLowerCase().includes(query)
    );
  }
  
  // Apply ROI filter
  if (selectedROIFilter.value !== 'all') {
    filtered = filtered.filter(v => v.roiStatus === selectedROIFilter.value);
  }
  
  return filtered;
});

const formatNumber = (num: number) => {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

const formatNumberShort = (num: number) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(0) + 'k';
  }
  return num.toString();
};

const handleVehicleClick = (vehicleId: number) => {
  router.push(`/models/fleet.vehicle/${vehicleId}`);
};

const loadAnalyticsData = async () => {
  try {
    console.log('=== ANALYTICS DATA DEBUG ===');
    
    const [vehiclesResponse, expensesResponse] = await Promise.all([
      api.get('/models/fleet.vehicle?limit=100'),
      api.get('/models/fleet.expense?limit=1000')
    ]);

    const vehicles = vehiclesResponse?.data?.items || [];
    const expenses = expensesResponse?.data?.items || [];

    console.log('Fetched data counts:');
    console.log('- Vehicles:', vehicles.length);
    console.log('- Expenses:', expenses.length);
    
    if (vehicles.length > 0) {
      console.log('First vehicle:', vehicles[0]);
      console.log('Vehicle computed fields:', {
        fuel_efficiency: vehicles[0].fuel_efficiency,
        vehicle_roi: vehicles[0].vehicle_roi,
        total_revenue: vehicles[0].total_revenue,
        total_distance: vehicles[0].total_distance,
        total_fuel_cost: vehicles[0].total_fuel_cost,
        total_maintenance_cost: vehicles[0].total_maintenance_cost
      });
    }

    // Calculate total costs from expenses
    const fuelExpenses = expenses.filter((e: any) => e.expense_type === 'fuel');
    const maintenanceExpenses = expenses.filter((e: any) => e.expense_type !== 'fuel');
    
    console.log('Fuel expenses:', fuelExpenses.length);
    console.log('Maintenance expenses:', maintenanceExpenses.length);
    
    stats.value.fuelCost = fuelExpenses.reduce((sum: number, e: any) => sum + (e.cost || 0), 0);
    stats.value.maintenanceCost = maintenanceExpenses.reduce((sum: number, e: any) => sum + (e.cost || 0), 0);
    stats.value.totalCost = stats.value.fuelCost + stats.value.maintenanceCost;
    
    console.log('Total costs - Fuel:', stats.value.fuelCost, 'Maintenance:', stats.value.maintenanceCost);
    
    stats.value.fuelPercentage = stats.value.totalCost > 0 ? (stats.value.fuelCost / stats.value.totalCost) * 100 : 0;
    stats.value.maintenancePercentage = stats.value.totalCost > 0 ? (stats.value.maintenanceCost / stats.value.totalCost) * 100 : 0;
    stats.value.costChange = 12.4; // Mock data
    stats.value.roiChange = 2.1; // Mock data
    stats.value.roiAboveAverage = 5; // Mock data

    // Use computed fields from backend
    console.log('Building vehicle performance data from computed fields...');
    const vehicleData = vehicles.map((v: any) => {
      console.log(`Vehicle ${v.name} (ID: ${v.id}):`);
      console.log('  - Total distance:', v.total_distance);
      console.log('  - Fuel efficiency:', v.fuel_efficiency);
      console.log('  - Vehicle ROI:', v.vehicle_roi);
      console.log('  - Total revenue:', v.total_revenue);
      console.log('  - Fuel cost:', v.total_fuel_cost);
      console.log('  - Maintenance cost:', v.total_maintenance_cost);

      const roi = v.vehicle_roi || 0;
      
      let roiStatus = 'stable';
      let roiLabel = 'Fair';
      if (roi >= 15) {
        roiStatus = 'high';
        roiLabel = 'Excellent';
      } else if (roi >= 8) {
        roiStatus = 'stable';
        roiLabel = 'Good';
      } else if (roi >= 3) {
        roiStatus = 'warning';
        roiLabel = 'Fair';
      } else {
        roiStatus = 'critical';
        roiLabel = 'Poor';
      }

      return {
        id: v.id,
        name: v.name,
        distance: v.total_distance || 0,
        fuelCost: v.total_fuel_cost || 0,
        maintenanceCost: v.total_maintenance_cost || 0,
        revenue: v.total_revenue || 0,
        roi: roi.toFixed(1),
        roiStatus: roiStatus,
        roiLabel: roiLabel,
        fuelEfficiency: v.fuel_efficiency || 0
      };
    });
    
    console.log('Vehicle data:', vehicleData);
    
    vehiclePerformance.value = vehicleData.sort((a: any, b: any) => parseFloat(b.roi) - parseFloat(a.roi));

    console.log('Final vehicle performance array:', vehiclePerformance.value);

    // Calculate average ROI
    const vehiclesWithData = vehicleData.filter((v: any) => v.distance > 0 || v.fuelCost > 0 || v.maintenanceCost > 0);
    
    if (vehiclesWithData.length > 0) {
      const totalROI = vehiclesWithData.reduce((sum: number, v: any) => sum + parseFloat(v.roi), 0);
      stats.value.avgROI = parseFloat((totalROI / vehiclesWithData.length).toFixed(1));
      
      // Sort by ROI to get highest and lowest
      const sortedByROI = [...vehiclesWithData].sort((a: any, b: any) => parseFloat(b.roi) - parseFloat(a.roi));
      
      stats.value.highestROI = {
        name: sortedByROI[0]?.name || '—',
        value: parseFloat(sortedByROI[0]?.roi || 0)
      };
      
      stats.value.lowestROI = {
        name: sortedByROI[sortedByROI.length - 1]?.name || '—',
        value: parseFloat(sortedByROI[sortedByROI.length - 1]?.roi || 0)
      };
      
      console.log('ROI stats:', {
        avgROI: stats.value.avgROI,
        highestROI: stats.value.highestROI,
        lowestROI: stats.value.lowestROI,
        vehiclesWithData: vehiclesWithData.length
      });
    } else {
      console.log('No vehicle data available for ROI calculation');
    }

    // Create Fuel Efficiency Chart Data
    const vehiclesWithEfficiency = vehicleData.filter((v: any) => v.fuelEfficiency > 0);
    if (vehiclesWithEfficiency.length > 0) {
      fuelEfficiencyChartData.value = {
        labels: vehiclesWithEfficiency.map((v: any) => v.name),
        datasets: [
          {
            label: 'Actual km/L',
            data: vehiclesWithEfficiency.map((v: any) => v.fuelEfficiency),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'Target (10 km/L)',
            data: vehiclesWithEfficiency.map(() => 10),
            borderColor: '#94a3b8',
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0
          }
        ]
      };
    }

    // Create Cost Distribution Chart Data
    if (stats.value.totalCost > 0) {
      costDistributionChartData.value = {
        labels: ['Fuel', 'Maintenance'],
        datasets: [{
          data: [stats.value.fuelCost, stats.value.maintenanceCost],
          backgroundColor: ['#3b82f6', '#10b981'],
          borderWidth: 0
        }]
      };
    }

    console.log('=== END ANALYTICS DEBUG ===');

  } catch (error) {
    console.error('Error loading analytics:', error);
  }
};

onMounted(() => {
  loadAnalyticsData();
});
</script>

<style scoped lang="scss">
@use "../styles/variables" as v;

.analytics-view {
  width: 100%;
  height: 100%;
  padding: 2rem;
  background: v.$bg-main;
  color: v.$text-primary;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Header */
.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-left {
  flex: 1;
  min-width: 0;
}

.analytics-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: v.$text-primary;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.period-selector {
  display: flex;
  background: v.$bg-secondary;
  border-radius: v.$radius-md;
  padding: 0.25rem;
  gap: 0.25rem;
}

.period-btn {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  background: transparent;
  color: v.$text-secondary;
  border-radius: v.$radius-sm;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn.active {
  background: v.$white;
  color: v.$primary-color;
  box-shadow: v.$shadow-sm;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: v.$primary-color;
  color: v.$white;
  border: none;
  border-radius: v.$radius-btn;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: v.$primary-hover;
}

.btn-icon {
  font-size: 0.875rem;
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.kpi-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  padding: 1.5rem;
  box-shadow: v.$shadow-sm;
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.kpi-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: v.$text-secondary;
}

.kpi-badge {
  padding: 0.25rem 0.5rem;
  border-radius: v.$radius-pill;
  font-size: 0.75rem;
  font-weight: 700;
}

.kpi-badge-danger {
  background: v.$danger-bg;
  color: v.$danger-color;
}

.kpi-badge-success {
  background: v.$success-bg;
  color: v.$success-color;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
  color: v.$text-primary;
}

.kpi-description {
  font-size: 0.875rem;
  color: v.$text-secondary;
  margin: 0.5rem 0 1rem;
}

.cost-breakdown {
  margin-top: 1.5rem;
}

.cost-bar {
  display: flex;
  height: 0.5rem;
  background: v.$bg-secondary;
  border-radius: v.$radius-pill;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.cost-segment {
  height: 100%;
}

.cost-fuel {
  background: v.$primary-color;
}

.cost-maintenance {
  background: v.$success-color;
}

.cost-legend {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.legend-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

.legend-fuel {
  background: v.$primary-color;
}

.legend-maintenance {
  background: v.$success-color;
}

.legend-text {
  color: v.$text-secondary;
}

.legend-text strong {
  color: v.$text-primary;
}

.roi-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.roi-box {
  background: v.$bg-secondary;
  padding: 0.75rem;
  border-radius: v.$radius-md;
  border: 1px solid v.$border-color;
}

.roi-box-label {
  font-size: 0.625rem;
  text-transform: uppercase;
  font-weight: 700;
  color: v.$text-tertiary;
  margin: 0 0 0.25rem 0;
}

.roi-box-value {
  font-size: 0.875rem;
  font-weight: 700;
  margin: 0;
}

.roi-success {
  color: v.$success-color;
}

.roi-danger {
  color: v.$danger-color;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  padding: 1.5rem;
  box-shadow: v.$shadow-sm;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: v.$text-primary;
}

.chart-legend {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
}

.legend-line {
  display: inline-block;
  width: 1rem;
  height: 2px;
}

.legend-actual {
  background: v.$primary-color;
}

.legend-target {
  border-top: 2px dashed v.$text-tertiary;
}

.legend-text-muted {
  color: v.$text-tertiary;
}

.chart-placeholder {
  height: 16rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: v.$bg-secondary;
  border-radius: v.$radius-md;
  border: 2px dashed v.$border-color;
}

.chart-container {
  height: 16rem;
  position: relative;
}

.chart-placeholder-text {
  font-size: 1rem;
  font-weight: 600;
  color: v.$text-secondary;
  margin: 0;
}

.chart-placeholder-subtext {
  font-size: 0.75rem;
  color: v.$text-tertiary;
  margin: 0.5rem 0 0 0;
}

.doughnut-chart {
  height: 16rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  position: relative;
}

.distribution-legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.distribution-item {
  font-size: 0.75rem;
}

.distribution-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.distribution-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.distribution-dot {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: v.$radius-sm;
}

.dot-primary {
  background: v.$primary-color;
}

.dot-success {
  background: v.$success-color;
}

.dot-warning {
  background: v.$warning-color;
}

.dot-neutral {
  background: v.$bg-secondary;
}

.distribution-label {
  color: v.$text-secondary;
}

.distribution-value {
  font-weight: 700;
  color: v.$text-primary;
}

/* Table */
.table-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  box-shadow: v.$shadow-sm;
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid v.$border-color;
  gap: 1rem;
  flex-wrap: wrap;
}

.table-header-left {
  flex: 1;
  min-width: 0;
}

.table-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: v.$text-primary;
}

.table-subtitle {
  font-size: 0.75rem;
  color: v.$text-secondary;
  margin: 0;
}

.table-header-right {
  display: flex;
  gap: 0.5rem;
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 0.625rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.875rem;
  color: v.$text-tertiary;
}

.search-input {
  padding: 0.5rem 0.75rem 0.5rem 2rem;
  font-size: 0.75rem;
  background: v.$bg-secondary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-btn;
  color: v.$text-primary;
  width: 12rem;
}

.search-input:focus {
  outline: none;
  border-color: v.$primary-color;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  background: v.$bg-secondary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-btn;
  color: v.$text-primary;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: v.$bg-tertiary;
}

.filter-dropdown {
  position: relative;
}

.filter-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  box-shadow: v.$shadow-lg;
  min-width: 200px;
  z-index: 100;
  overflow: hidden;
}

.filter-menu-item {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  background: transparent;
  border: none;
  color: v.$text-primary;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 1px solid v.$border-color;
}

.filter-menu-item:last-child {
  border-bottom: none;
}

.filter-menu-item:hover {
  background: v.$bg-secondary;
}

.filter-menu-item.active {
  background: v.$primary-color;
  color: v.$white;
  font-weight: 600;
}

.table-wrapper {
  overflow-x: auto;
}

.analytics-table {
  width: 100%;
  border-collapse: collapse;
}

.analytics-table thead {
  background: v.$table-header-bg;
  border-bottom: 1px solid v.$border-color;
}

.analytics-table th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: v.$text-secondary;
}

.analytics-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid v.$border-color;
  font-size: 0.875rem;
  color: v.$text-primary;
}

.analytics-table tbody tr {
  transition: background 0.2s;
}

.table-row-clickable {
  cursor: pointer;
}

.analytics-table tbody tr:hover {
  background: v.$table-hover;
}

.text-right {
  text-align: right;
}

.font-medium {
  font-weight: 500;
}

.font-semibold {
  font-weight: 600;
}

.text-danger {
  color: v.$danger-color;
  font-weight: 700;
}

.text-muted {
  color: v.$text-tertiary;
}

.roi-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.5rem;
  border-radius: v.$radius-sm;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
}

.roi-badge-high {
  background: v.$success-bg;
  color: v.$success-color;
}

.roi-badge-stable {
  background: v.$info-bg;
  color: v.$primary-color;
}

.roi-badge-warning {
  background: v.$warning-bg;
  color: v.$warning-color;
}

.roi-badge-critical {
  background: v.$danger-bg;
  color: v.$danger-color;
}

.roi-dot {
  width: 0.25rem;
  height: 0.25rem;
  border-radius: 50%;
  background: currentColor;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: v.$bg-secondary;
  border-top: 1px solid v.$border-color;
}

.table-footer-text {
  font-size: 0.75rem;
  color: v.$text-secondary;
}

.pagination {
  display: flex;
  gap: 0.25rem;
}

.pagination-btn {
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  border: none;
  background: transparent;
  color: v.$text-primary;
  border-radius: v.$radius-sm;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover {
  background: v.$bg-tertiary;
}

.pagination-btn.active {
  background: v.$primary-color;
  color: v.$white;
  font-weight: 700;
}

/* Dark Mode */
[data-theme="dark"] {
  .kpi-card,
  .chart-card,
  .table-card {
    background: #161b22;
    border-color: #30363d;
  }

  .table-header,
  .table-footer {
    background: #0d1117;
    border-color: #30363d;
  }

  .analytics-table thead {
    background: #0d1117;
    border-color: #30363d;
  }

  .analytics-table td {
    border-color: #21262d;
  }

  .analytics-table tbody tr:hover {
    background: #21262d;
  }

  .period-btn.active {
    background: #21262d;
  }

  .doughnut-center {
    background: #161b22;
  }

  .chart-placeholder {
    background: #0d1117;
  }

  .filter-menu {
    background: #161b22;
    border-color: #30363d;
  }

  .filter-menu-item {
    color: #c9d1d9;
    border-color: #30363d;
  }

  .filter-menu-item:hover {
    background: #21262d;
  }

  .filter-menu-item.active {
    background: v.$primary-color;
    color: v.$white;
  }
}
</style>
