<template>
    <div class="container">
        <div id="system">
            <h3>系统信息</h3>
            <el-table :data="datas[3]" border :show-header="false" height="320">
                <el-table-column prop="name" label="KEY" align="center" />
                <el-table-column prop="value" label="VALUE" align="center" />
            </el-table>
        </div>
        <div id="disk"></div>
        <div id="cpu"></div>
        <div id="mem"></div>
    </div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts';
import { ref, onMounted, onUnmounted, nextTick, watch, onBeforeUnmount } from "vue";
import { API_BASE_URL } from "@/utils/config/index";

const datas: any = ref([]);
const eventSource = ref()
const echartsdom: any = ref([])

const setdiskopt = () => {
    echartsdom.value[0].setOption({
        title: {
            text: '磁盘使用情况(GB)',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#283b56'
                }
            }
        },
        legend: {
            show: false
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: true,
                data: datas.value[0][0]
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '总量',
                type: 'bar',
                data: datas.value[0][1]
            },
            {
                name: '已使用',
                type: 'bar',
                data: datas.value[0][2]
            },
            {
                name: '剩余',
                type: 'bar',
                data: datas.value[0][3]
            }
        ]
    })
}
const setmemopt = () => {
    echartsdom.value[2].setOption({
        title: {
            text: '内存使用情况(GB/%)',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            show: false,
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: '内存',
                type: 'pie',
                radius: '50%',
                data: datas.value[2],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                label: {
                    show: true,
                    formatter: '{b} -> {c} -> {d}%',
                    color: '#fff'
                }
            }
        ]
    })
}
const setcpuopt = () => {
    echartsdom.value[1].setOption({
        title: {
            text: 'CPU 使用情况(%)',
            left: 'center'
        },
        tooltip: {
            formatter: '{a} <br/>{b} : {c}%'
        },
        series: [
            {
                name: 'CPU',
                type: 'gauge',
                progress: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    formatter: '{value}'
                },
                data: datas.value[1],
            }
        ]
    })
}

watch(datas, () => {
    setmemopt();
    setdiskopt();
    setcpuopt();
}), { deep: true, immediate: true }

nextTick(() => {
    const diskdom = document.getElementById('disk');
    const diskbar = echarts.init(diskdom, 'dark')
    const cpudom = document.getElementById('cpu');
    const cpubar = echarts.init(cpudom, 'dark')
    const memdom = document.getElementById('mem');
    const membar = echarts.init(memdom, 'dark')
    echartsdom.value = [diskbar, cpubar, membar]
})

onMounted(() => {
    eventSource.value = new EventSource(`${API_BASE_URL}/api/systeminfo/`)
    eventSource.value.onmessage = (event: any) => {
        datas.value = JSON.parse(event.data).data
        // console.log(datas.value[2])
    }
    eventSource.value.onerror = () => eventSource.value = new EventSource(`${API_BASE_URL}/api/systeminfo/progress/`)
    window.onresize = () => {
        for (let i = 0; i < echartsdom.value.length; i++) {
            echartsdom.value[i].resize();
        }
    }
});
onBeforeUnmount(() => {
    for (let i = 0; i < echartsdom.value.length; i++) {
        echartsdom.value[i].dispose();
    }
})
onUnmounted(() => { if (eventSource.value) eventSource.value.close(); });
</script>

<style scoped lang="less">
.container {
    width: calc(100% - 200px);
    height: calc(100% - 50px);
    margin: 50px 0 0 200px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    flex-wrap: wrap;
    align-items: center;

    #disk,
    #cpu,
    #mem,
    #system {
        width: calc(50% - 2px);
        height: calc(50% - 2px);
    }

    #system {
        border-bottom: 1px dashed #ccc;
        border-right: 1px dashed #ccc;
        h3 {
            text-align: center;
            margin-bottom: 30px;
        }
    }
    #disk {
        border-bottom: 1px dashed #ccc;
    }
    #cpu {
        border-right: 1px dashed #ccc;
    }
}
</style>