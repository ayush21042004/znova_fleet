<template>
  <div class="o2m-field-wrapper">
    <!-- Show display_name directly in readonly mode if available -->
    <a 
      v-if="readonly && displayName" 
      class="o2m-readonly-link"
      @click.prevent="openRecord"
      :title="`Open ${displayName}`"
    >
      {{ displayName }}
    </a>
    <Many2OneField
      v-else
      :model-value="parsedValue"
      :options="options"
      :readonly="readonly"
      :invalid="invalid"
      :relation="fieldMeta?.relation"
      :placeholder="fieldMeta?.label || 'Select...'"
      @update:model-value="handleUpdate"
      @focus="$emit('focus')"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import Many2OneField from '../Many2OneField.vue';

const props = defineProps<{
  modelValue: any | null;
  fieldMeta: any;
  readonly?: boolean;
  invalid?: boolean;
  relationOptions?: any[];
  context?: Record<string, any>;
}>();

const emit = defineEmits(['update:modelValue', 'focus']);
const router = useRouter();

// Extract display_name if value is an object
const displayName = computed(() => {
  if (props.modelValue && typeof props.modelValue === 'object') {
    return props.modelValue.display_name || props.modelValue.name || props.modelValue.full_name || null;
  }
  return null;
});

// Extract record ID for navigation
const recordId = computed(() => {
  if (props.modelValue && typeof props.modelValue === 'object') {
    return props.modelValue.id;
  }
  return props.modelValue;
});

// Open the related record
const openRecord = () => {
  if (recordId.value && props.fieldMeta?.relation) {
    router.push(`/models/${props.fieldMeta.relation}/${recordId.value}`);
  }
};

// Handle both ID (int) and Object ({id, name}) values
const parsedValue = computed(() => {
  if (props.modelValue && typeof props.modelValue === 'object') {
    return props.modelValue.id;
  }
  return props.modelValue;
});

const localOptions = ref<any[]>([]);

const options = computed(() => {
  const sourceOptions = localOptions.value.length > 0 ? localOptions.value : (props.relationOptions || []);
  
  // If we have a modelValue object with display_name, ensure it's in the options
  if (props.modelValue && typeof props.modelValue === 'object' && props.modelValue.id) {
    const existingOption = sourceOptions.find((opt: any) => opt.id === props.modelValue.id);
    if (!existingOption) {
      const recName = props.fieldMeta?.rec_name || 'display_name';
      const displayValue = props.modelValue[recName] || props.modelValue.display_name || props.modelValue.name || props.modelValue.full_name || props.modelValue.subject || `#${props.modelValue.id}`;
      sourceOptions.push({
        id: props.modelValue.id,
        [recName]: displayValue,
        display_name: displayValue,
        name: displayValue
      });
    }
  }
  
  const recName = props.fieldMeta?.rec_name || 'display_name';
  return sourceOptions.map(opt => ({
    val: opt.id,
    label: opt[recName] || opt.display_name || opt.name || opt.full_name || opt.subject || `#${opt.id}`
  }));
});

import api from '../../../core/api';
import { DomainEngine } from '../../../core/domain-engine';

const loadOptions = async () => {
  if (!props.fieldMeta?.domain || !props.fieldMeta?.relation) return;
  
  try {
    const domainEngine = new DomainEngine();
    const domain = domainEngine.resolveDomain(props.fieldMeta.domain, props.context || {});
    
    if (domain && domain.length > 0) {
      const resp = await api.get(`/models/${props.fieldMeta.relation}`, {
        params: { domain: JSON.stringify(domain) }
      });
      localOptions.value = resp.data?.items || [];
    }
  } catch (e) {
    // Silently fail
  }
};

onMounted(() => {
  if (props.fieldMeta?.domain) {
    loadOptions();
  }
});

watch(() => props.context, () => {
  if (props.fieldMeta?.domain) {
    loadOptions();
  }
}, { deep: true });

const handleUpdate = (value: any) => {
  emit('update:modelValue', value);
};
</script>

<style scoped>
.o2m-field-wrapper {
  padding: 0 4px; /* Reduced padding */
  position: relative;
  width: 100%;
  min-width: 120px; /* Ensure minimum usable width */
}

.o2m-readonly-link {
  display: inline-block;
  padding: 6px 8px;
  color: #5b8fd8; /* Blue faded color */
  font-size: 0.875rem;
  line-height: 1.5;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
  opacity: 0.85; /* Slightly faded */
}

.o2m-readonly-link:hover {
  color: #4a7bc4; /* Darker blue on hover */
  opacity: 1;
  text-decoration: underline;
}

.o2m-readonly-link:active {
  color: #3a6bb0; /* Even darker on click */
}

/* Override dropdown width to prevent narrow dropdowns */
:deep(.dropdown-list) {
  min-width: 200px !important;
  width: max-content !important;
  max-width: 300px !important;
}

/* Ensure proper spacing for actions */
:deep(.selected-display) {
  width: calc(100% - 60px) !important; /* Reduced reserved space to show more text */
  padding-right: 4px;
}

:deep(.many2one-input) {
  padding-right: 60px; /* Reduced reserved space */
}

/* On hover/focus, we might need more space for actions if they appear, 
   but 60px should be enough for clear + arrow */
</style>
