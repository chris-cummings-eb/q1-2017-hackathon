import 'babel-polyfill'
import React, { Component } from 'react'

import Title from './Title'
import AutomationList from './AutomationList'
import FilterInput from './FilterInput'

class App extends Component {
  constructor() {
    super()
    this.socket = io('http://localhost:5555') // eslint-disable-line no-undef
    this.state = {
      automations: [],
      clipboard: '',
    }
  }

  componentDidMount() {
    this.socket.on('automations_list_update', data => this.updateAutomations(data.automations))
    this.socket.on('clipboard', (data) => {
      console.log(data)
      this.setState(data)
    })
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
    const { automations } = this.state
    const updatedAutomations = automations.map(e => (
      e.id === itemID ? { ...e, dispatched: true } : { ...e }
    ))

    this.setState(prevState => ({ ...prevState, automations: updatedAutomations }))

    const toDispatch = updatedAutomations.filter(e => e.dispatched)
    if (toDispatch.length > 0) {
      this.socket.emit('dispatch', { automations: toDispatch })
    }
  }


  render() {
    const { automations, clipboard } = this.state
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
