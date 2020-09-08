<template>
    <div id="generalSearchVideoList">
        <b-card class="searchResult"
                v-for="item in videoList"
                :key="videoList.indexOf(item)">
            <b-card-group>
                <b-card style="min-width: 360px">
                    <b-embed
                            type="iframe"
                            aspect="16by9"
                            :src="urlConverter(item.tracks[1].url)"
                            allowfullscreen
                    />
                </b-card>
                <b-card style="min-width: 360px">
                    <b-card-group id="metaInfo" style="margin-bottom: 20px">
                        <b-card style="font-size: 100%">
                            <span class="mr-4">
                                <b-icon icon="hand-thumbs-up" aria-hidden="true"></b-icon>
                                /
                                <b-icon icon="hand-thumbs-down" aria-hidden="true"></b-icon>
                                : {{ Math.round(item.features.like_ratio * 10000) /100 }} %
                            </span>
                            <span class="mr-4">
                                <b-icon icon="bookmark-check" aria-hidden="true"></b-icon>
                                : {{ item.features.subs }}
                            </span>
                            <span class="">
                                <b-icon icon="eye" aria-hidden="true"></b-icon>
                                : {{ item.features.views }}
                            </span>
                        </b-card>

                    </b-card-group>

                    <b-card-group id="subtitles" style="margin-top: auto">
                        <b-card class="subtitleSection" style="font-size: 130%">
                            <span>... </span>
                            <div v-for="track in item.tracks" :key="item.tracks.indexOf(track)">
                                <span>{{ track.content }}</span>
                            </div >
                            <span> ...</span>
                        </b-card>
                    </b-card-group>
                </b-card>
            </b-card-group>
        </b-card>
    </div>
</template>

<script>
    export default {
        name: "generalSearchVideoList",

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
                return `${minute}:${second}`
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
                const langId = this.$store.state.generalSearch.search.language

                return `https://www.youtube.com/embed/${videoKey}?start=${startTime}&cc_load_policy=1&cc_lang_pref=${langId}`
            }
        },
        computed: {
            videoList () {
                return this.$store.state.generalSearch.videoQueryResult
            }
        },
        watch: {
        }

    }
</script>

<style>

</style>