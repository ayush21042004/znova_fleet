<template>
  <div class="command-center">
    <!-- Header -->
    <div class="cc-header">
      <div class="cc-header-content">
        <h1 class="cc-title">Command Center</h1>
        <p class="cc-subtitle">Real-time fleet oversight and operational metrics</p>
      </div>
      <button class="cc-btn-primary" @click="handleNewDispatch">
        <span class="cc-btn-icon">+</span>
        New Dispatch
      </button>
    </div>

    <!-- KPI Cards -->
    <div class="cc-kpi-grid">
      <!-- Active Fleet -->
      <div class="cc-kpi-card cc-kpi-card-clickable" @click="handleKpiClick('fleet.vehicle', 'in_use')">
        <div class="cc-kpi-left">
          <span class="cc-kpi-label">Active Fleet</span>
          <div class="cc-kpi-value-group">
            <span class="cc-kpi-value">{{ stats.activeFleet }}</span>
            <span class="cc-kpi-total">/ {{ stats.totalFleet }} units</span>
          </div>
          <span class="cc-kpi-trend cc-trend-up">
            ↑ {{ stats.utilizationRate }}% utilization
          </span>
        </div>
        <div class="cc-kpi-right">
          <div class="cc-progress-circle">
            <svg width="64" height="64" viewBox="0 0 64 64">
              <circle cx="32" cy="32" r="28" class="cc-progress-bg" />
              <circle 
                cx="32" cy="32" r="28" 
                class="cc-progress-bar"
                :style="{ strokeDashoffset: 175.9 - (175.9 * stats.utilizationRate / 100) }"
              />
            </svg>
            <span class="cc-progress-text">{{ stats.utilizationRate }}%</span>
          </div>
        </div>
      </div>

      <!-- Maintenance Alerts -->
      <div class="cc-kpi-card cc-kpi-card-clickable" @click="handleKpiClick('fleet.vehicle', 'in_shop')">
        <div class="cc-kpi-left">
          <span class="cc-kpi-label">Maintenance Alerts</span>
          <span class="cc-kpi-value">{{ stats.maintenanceAlerts }}</span>
          <span class="cc-kpi-status cc-status-warning">
            {{ stats.maintenanceAlerts > 0 ? 'ACTION REQUIRED' : 'ALL CLEAR' }}
          </span>
        </div>
        <div class="cc-kpi-icon cc-icon-warning">⚠</div>
      </div>

      <!-- Trips Today -->
      <div class="cc-kpi-card cc-kpi-card-clickable" @click="handleKpiClick('fleet.trip', 'in_progress')">
        <div class="cc-kpi-left">
          <span class="cc-kpi-label">Trips Today</span>
          <span class="cc-kpi-value">{{ stats.tripsToday }}</span>
          <div class="cc-kpi-meta">
            <span class="cc-meta-success">{{ stats.completedTrips }} completed</span>
            <span class="cc-meta-sep">•</span>
            <span class="cc-meta-primary">{{ stats.activeTrips }} active</span>
          </div>
        </div>
        <div class="cc-kpi-icon cc-icon-primary">🚚</div>
      </div>

      <!-- Pending Cargo -->
      <div class="cc-kpi-card cc-kpi-card-clickable" @click="handleKpiClick('fleet.trip', 'draft')">
        <div class="cc-kpi-left">
          <span class="cc-kpi-label">Pending Cargo</span>
          <span class="cc-kpi-value">{{ stats.pendingCargo }}</span>
          <span class="cc-kpi-meta">
            <span class="cc-meta-secondary">Awaiting dispatch</span>
          </span>
        </div>
        <div class="cc-kpi-icon cc-icon-neutral">📦</div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="cc-main-grid">
      <!-- Active Trips Table -->
      <div class="cc-card cc-table-card">
        <div class="cc-card-header">
          <div class="cc-card-title-group">
            <span class="cc-card-icon">📡</span>
            <h3 class="cc-card-title">Active Trips</h3>
          </div>
          <div class="cc-card-actions">
            <button class="cc-btn-secondary" @click="toggleFilter">
              <span class="btn-icon">🔍</span>
              Filter
            </button>
          </div>
        </div>
        
        <!-- Filter Bar -->
        <div v-if="showFilter" class="cc-filter-bar">
          <button 
            v-for="filter in tripFilters" 
            :key="filter.value"
            class="cc-filter-chip"
            :class="{ active: activeFilter === filter.value }"
            @click="applyFilter(filter.value)"
          >
            {{ filter.label }}
          </button>
        </div>
        
        <div class="cc-table-wrapper">
          <table class="cc-table">
            <thead>
              <tr>
                <th>TRIP</th>
                <th>VEHICLE</th>
                <th>DRIVER</th>
                <th>ROUTE</th>
                <th>STATUS</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="trip in filteredTrips" 
                :key="trip.id"
                @click="handleTripClick(trip.id)"
                class="cc-table-row-clickable"
              >
                <td>
                  <div class="cc-vehicle-cell">
                    <span class="cc-vehicle-icon">📦</span>
                    <strong>{{ trip.name }}</strong>
                  </div>
                </td>
                <td class="cc-text-secondary">{{ trip.vehicle || '—' }}</td>
                <td class="cc-text-secondary">{{ trip.driver || '—' }}</td>
                <td class="cc-text-secondary">{{ trip.route }}</td>
                <td>
                  <span class="cc-badge" :class="`cc-badge-${trip.status}`">
                    {{ formatTripStatus(trip.status) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="cc-card-footer">
          <span class="cc-footer-text">Showing {{ filteredTrips.length }} of {{ allTrips.length }} trips</span>
          <router-link to="/models/fleet.trip" class="cc-footer-link">View All →</router-link>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="cc-sidebar">
        <!-- Fleet Distribution -->
        <div class="cc-card">
          <div class="cc-card-header">
            <h3 class="cc-card-title">Fleet Distribution</h3>
            <span class="cc-card-icon">📊</span>
          </div>
          
          <div class="cc-card-body">
            <div class="cc-dist-list">
              <div v-for="status in statusDistribution" :key="status.name" class="cc-dist-item">
                <div class="cc-dist-header">
                  <span class="cc-dist-label">{{ status.name }}</span>
                  <span class="cc-dist-value">{{ status.count }} Units</span>
                </div>
                <div class="cc-progress-bar-wrapper">
                  <div 
                    class="cc-progress-bar-fill" 
                    :class="`cc-progress-${status.name.toLowerCase().replace(' ', '-')}`"
                    :style="{ width: status.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="cc-stats-grid">
              <div class="cc-stat">
                <div class="cc-stat-value">{{ stats.avgMilesPerDay }}</div>
                <div class="cc-stat-label">AVG MILES/DAY</div>
              </div>
              <div class="cc-stat-divider"></div>
              <div class="cc-stat">
                <div class="cc-stat-value">{{ stats.onTimeRate }}%</div>
                <div class="cc-stat-label">ON-TIME RATE</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Vehicle Type Distribution -->
        <div class="cc-card">
          <div class="cc-card-header">
            <h3 class="cc-card-title">By Vehicle Type</h3>
            <span class="cc-card-icon">🚛</span>
          </div>
          
          <div class="cc-card-body">
            <div class="cc-dist-list">
              <div v-for="type in vehicleTypeDistribution" :key="type.name" class="cc-dist-item">
                <div class="cc-dist-header">
                  <span class="cc-dist-label">{{ type.name }}</span>
                  <span class="cc-dist-value">{{ type.count }} Units</span>
                </div>
                <div class="cc-progress-bar-wrapper">
                  <div 
                    class="cc-progress-bar-fill" 
                    :class="`cc-progress-${type.name.toLowerCase()}`"
                    :style="{ width: type.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Region Distribution -->
        <div class="cc-card">
          <div class="cc-card-header">
            <h3 class="cc-card-title">By Region</h3>
            <span class="cc-card-icon">🗺️</span>
          </div>
          
          <div class="cc-card-body">
            <div class="cc-dist-list">
              <div v-for="region in regionDistribution" :key="region.name" class="cc-dist-item">
                <div class="cc-dist-header">
                  <span class="cc-dist-label">{{ region.name }}</span>
                  <span class="cc-dist-value">{{ region.count }} Units</span>
                </div>
                <div class="cc-progress-bar-wrapper">
                  <div 
                    class="cc-progress-bar-fill" 
                    :class="`cc-progress-${region.name.toLowerCase()}`"
                    :style="{ width: region.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="cc-card">
          <div class="cc-card-header">
            <h3 class="cc-card-title">Quick Actions</h3>
          </div>
          <div class="cc-card-body">
            <div class="cc-actions-list">
              <a href="#" @click.prevent="handleQuickAction('fleet.vehicle')" class="cc-action">
                <div class="cc-action-icon cc-action-primary">🚛</div>
                <div class="cc-action-content">
                  <div class="cc-action-title">Add Vehicle</div>
                  <div class="cc-action-desc">Register new vehicle</div>
                </div>
                <span class="cc-action-arrow">›</span>
              </a>

              <a href="#" @click.prevent="handleQuickAction('fleet.maintenance.log')" class="cc-action">
                <div class="cc-action-icon cc-action-warning">🔧</div>
                <div class="cc-action-content">
                  <div class="cc-action-title">Log Maintenance</div>
                  <div class="cc-action-desc">Record service</div>
                </div>
                <span class="cc-action-arrow">›</span>
              </a>

              <a href="#" @click.prevent="handleQuickAction('fleet.expense')" class="cc-action">
                <div class="cc-action-icon cc-action-success">💰</div>
                <div class="cc-action-content">
                  <div class="cc-action-title">Add Expense</div>
                  <div class="cc-action-desc">Track costs</div>
                </div>
                <span class="cc-action-arrow">›</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../core/api';

const router = useRouter();

const stats = ref({
  activeFleet: 0,
  totalFleet: 0,
  utilizationRate: 0,
  maintenanceAlerts: 0,
  tripsToday: 0,
  completedTrips: 0,
  activeTrips: 0,
  pendingCargo: 0,
  avgMilesPerDay: 0,
  onTimeRate: 0
});

const allTrips = ref<any[]>([]);
const showFilter = ref(false);
const activeFilter = ref('all');

const tripFilters = [
  { label: 'All', value: 'all' },
  { label: 'Draft', value: 'draft' },
  { label: 'Dispatched', value: 'dispatched' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' }
];

const filteredTrips = computed(() => {
  if (activeFilter.value === 'all') {
    return allTrips.value.slice(0, 5);
  }
  return allTrips.value.filter(t => t.status === activeFilter.value).slice(0, 5);
});

const toggleFilter = () => {
  showFilter.value = !showFilter.value;
};

const applyFilter = (filterValue: string) => {
  activeFilter.value = filterValue;
};

const handleNewDispatch = () => {
  router.push('/models/fleet.trip/new');
};

const handleTripClick = (tripId: number) => {
  router.push(`/models/fleet.trip/${tripId}`);
};

const handleKpiClick = (model: string, filterName: string) => {
  // Navigate to the model list with a filter applied
  // The filter array format matches what GenericView expects
  const filters = [filterName];
  
  router.push({
    path: `/models/${model}`,
    query: { 
      filters: JSON.stringify(filters)
    }
  });
};

const handleQuickAction = (model: string) => {
  // Navigate directly to the new record form
  router.push(`/models/${model}/new`);
};

const statusDistribution = computed(() => {
  const total = stats.value.totalFleet || 1;
  return [
    { 
      name: 'Available', 
      count: stats.value.totalFleet - stats.value.activeFleet - stats.value.maintenanceAlerts,
      percentage: ((stats.value.totalFleet - stats.value.activeFleet - stats.value.maintenanceAlerts) / total) * 100
    },
    { 
      name: 'In Use', 
      count: stats.value.activeFleet,
      percentage: (stats.value.activeFleet / total) * 100
    },
    { 
      name: 'In Shop', 
      count: stats.value.maintenanceAlerts,
      percentage: (stats.value.maintenanceAlerts / total) * 100
    }
  ];
});

const allVehicles = ref<any[]>([]);

const vehicleTypeDistribution = computed(() => {
  const total = allVehicles.value.length || 1;
  const trucks = allVehicles.value.filter((v: any) => v.vehicle_type === 'truck').length;
  const vans = allVehicles.value.filter((v: any) => v.vehicle_type === 'van').length;
  const bikes = allVehicles.value.filter((v: any) => v.vehicle_type === 'bike').length;
  
  return [
    { name: 'Truck', count: trucks, percentage: (trucks / total) * 100 },
    { name: 'Van', count: vans, percentage: (vans / total) * 100 },
    { name: 'Bike', count: bikes, percentage: (bikes / total) * 100 }
  ].filter(item => item.count > 0);
});

const regionDistribution = computed(() => {
  const total = allVehicles.value.length || 1;
  const north = allVehicles.value.filter((v: any) => v.region === 'north').length;
  const south = allVehicles.value.filter((v: any) => v.region === 'south').length;
  const east = allVehicles.value.filter((v: any) => v.region === 'east').length;
  const west = allVehicles.value.filter((v: any) => v.region === 'west').length;
  const central = allVehicles.value.filter((v: any) => v.region === 'central').length;
  
  return [
    { name: 'North', count: north, percentage: (north / total) * 100 },
    { name: 'South', count: south, percentage: (south / total) * 100 },
    { name: 'East', count: east, percentage: (east / total) * 100 },
    { name: 'West', count: west, percentage: (west / total) * 100 },
    { name: 'Central', count: central, percentage: (central / total) * 100 }
  ].filter(item => item.count > 0);
});

const formatTripStatus = (status: string) => {
  const map: Record<string, string> = {
    'draft': 'DRAFT',
    'dispatched': 'DISPATCHED',
    'in_progress': 'IN PROGRESS',
    'completed': 'COMPLETED',
    'cancelled': 'CANCELLED'
  };
  return map[status] || status.toUpperCase();
};

const loadDashboardData = async () => {
  try {
    const [vehiclesResponse, tripsResponse] = await Promise.all([
      api.get('/models/fleet.vehicle?limit=100'),
      api.get('/models/fleet.trip?limit=100')
    ]);

    const vehicles = vehiclesResponse?.data?.items || [];
    const trips = tripsResponse?.data?.items || [];

    // Store vehicles for distribution calculations
    allVehicles.value = vehicles;

    // Debug logging
    console.log('=== DASHBOARD DATA DEBUG ===');
    console.log('Raw trips data:', trips);
    if (trips.length > 0) {
      console.log('First trip sample:', trips[0]);
      console.log('First trip vehicle_id:', trips[0].vehicle_id);
      console.log('First trip driver_id:', trips[0].driver_id);
      console.log('vehicle_id type:', typeof trips[0].vehicle_id);
      console.log('driver_id type:', typeof trips[0].driver_id);
      console.log('vehicle_id is array?', Array.isArray(trips[0].vehicle_id));
      console.log('driver_id is array?', Array.isArray(trips[0].driver_id));
    }

    stats.value.totalFleet = vehicles.length;
    stats.value.activeFleet = vehicles.filter((v: any) => v.status === 'in_use').length;
    stats.value.maintenanceAlerts = vehicles.filter((v: any) => v.status === 'in_shop').length;
    stats.value.utilizationRate = stats.value.totalFleet > 0 
      ? Math.round((stats.value.activeFleet / stats.value.totalFleet) * 100) 
      : 0;

    const today = new Date().toISOString().split('T')[0];
    stats.value.tripsToday = trips.filter((t: any) => t.scheduled_date?.startsWith(today)).length;
    stats.value.completedTrips = trips.filter((t: any) => t.status === 'completed').length;
    stats.value.activeTrips = trips.filter((t: any) => ['dispatched', 'in_progress'].includes(t.status)).length;
    stats.value.pendingCargo = trips.filter((t: any) => t.status === 'draft').length;

    // Calculate average miles per day from completed trips
    const completedTripsWithDistance = trips.filter((t: any) => 
      t.status === 'completed' && t.distance && t.start_time && t.end_time
    );
    
    if (completedTripsWithDistance.length > 0) {
      const totalDistance = completedTripsWithDistance.reduce((sum: number, t: any) => sum + (t.distance || 0), 0);
      const totalDays = completedTripsWithDistance.reduce((sum: number, t: any) => {
        const start = new Date(t.start_time);
        const end = new Date(t.end_time);
        const days = Math.max(1, Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)));
        return sum + days;
      }, 0);
      stats.value.avgMilesPerDay = Math.round(totalDistance / totalDays);
    } else {
      stats.value.avgMilesPerDay = 0;
    }

    // Calculate on-time rate from completed trips
    const completedTripsWithSchedule = trips.filter((t: any) => 
      t.status === 'completed' && t.scheduled_date && t.end_time
    );
    
    if (completedTripsWithSchedule.length > 0) {
      const onTimeTrips = completedTripsWithSchedule.filter((t: any) => {
        const scheduled = new Date(t.scheduled_date);
        const completed = new Date(t.end_time);
        // Consider on-time if completed within 24 hours of scheduled date
        const diffHours = (completed.getTime() - scheduled.getTime()) / (1000 * 60 * 60);
        return diffHours <= 24;
      }).length;
      stats.value.onTimeRate = Math.round((onTimeTrips / completedTripsWithSchedule.length) * 100);
    } else {
      stats.value.onTimeRate = 0;
    }

    allTrips.value = trips.map((t: any) => {
      // Handle Many2one fields - API returns {id: X, display_name: "Name"}
      
      let vehicleName = '—';
      if (typeof t.vehicle_id === 'object' && t.vehicle_id !== null) {
        vehicleName = t.vehicle_id.display_name || t.vehicle_id.name || '—';
      } else if (typeof t.vehicle_id === 'string') {
        vehicleName = t.vehicle_id;
      }
      
      let driverName = '—';
      if (typeof t.driver_id === 'object' && t.driver_id !== null) {
        driverName = t.driver_id.display_name || t.driver_id.name || '—';
      } else if (typeof t.driver_id === 'string') {
        driverName = t.driver_id;
      }

      const mappedTrip = {
        id: t.id,
        name: t.name,
        vehicle: vehicleName,
        driver: driverName,
        route: `${t.origin || '—'} → ${t.destination || '—'}`,
        status: t.status
      };
      
      console.log('Mapped trip:', mappedTrip);
      return mappedTrip;
    });
    
    console.log('Final allTrips:', allTrips.value);
    console.log('=== END DEBUG ===');
  } catch (error) {
    console.error('Error loading dashboard:', error);
  }
};

onMounted(() => {
  loadDashboardData();
});
</script>

<style scoped lang="scss">
@use "../styles/variables" as v;

.command-center {
  width: 100%;
  height: 100%;
  padding: 2rem;
  background: v.$bg-main;
  color: v.$text-primary;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Header */
.cc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.cc-header-content {
  flex: 1;
}

.cc-title {
  font-size: 1.875rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.cc-subtitle {
  font-size: 0.875rem;
  color: var(--text-color-secondary);
  margin: 0;
}

.cc-btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: v.$primary-color;
  color: v.$white;
  border-radius: v.$radius-btn;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 2px v.$shadow-light;
}

.cc-btn-primary:hover {
  background: v.$primary-hover;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px v.$shadow-medium;
}

.cc-btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px v.$shadow-light;
}

.cc-btn-icon {
  font-size: 1.25rem;
  line-height: 1;
}

/* KPI Grid */
.cc-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.cc-kpi-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  transition: all 0.2s;
  box-shadow: v.$shadow-sm;
  min-height: 120px;
}

.cc-kpi-card-clickable {
  cursor: pointer;
}

.cc-kpi-card-clickable:hover {
  border-color: v.$primary-color;
  box-shadow: v.$shadow-md;
  transform: translateY(-2px);
}

.cc-kpi-card:hover {
  border-color: v.$border-light;
  box-shadow: v.$shadow-md;
}

.cc-alert-card {
  border-left: 4px solid v.$warning-color;
}

.cc-kpi-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.cc-kpi-label {
  display: block;
  font-size: 0.875rem;
  color: v.$text-secondary;
  font-weight: 500;
  line-height: 1.2;
}

.cc-kpi-value-group {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.cc-kpi-value {
  font-size: 2rem;
  font-weight: 700;
  color: v.$text-primary;
  line-height: 1;
}

.cc-kpi-total {
  font-size: 0.875rem;
  color: v.$text-secondary;
  line-height: 1.2;
}

.cc-kpi-trend {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.2;
}

.cc-trend-up {
  color: v.$success-color;
}

.cc-kpi-status {
  display: inline-block;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  line-height: 1.2;
}

.cc-status-warning {
  color: v.$warning-color;
}

.cc-kpi-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  flex-wrap: wrap;
  line-height: 1.2;
}

.cc-meta-success {
  color: v.$success-color;
  font-weight: 600;
}

.cc-meta-primary {
  color: v.$primary-color;
  font-weight: 600;
}

.cc-meta-secondary {
  color: v.$text-secondary;
  font-weight: 500;
}

.cc-meta-sep {
  color: v.$text-tertiary;
}

.cc-kpi-link {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  color: v.$link-color;
  text-decoration: none;
  line-height: 1.2;
}

.cc-kpi-link:hover {
  text-decoration: underline;
  color: v.$link-hover;
}

.cc-kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: v.$radius-md;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.cc-icon-primary {
  background: v.$info-bg;
}

.cc-icon-warning {
  background: v.$warning-bg;
}

.cc-icon-success {
  background: v.$success-bg;
}

.cc-icon-neutral {
  background: v.$bg-secondary;
}

.cc-kpi-right {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.cc-icon-neutral {
  background: rgba(148, 163, 184, 0.1);
}

.cc-kpi-right {
  flex-shrink: 0;
}

.cc-progress-circle {
  position: relative;
  width: 64px;
  height: 64px;
}

.cc-progress-circle svg {
  transform: rotate(-90deg);
}

.cc-progress-bg {
  fill: none;
  stroke: rgba(51, 65, 85, 0.8);
  stroke-width: 4;
}

.cc-progress-bar {
  fill: none;
  stroke: var(--primary-color);
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 175.9;
  transition: stroke-dashoffset 0.5s ease;
}

.cc-progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
}

/* Main Grid */
.cc-main-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 1.5rem;
}

@media (max-width: 1280px) {
  .cc-main-grid {
    grid-template-columns: 1fr;
  }
}

.cc-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-md;
  overflow: hidden;
  box-shadow: v.$shadow-sm;
}

.cc-table-card {
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.cc-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid v.$border-color;
  background: v.$bg-secondary;
}

.cc-card-title-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cc-card-icon {
  font-size: 1.25rem;
}

.cc-card-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-color);
}

.cc-card-actions {
  display: flex;
  gap: 0.5rem;
}

.cc-btn-secondary {
  padding: 0.5rem 1rem;
  background: v.$bg-main;
  color: v.$text-primary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-btn;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cc-btn-secondary:hover {
  background: v.$bg-secondary;
  border-color: v.$border-light;
}

.btn-icon {
  font-size: 1rem;
}

/* Filter Bar */
.cc-filter-bar {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid v.$border-color;
  background: v.$bg-secondary;
  flex-wrap: wrap;
}

.cc-filter-chip {
  padding: 0.375rem 0.875rem;
  background: v.$bg-main;
  color: v.$text-secondary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-pill;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cc-filter-chip:hover {
  background: v.$bg-secondary;
  color: v.$text-primary;
}

.cc-filter-chip.active {
  background: v.$primary-color;
  color: v.$white;
  border-color: v.$primary-color;
}

.cc-table-wrapper {
  flex: 1;
  overflow-x: auto;
}

.cc-table {
  width: 100%;
  border-collapse: collapse;
}

.cc-table thead {
  background: v.$table-header-bg;
  border-bottom: 1px solid v.$border-color;
}

.cc-table th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

.cc-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
  color: var(--text-color);
  font-size: 0.875rem;
}

.cc-table tbody tr {
  transition: background 0.2s;
}

.cc-table-row-clickable {
  cursor: pointer;
}

.cc-table tbody tr:hover {
  background: v.$table-hover;
}

.cc-vehicle-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cc-vehicle-icon {
  font-size: 1.25rem;
}

.cc-text-secondary {
  color: #94a3b8;
}

.cc-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid;
}

.cc-badge-draft {
  background: v.$info-bg;
  color: v.$info-color;
  border-color: v.$info-border;
}

.cc-badge-dispatched {
  background: v.$info-bg;
  color: v.$primary-color;
  border-color: v.$info-border;
}

.cc-badge-in_progress {
  background: v.$warning-bg;
  color: v.$warning-color;
  border-color: v.$warning-border;
}

.cc-badge-completed {
  background: v.$success-bg;
  color: v.$success-color;
  border-color: v.$success-border;
}

.cc-badge-cancelled {
  background: v.$bg-secondary;
  color: v.$text-tertiary;
  border-color: v.$border-color;
}

.cc-badge-available {
  background: v.$success-bg;
  color: v.$success-color;
  border-color: v.$success-border;
}

.cc-badge-in_use {
  background: v.$info-bg;
  color: v.$primary-color;
  border-color: v.$info-border;
}

.cc-badge-in_shop {
  background: v.$warning-bg;
  color: v.$warning-color;
  border-color: v.$warning-border;
}

.cc-badge-retired {
  background: v.$bg-secondary;
  color: v.$text-tertiary;
  border-color: v.$border-color;
}

.cc-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-top: 1px solid v.$border-color;
  background: v.$bg-secondary;
}

.cc-footer-text {
  font-size: 0.875rem;
  color: #94a3b8;
}

.cc-footer-link {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3b82f6;
  text-decoration: none;
}

.cc-footer-link:hover {
  text-decoration: underline;
}

/* Sidebar */
.cc-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cc-card-body {
  padding: 1.5rem;
}

.cc-dist-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.cc-dist-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cc-dist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.cc-dist-label {
  color: #94a3b8;
  font-weight: 500;
}

.cc-dist-value {
  color: #fff;
  font-weight: 600;
}

.cc-progress-bar-wrapper {
  height: 8px;
  background: rgba(51, 65, 85, 0.8);
  border-radius: 9999px;
  overflow: hidden;
}

.cc-progress-bar-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.5s ease;
}

.cc-progress-available {
  background: #10b981;
}

.cc-progress-in-use {
  background: #3b82f6;
}

.cc-progress-in-shop {
  background: #f97316;
}

/* Vehicle Type Progress Colors */
.cc-progress-truck {
  background: #3b82f6;
}

.cc-progress-van {
  background: #06b6d4;
}

.cc-progress-bike {
  background: #10b981;
}

/* Region Progress Colors */
.cc-progress-north {
  background: #3b82f6;
}

.cc-progress-south {
  background: #10b981;
}

.cc-progress-east {
  background: #f59e0b;
}

.cc-progress-west {
  background: #06b6d4;
}

.cc-progress-central {
  background: #8b5cf6;
}

.cc-stats-grid {
  display: flex;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(51, 65, 85, 0.8);
}

.cc-stat {
  flex: 1;
  text-align: center;
}

.cc-stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.25rem;
}

.cc-stat-label {
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

.cc-stat-divider {
  width: 1px;
  height: 2rem;
  background: rgba(51, 65, 85, 0.8);
}

/* Quick Actions */
.cc-actions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cc-action {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background 0.2s;
}

.cc-action:hover {
  background: v.$bg-secondary;
}

.cc-action-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.cc-action-primary {
  background: rgba(59, 130, 246, 0.1);
}

.cc-action-warning {
  background: rgba(249, 115, 22, 0.1);
}

.cc-action-success {
  background: rgba(16, 185, 129, 0.1);
}

.cc-action-content {
  flex: 1;
}

.cc-action-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.125rem;
}

.cc-action-desc {
  font-size: 0.75rem;
  color: v.$text-secondary;
}

.cc-action-arrow {
  font-size: 1.5rem;
  color: v.$text-tertiary;
}

/* Dark Mode Overrides */
[data-theme="dark"] {
  .cc-kpi-card,
  .cc-card {
    background: #161b22;
    border-color: #30363d;
  }

  .cc-card-header,
  .cc-card-footer,
  .cc-filter-bar {
    background: #0d1117;
    border-color: #30363d;
  }

  .cc-table thead {
    background: #0d1117;
    border-color: #30363d;
  }

  .cc-table td {
    border-color: #21262d;
  }

  .cc-table tbody tr:hover {
    background: #21262d;
  }

  .cc-btn-secondary {
    background: #21262d;
    border-color: #30363d;
    color: #c9d1d9;
  }

  .cc-btn-secondary:hover {
    background: #30363d;
  }

  .cc-filter-chip {
    background: #21262d;
    border-color: #30363d;
    color: #8b949e;
  }

  .cc-filter-chip:hover {
    background: #30363d;
    color: #c9d1d9;
  }

  .cc-filter-chip.active {
    background: v.$primary-color;
    color: v.$white;
    border-color: v.$primary-color;
  }

  .cc-action:hover {
    background: #21262d;
  }

  .cc-progress-bar-wrapper {
    background: #21262d;
  }

  .cc-stat-divider {
    background: #30363d;
  }

  .cc-progress-bg {
    stroke: #30363d;
  }

  .cc-kpi-label,
  .cc-kpi-total,
  .cc-text-secondary,
  .cc-footer-text,
  .cc-dist-label,
  .cc-stat-label,
  .cc-action-desc {
    color: #8b949e;
  }

  .cc-kpi-value,
  .cc-title,
  .cc-card-title,
  .cc-dist-value,
  .cc-stat-value,
  .cc-action-title,
  .cc-progress-text {
    color: #c9d1d9;
  }

  .cc-subtitle {
    color: #7d8590;
  }
}
</style>
