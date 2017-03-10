import 'babel-polyfill'
import React, { Component } from 'react'

import { inArray } from '../utils/utils'

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
      tags: [],
    }
  }

  componentDidMount() {
    this.socket.on('automations_list_update', (data) => {
      this.setState(prevState => ({ ...prevState, ...data }))
      this.automationsFilter()
    })
    this.socket.on('clipboard', (data) => {
      this.setState(prevState => ({ ...prevState, ...data }))
      this.automationsFilter()
    })
  }

  automationsFilter(filter = '') {
    if (filter.length < 1 && this.state.tags.length > 0) {
      // if no search value, show relevant automations by tag matches clipboard contents
      const { automations, tags } = this.state
      const updatedAutomations = automations.map((e) => {
        if (e.tags.filter(tag => inArray(tag, tags)).length > 0) {
          return { ...e, filtered: false }
        }
        return { ...e, filtered: true }
      })
      this.setState({ automations: updatedAutomations })
    } else {
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
  }

  handleItemClick(itemID) {
    const { automations } = this.state
    const updatedAutomations = automations.map(e => (
      e.id === itemID ? { ...e, dispatched: true } : { ...e }
    ))

    this.setState(prevState => ({ ...prevState, automations: updatedAutomations }))

    const toDispatch = updatedAutomations.filter(e => e.dispatched)
    if (toDispatch.length > 0) {
      this.socket.emit('dispatch', { automations: [...toDispatch] })
    }
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
