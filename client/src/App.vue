<template><router-view></router-view></template>
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

document.addEventListener('keydown', (event) => { if ((event.ctrlKey === true || event.metaKey === true) && (event.which === 61 || event.which === 107 || event.which === 173 || event.which === 109 || event.which === 187 || event.which === 189)) { event.preventDefault(); } }, false);
document.addEventListener('mousewheel', (e: any) => { if ((e.wheelDelta && e.ctrlKey) || e.detail) { e.preventDefault(); } }, { capture: false, passive: false });
const handleResize = () => {
    const ratio = window.devicePixelRatio;
    document.body.style.zoom = `${ratio / ratio}`;
};

onMounted(() => {
    handleResize();
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {window.removeEventListener('resize', handleResize);});
</script>