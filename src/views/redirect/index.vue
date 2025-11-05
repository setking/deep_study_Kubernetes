<script lang="ts" setup>
const route = useRoute()
const router = useRouter()
console.log(route.params)
router.replace({ path: `/${route.params.path}`, query: route.query })
</script>

<template>
  <div />
</template>
