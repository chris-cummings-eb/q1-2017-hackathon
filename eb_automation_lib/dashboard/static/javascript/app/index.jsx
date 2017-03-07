// @flow
import 'babel-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import { AppContainer } from 'react-hot-loader'

import App from './components/App'

const root = document.getElementById('react-target-container')

const wrapApp = AppComponent => (
  <AppContainer>
    <AppComponent />
  </AppContainer>
)

ReactDOM.render(<App />, root)

// if (module.hot) {
  // flow-disable-next-line
  // module.hot.accept('./', () => {
    // // eslint-disable-next-line global-require
    // const NextApp = require('./components/App').default
    // ReactDOM.render(wrapApp(NextApp), root)
  // })
// }
