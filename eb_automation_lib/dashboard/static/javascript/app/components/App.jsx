import 'babel-polyfill'
import React, { Component } from 'react'

import Title from './Title'
import AutomationList from './AutomationList'
import FilterInput from './FilterInput'

class App extends Component {
  constructor() {
    super()
    this.state = {
      automations: [
        { id: 1, name: 'do cool thing 1', func: 'cool_thing_1', filtered: false, description: 'its so cool yo', dispatched: false, hidden: false },
        { id: 2, name: 'do cool thing 2', func: 'cool_thing_2', filtered: false, dispatched: false, hidden: false },
        { id: 3, name: 'do cool thing 3', func: 'cool_thing_3', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 4, func: 'no-name-bitches', filtered: false, description: 'I don\'t have a fuckin name bitches!', dispatched: false, hidden: false },
        { id: 5, name: 'do cool thing 4', func: 'cool_thing_4', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 6, name: 'do cool thing 5', func: 'cool_thing_5', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 7, name: 'do cool thing 6', func: 'cool_thing_6', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 8, name: 'do cool thing 7', func: 'cool_thing_7', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 9, name: 'do cool thing 8', func: 'cool_thing_8', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 10, name: 'do cool thing 9', func: 'cool_thing_9', filtered: false, description: 'so chill', dispatched: false, hidden: false },
        { id: 11, name: 'do cool thing 10', func: 'cool_thing_10', filtered: false, description: 'so chill', dispatched: false, hidden: false },
      ],
    }
  }

  automationsFilter(filter) {
    this.setState((prevState) => {
      const pattern = new RegExp(filter)
      const updatedAutomations = prevState.automations.map((e) => {
        if (filter.length < 1) {
          return { ...e, filtered: false }
        } else if (
            pattern.test(e.name) ||
            pattern.test(e.func) ||
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
