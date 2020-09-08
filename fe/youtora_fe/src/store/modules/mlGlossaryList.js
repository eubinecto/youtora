import axios from 'axios'


export default {
    namespaced: true,
    state: {
        isLoadingGlossaries: true,
        glossaryList: [],

        searchQuery: '',
        searchLanguage: 'en',

        perPage: 3,
        currentPage: 1,
        searchTotalCount: 30,

        searchResult: [],

    },
    getters: {
        GET_GLOSSARY_LIST: (state) => {return state.glossaryList},

        GET_SEARCH_QUERY: (state) => {return state.searchQuery},
        GET_SEARCH_LANGUAGE: (state) => {return state.searchLanguage},
        GET_PER_PAGE: (state) => {return state.perPage},

        GET_CURRENT_PAGE: (state) => {return state.currentPage},
        GET_TOTAL_COUNT: (state) => {return state.searchTotalCount},

        GET_SEARCH_RESULT: (state) => {return state.searchResult}

    },
    mutations: {
        SET_GLOSSARY_LOADING: (state, status) => {state.isLoadingGlossaries = status},
        SET_GLOSSARY_LIST: (state, glossary) => {state.glossaryList = glossary},

        SET_SEARCH_QUERY: (state, query) => {state.searchQuery = query},
        SET_SEARCH_LANGUAGE: (state, language) => {state.searchLanguage = language},
        SET_PER_PAGE: (state, perPage) => {state.perPage = perPage},

        SET_CURRENT_PAGE: (state, curPage) => {state.currentPage = curPage},

        SET_SEARCH_RESULT: (state, videoList) => {state.searchResult = videoList},
        SET_TOTAL_COUNT: (state, videoCount) => {state.searchTotalCount = videoCount}
    },
    actions: {
        SEARCH_GLOSSARY: async ({commit}) => {
            commit('SET_GLOSSARY_LOADING', true)
            const targetLink = process.env.VUE_APP_API + '/mongo/corpora_db/ml_gloss_raw_coll'


            await axios.get(targetLink, {data: null, params: null})
                .then(function (response) {
                    if (response.status !== 200) {
                        alert('WRONG REQUEST')

                    } else {
                        const glossaryResult = response.data
                        commit('SET_GLOSSARY_LIST', glossaryResult)
                        commit('SET_GLOSSARY_LOADING', false)

                    }
                })

        },
        SEARCH_WORD: async ({commit, state}) =>{
            const targetLink = process.env.VUE_APP_API + '/youtora_tracks/search'
            const payloadParams = {
                "content": state.searchQuery,
                "caption_lang_code": state.searchLanguage,
                "from": (state.currentPage - 1) * state.perPage + 1,
                "size": state.perPage
            }
            await axios.get(targetLink, {data: null, params: payloadParams})
                .then(function (response) {
                    if (response.status !== 200) {
                        alert('WRONG REQUEST')

                    } else {
                        const glossaryResult = response.data.data
                        const resultLength = response.data.meta
                        commit('SET_SEARCH_RESULT', glossaryResult)
                        if (resultLength < 30) {
                            commit('SET_TOTAL_COUNT', resultLength)
                        } else {
                            commit('SET_TOTAL_COUNT', 30)
                        }


                    }
                })
        }
    },

}