<template>
    <div id="videoList">
        <b-card v-for="item in videoList"
                :key="videoList.indexOf(item)">
            <b-card-group>
                <b-card v-for="track in item.tracks" :key="item.tracks.indexOf(track)">
                    {{ videoIndicator(item.tracks.indexOf(track)) }}
                    <b-embed
                            type="iframe"
                            aspect="16by9"
                            :src="urlConverter(track.url)"
                            allowfullscreen
                    />
                    {{ getTime(track.url) }}
                </b-card>
            </b-card-group>
            <b-card-group>
                <b-card>
                    <h5 class="mt-0 mb-1">Like Ratio</h5>
                    <p class="mb-0">
                        {{ item.features.like_ratio }}
                    </p>
                </b-card>
                <b-card>
                    <h5 class="mt-0 mb-1">Subscribers</h5>
                    <p class="mb-0">
                        {{ item.features.subs }}
                    </p>
                </b-card>
                <b-card>
                    <h5 class="mt-0 mb-1">View Counts</h5>
                    <p class="mb-0">
                        {{ item.features.views }}
                    </p>
                </b-card>
            </b-card-group>
        </b-card>
    </div>
</template>

<script>
    export default {
        name: "VideoList",
        data() {
            return{
                // videoList: this.$store.getters.GET_VIDEO_LIST
            }
        },
        methods: {
            getTime: function (original_link) {
                const timeSecond = original_link.split("=")[1]
                const minute = Math.floor(timeSecond/60)
                const second = timeSecond % 60
                return `Starting from ${minute}:${second}`
            },
            videoIndicator: function (idx) {
                if (idx === 0) {
                    return 'Previous subtitle'
                } else if (idx === 1) {
                    return 'Target subtitle'
                } else if (idx === 2) {
                    return 'Next subtitle'
                }
            },
            urlConverter: function (original_link) {
                const startTime = original_link.split("=")[1]
                const videoKey = original_link.split("/")[3].split("=")[0].split("?")[0]
                const newLink = `https://www.youtube.com/embed/${videoKey}?start=${startTime}&cc_load_policy=1`

                return newLink
            }
        },
        computed: {
            videoList () {
                return this.$store.state.videoQueryResult
            }
        },
        watch: {
        }

    }
</script>

<style>

</style>