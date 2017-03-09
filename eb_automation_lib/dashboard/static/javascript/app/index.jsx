// @flow
import 'babel-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'

import App from './components/App'

const root = document.getElementById('react-target-container')

ReactDOM.render(<App />, root)
