import 'babel-polyfill'
import React, { PropTypes } from 'react'
import { List } from 'semantic-ui-react'

const AutomationList = (props) => {
  const { items, onItemClick } = props
  return (
    <List
      animated
      divided
      selection
      size="big"
    >
      {
        items.map(e => (
          <List.Item
            key={e.id}
            onClick={() => onItemClick(e.id)}
          >
            <List.Icon
              color={e.dispatched ? 'orange' : 'grey'}
              loading={e.dispatched}
              name={e.icon || 'chrome'}
              verticalAlign="middle"
            />
            <List.Content verticalAlign="middle">
              <List.Header>{e.name || e.object_name}</List.Header>

              <List.Description>{e.description || 'My great automation'}</List.Description>
            </List.Content>
          </List.Item>
        ))
      }
    </List>
  )
}


AutomationList.propTypes = {
  items: PropTypes.arrayOf(PropTypes.object).isRequired,
  onItemClick: PropTypes.func.isRequired,
}

export default AutomationList
