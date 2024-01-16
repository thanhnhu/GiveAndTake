import cityService from '../../services/cityService'

const FETCH_CITIES_REQUEST = 'FETCH_CITIES_REQUEST'
const FETCH_CITIES_SUCCESS = 'FETCH_CITIES_SUCCESS'
const FETCH_CITIES_FAILURE = 'FETCH_CITIES_FAILURE'

const state = {
  fetchingData: true,
  error: null,
  cities: []
}

const getters = {
  optionCities: state => {
    return [{ id: null, name: 'Chọn thành phố' }, ...state.cities]
  }
}

const actions = {
  getCities({ commit }) {
    commit(FETCH_CITIES_REQUEST)
    cityService.fetchCities()
      .then(cities => { commit(FETCH_CITIES_SUCCESS, cities) })
      .catch(error => commit(FETCH_CITIES_FAILURE, { error }))
  }
}

const mutations = {
  [FETCH_CITIES_REQUEST](state) {
    state.fetchingData = true
    state.error = null
    state.cities = []
  },
  [FETCH_CITIES_SUCCESS](state, cities) {
    var first = [15, 58];
    cities = cities.sort(function (x, y) { return first.includes(x.id) ? -1 : first.includes(y.id) ? 1 : 0; });
    state.cities = cities
    state.fetchingData = false
    state.error = null
  },
  [FETCH_CITIES_FAILURE](state, { error }) {
    state.fetchingData = false
    state.error = error
    state.cities = []
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}