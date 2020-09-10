<template>
    <div id="generalSearchVideoList">
        <b-card class="searchResult"
                v-for="item in videoList"
                :key="videoList.indexOf(item)">
            <b-card-group>
                <b-card style="min-width: 450px">
                    <b-embed
                            type="iframe"
                            aspect="16by9"
                            :src="urlConverter(item.tracks[1].url)"
                            allowfullscreen
                    />
                </b-card>
                <b-card style="min-width: 450px">
                    <b-card-group id="subtitles">
                        <b-card class="subtitleSection border-white" style="font-size: 150%; vertical-align: center">
                            <span>..... </span>
                            <span v-html="item.highlight.context[0]"></span>
                            <span> .....</span>
                        </b-card>
                    </b-card-group>
                </b-card>
            </b-card-group>

            <b-card-group id="metaInfo" style="margin-bottom: 20px">
                <b-card style="font-size: 90%">
                    <b-card-group>
                        <b-card class="border-white" style="min-width: 140px">
                            <span>
                                <font-awesome-icon icon="thumbs-up" size="lg"/>
                                /
                                <font-awesome-icon icon="thumbs-down" size="lg"/>
                                : {{ Math.round(item.features.caption.video.like_ratio * 10000) /100 }}%
                            </span>
                        </b-card>
                        <b-card class="border-white" style="min-width: 140px">
                            <span>
                                <font-awesome-icon icon="bookmark" size="lg"/>
                                : {{ item.features.caption.video.channel.subs }}
                            </span>
                        </b-card>
                        <b-card class="border-white" style="min-width: 140px">
                            <span>
                                <font-awesome-icon icon="eye" size="lg"/>
                                : {{ item.features.caption.video.views }}
                            </span>
                        </b-card>
                        <b-card class="border-white" style="min-width: 140px">
                            <span>
                                <font-awesome-icon icon="closed-captioning" size="lg"/>
                                : {{ isAuto(item.features.caption.is_auto) }}
                            </span>
                        </b-card>
                        <b-card class="border-white" style="min-width: 140px">
                            <span>
                                <font-awesome-icon icon="language" size="lg"/>
                                : {{ item.features.caption.lang_code }}
                            </span>
                        </b-card>
                        <b-card class="border-white" style="min-width: 150px">
                            <span>
                                <font-awesome-icon icon="filter" size="lg"/>
                                : {{ item.features.caption.video.category }}
                            </span>
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

            isAuto: function (target) {
                if (target === true) {
                    return 'Auto'
                } else {
                    return 'Manual'
                }
            },
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