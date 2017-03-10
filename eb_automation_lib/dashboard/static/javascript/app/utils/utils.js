import 'babel-polyfill'

export function inArray(value, list) {
  let test = []
  list.forEach(e => test.push(e === value))
  test = test.filter(e => e === true)
  return test.length > 0
} 

export default inArray
