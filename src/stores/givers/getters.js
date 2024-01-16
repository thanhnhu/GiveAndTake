import { arrayOrderedToObject } from '../../helpers'

export default {
  // Array as Object => this make easier to handle
  givers: state => {
    return { ...arrayOrderedToObject(state.givers, "id") }
  }
}
