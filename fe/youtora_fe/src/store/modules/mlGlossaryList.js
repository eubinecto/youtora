import axios from 'axios'


export default {
    namespaced: true,
    state: {
        isLoadingGlossaries: true,
        isLoadingVideos: true,
        glossaryList: [],
        glossaryDict : {},

        searchQuery: '',
        searchLanguage: 'en',
        targetDesc: '',
        targetCredit: '',

        perPage: 3,
        currentPage: 1,
        searchTotalCount: 30,

        searchResult: [],

    },
    getters: {
        GET_GLOSSARY_LIST: (state) => {return state.glossaryList},
        GET_GLOSSARY_DICT: (state) => {return state.glossaryDict},
        GET_SEARCH_QUERY: (state) => {return state.searchQuery},
        GET_TARGET_DESC: (state) => {return state.targetDesc},
        GET_TARGET_CREDIT: (state) => {return state.targetCredit},
        GET_SEARCH_LANGUAGE: (state) => {return state.searchLanguage},
        GET_PER_PAGE: (state) => {return state.perPage},

        GET_CURRENT_PAGE: (state) => {return state.currentPage},
        GET_TOTAL_COUNT: (state) => {return state.searchTotalCount},

        GET_SEARCH_RESULT: (state) => {return state.searchResult}

    },
    mutations: {
        SET_GLOSSARY_LOADING: (state, status) => {state.isLoadingGlossaries = status},
        SET_VIDEO_LOADING: (state, status) => {state.isLoadingVideos = status},

        SET_GLOSSARY_LIST: (state, glossary) => {state.glossaryList = glossary},
        SET_GLOSSARY_DICT: (state, glossaryDict) => {state.glossaryDict = glossaryDict},

        SET_SEARCH_QUERY: (state, query) => {state.searchQuery = query},
        SET_TARGET_DESC: (state, desc) => {state.targetDesc = desc},
        SET_TARGET_CREDIT: (state, credit) => {state.targetCredit = credit},
        SET_SEARCH_LANGUAGE: (state, language) => {state.searchLanguage = language},
        SET_PER_PAGE: (state, perPage) => {state.perPage = perPage},

        SET_CURRENT_PAGE: (state, curPage) => {state.currentPage = curPage},

        SET_SEARCH_RESULT: (state, videoList) => {state.searchResult = videoList},
        SET_TOTAL_COUNT: (state, videoCount) => {state.searchTotalCount = videoCount}
    },
    actions: {
        SEARCH_GLOSSARY: async ({commit}) => {
            commit('SET_GLOSSARY_LOADING', true)
            const targetLink = process.env.VUE_APP_API + '/mongo/corpora_db/ml_gloss_coll'

            await axios.get(targetLink, {data: null, params: null})
                .then(function (response) {
                    if (response.status !== 200) {
                        alert('WRONG REQUEST')

                    } else {
                        const glossaryResult = response.data
                        commit('SET_GLOSSARY_LIST', glossaryResult)

                        const glossaries = glossaryResult
                        var glossaryDict = {
                            'a': [],
                            'b': [],
                            'c': [],
                            'd': [],
                            'e': [],
                            'f': [],
                            'g': [],
                            'h': [],
                            'i': [],
                            'j': [],
                            'k': [],
                            'l': [],
                            'm': [],
                            'n': [],
                            'o': [],
                            'p': [],
                            'q': [],
                            'r': [],
                            's': [],
                            't': [],
                            'u': [],
                            'v': [],
                            'w': [],
                            'x': [],
                            'y': [],
                            'z': []

                        }
                        for (let i = 0; i < glossaries.length; i++) {
                            var curWord = glossaries[i].word
                            curWord = curWord.charAt(0).toUpperCase() + curWord.slice(1)
                            var firstChar = curWord.charAt(0).toLowerCase()

                            glossaryDict[firstChar].push(glossaries[i])
                        }
                        commit('SET_GLOSSARY_DICT', glossaryDict)

                        commit('SET_GLOSSARY_LOADING', false)

                    }
                })

        },
        SEARCH_WORD: async ({commit, state}) =>{
            state.isLoadingVideos = true
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
                        commit('SET_VIDEO_LOADING', false)
                        console.log(state.searchResult)
                        this.getDesc(this.getOrgWord(this.targetWord))
                        this.getCredit(this.getOrgWord(this.targetWord))
                    }
                })
        },

    },

}