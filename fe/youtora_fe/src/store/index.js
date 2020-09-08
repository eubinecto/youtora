import mlGlossaryList from "./modules/mlGlossaryList";
import generalSearch from "./modules/generalSearch";

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        generalSearch: generalSearch,
        mlGlossary: mlGlossaryList
    }
})