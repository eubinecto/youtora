<template>
    <div id="generalSearchVideoList">
        <b-card v-for="item in videoList"
                :key="videoList.indexOf(item)">
            <b-card-group>
                <b-card>
                    <b-embed
                            type="iframe"
                            aspect="16by9"
                            :src="urlConverter(item.tracks[1].url)"
                            allowfullscreen
                    />

                    <b-card-group id="subtitles" class="mb-2 mt-2">
                        <b-card class="subtitleSection border-white" style="font-size: 150%; vertical-align: center" align="center">
                            <h5>... </h5>
                            <div v-for="track in item.tracks" :key="item.tracks.indexOf(track)">
                                <h5>{{ track.content }}</h5>
                            </div >
                            <h5> ...</h5>
                        </b-card>
                    </b-card-group>

                    <b-card-group id="metaInfo" class="mb-2 mt-2">
                        <b-card align="center">
                            <b-card-group>
                                <b-card class="border-white">
                                    <b-icon icon="hand-thumbs-up" aria-hidden="true"/>
                                    /
                                    <b-icon icon="hand-thumbs-down" aria-hidden="true" class="mr-2"/>
                                        {{ Math.round(item.features.like_ratio * 10000) /100 }} %
                                </b-card>

                                <b-card class="border-white">
                                    <b-icon icon="bookmark-check" aria-hidden="true" class="mr-2"/>
                                        {{ item.features.subs }}
                                </b-card>

                                <b-card class="border-white">
                                    <b-icon icon="eye" aria-hidden="true" class="mr-2"/>
                                    {{ item.features.views }}
                                </b-card>
                            </b-card-group>
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
                const langId = this.$store.state.mlGlossary.searchLanguage

                return `https://www.youtube.com/embed/${videoKey}?start=${startTime}&cc_load_policy=1&cc_lang_pref=${langId}`
            }
        },
        computed: {
            videoList () {
                return this.$store.state.mlGlossary.searchResult
            }
        },
        watch: {
        }

    }
</script>

<style>

</style>