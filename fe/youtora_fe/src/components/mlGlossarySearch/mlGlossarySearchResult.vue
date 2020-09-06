<template>
    <div id="generalSearchVideoList">
        <b-card v-for="item in videoList"
                :key="videoList.indexOf(item)">
            <b-card-group>
                <b-card>
                    <b-embed
                            type="iframe"
                            aspect="16by9"
                            :src="urlConverter(item.tracks[0].url)"
                            allowfullscreen
                    />
                </b-card>
                <b-card>
                    <div id="videoMetaBase" align="left">
                        <b-card>
                            <h6>* Title: </h6>
                        </b-card>
                        <b-card>
                            <h6>* Owner: </h6>
                        </b-card>

                    </div>

                    <b-card-group id="metaInfo" style="margin-bottom: 20px">
                        <b-card>
                            <h6 class="mt-0 mb-1">
                                <b-icon icon="hand-thumbs-up" aria-hidden="true"></b-icon>
                                /
                                <b-icon icon="hand-thumbs-down" aria-hidden="true"></b-icon>
                                <br/>
                                Like Ratio
                            </h6>
                            <p class="mb-0">
                                {{ Math.round(item.features.like_ratio * 10000) /100 }} %
                            </p>
                        </b-card>
                        <b-card>
                            <h6 class="mt-0 mb-1">
                                <b-icon icon="bookmark-check" aria-hidden="true"></b-icon>
                                <br/>
                                Subscribers
                            </h6>
                            <p class="mb-0">
                                {{ item.features.subs }}
                            </p>
                        </b-card>
                        <b-card>
                            <h6 class="mt-0 mb-1">
                                <b-icon icon="eye" aria-hidden="true"></b-icon>
                                <br/>
                                View Counts
                            </h6>
                            <p class="mb-0">
                                {{ item.features.views }}
                            </p>
                        </b-card>
                    </b-card-group>

                    <h3>Subtitle</h3><br/>
                    <b-card-group id="subtitles" style="margin-top: auto" align="left">
                        <div v-for="track in item.tracks" :key="item.tracks.indexOf(track)">
                            <h5>
                                [ {{ getTime(track.url) }} ] : {{ track.content }}
                            </h5>
                        </div>
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