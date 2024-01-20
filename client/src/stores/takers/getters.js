import { arrayOrderedToObject } from '../../helpers'

export default {
  // Array as Object => this make easier to handle
  takers: state => {
    return { ...arrayOrderedToObject(state.takers, "id") }
  }
}
