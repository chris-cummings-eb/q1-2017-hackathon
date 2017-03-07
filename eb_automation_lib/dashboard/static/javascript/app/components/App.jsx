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
      ],
      filter: '',
    }
  }

  automationsFilter() {
    this.setState((prevState) => {
      const { automations, filter } = prevState
      const pattern = new RegExp(filter)

      return (
        automations.map((e) => {
          if (filter.length < 1) {
            return { ...e, filtered: false }
          } else if (pattern.test(e.name) || pattern.test(e.funcc) || pattern.test(e.description)) {
            return { ...e, filtered: false }
          }
          return { ...e, filtered: true }
        })
      )
    })
  }

  handleItemClick(itemID) {
    this.setState(prevState => (
      [...prevState.automations].map((e) => {
        if (e.id === itemID) {
          return { ...e, dispatched: true }
        }
        return { ...e }
      })
    ))
  }

  updateFilter(text) {
    this.setState(prevState => Object.assign({ ...prevState }, { filter: text }))
  }

  render() {
    const { automations, filter } = this.state
    const getVisible = list => list.filter(e => !e.filtered && !e.hidden)

    return (
      <div style={{ padding: '15px' }}>
        <Title />
        <AutomationList
          items={getVisible(automations)}
          onItemClick={itemID => this.handleItemClick(itemID)}
        />
        <FilterInput onChange={(e, d) => this.updateFilter(d.value)} />
      </div>
    )
  }
}

export default App
