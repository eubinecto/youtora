import axios from 'axios'

export default {
    namespaced: true,
    state: {
        search: {
            query: null,
            language: null,
            chan_lang: null,
            perPage: 10
        },
        currentPage: 1,

        videoQueryResult: [],
        videoTotalCount: 0


    },
    getters: {
        GET_SEARCH_QUERY: (state) => {return state.search.query},
        GET_SEARCH_LANGUAGE: (state) => {return state.search.language},
        GET_CHAN_LANG: (state) => {return state.search.chan_lang},
        GET_PER_PAGE: (state) => {return state.search.perPage},

        GET_CURRENT_PAGE: (state) => {return state.currentPage},

        GET_VIDEO_LIST: (state) => {return state.videoQueryResult},
        GET_VIDEO_TOTAL_COUNT: (state) => {return state.videoTotalCount}
    },
    mutations: {
        CLEAR_SEARCH: (state) => {
            state.search.query = ''
            state.videoQueryResult = []
            state.videoTotalCount = 0
            state.currentPage = 1
        },

        SET_SEARCH_QUERY: (state, query) => {state.search.query = query},
        SET_SEARCH_LANGUAGE: (state, language) => {state.search.language = language},
        SET_CHAN_LANG: (state, lang) => {state.search.chan_lang = lang},
        SET_PER_PAGE: (state, perPage) => {state.search.perPage = perPage},

        SET_CURRENT_PAGE: (state, curPage) => {state.currentPage = curPage},

        SET_VIDEO_LIST: (state, videoList) => {state.videoQueryResult = videoList},
        SET_VIDEO_TOTAL_COUNT: (state, videoCount) => {state.videoTotalCount = videoCount}
    },
    actions: {
        SEARCH_VIDEOS: async ({commit, state}) => {
            const targetLink = process.env.VUE_APP_API + '/youtora_tracks/search'
            const payloadParams = {
                "content": state.search.query,
                "caption_lang_code": state.search.language,
                "chan_lang_code": state.search.chan_lang,
                "from": (state.currentPage - 1) * state.search.perPage + 1,
                "size": state.search.perPage
            }
            await axios.get(targetLink, {data: null, params: payloadParams})
                .then(function (response) {
                    if (response.status !== 200) {
                        alert('QUERY' + state.search.query + 'not in DB')
                        commit('CLEAR_SEARCH')
                    } else {
                        const searchResult = response.data.data
                        const totalCnt = response.data.meta
                        commit('SET_VIDEO_LIST', searchResult)
                        commit('SET_VIDEO_TOTAL_COUNT', totalCnt)

                    }
                })

        }
    },

}