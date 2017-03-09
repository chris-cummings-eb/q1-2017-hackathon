import 'babel-polyfill'
import React, { Component } from 'react'

import Title from './Title'
import AutomationList from './AutomationList'
import FilterInput from './FilterInput'

class App extends Component {
  constructor() {
    super()
    this.state = {
      automations: [],
    }
  }

  componentDidMount() {
    const socket = io('http://localhost:5555') // eslint-disable-line no-undef
    socket.on('connect', () => console.log('connected')) // eslint-disable-line no-console
    socket.on('event', data => console.log('there was an event', data)) // eslint-disable-line no-console
    socket.on('message', message => console.log(message)) // eslint-disable-line no-console

    // when automations are set, update what is displayed
    socket.on('automations_list_update', data => this.updateAutomations(data.automations))
  }

  updateAutomations(list) {
    this.setState(prevState => ({
      ...prevState,
      automations: list.map(e => Object.assign({}, e, { filtered: false, hidden: false })),
    }))
  }

  automationsFilter(filter) {
    this.setState((prevState) => {
      const pattern = new RegExp(filter)
      const updatedAutomations = prevState.automations.map((e) => {
        if (filter.length < 1) {
          return { ...e, filtered: false }
        } else if (
            pattern.test(e.name) ||
            pattern.test(e.object_name) ||
            pattern.test(e.description)
          ) {
          return { ...e, filtered: false }
        }
        return { ...e, filtered: true }
      })

      return { ...prevState, automations: updatedAutomations }
    })
  }

  handleItemClick(itemID) {
    this.setState((prevState) => {
      const updatedAutomations = [...prevState.automations].map((e) => {
        if (e.id === itemID) {
          return { ...e, dispatched: true }
        }
        return { ...e }
      })

      return { ...prevState, automations: updatedAutomations }
    })
  }


  render() {
    const { automations } = this.state
    const getVisible = list => list.filter(e => !e.filtered && !e.hidden)

    return (
      <div style={{ padding: '15px' }}>
        <Title />
        <FilterInput
          onChange={(e, d) => this.automationsFilter(d.value)}
        />
        <AutomationList
          items={getVisible(automations)}
          onItemClick={itemID => this.handleItemClick(itemID)}
        />
      </div>
    )
  }
}

export default App
