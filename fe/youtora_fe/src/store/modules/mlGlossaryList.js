import axios from 'axios'


export default {
    namespaced: true,
    state: {
        isLoadingGlossaries: true,
        glossaryList: []
    },
    getters: {
        GET_GLOSSARY_LIST: (state) => {return state.glossaryList}
    },
    mutations: {
        SET_GLOSSARY_LOADING: (state, status) => {state.isLoadingGlossaries = status},
        SET_GLOSSARY_LIST: (state, glossary) => {state.glossaryList = glossary}
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

        }
    },

}