import 'babel-polyfill'
import React, { PropTypes } from 'react'
import { List } from 'semantic-ui-react'

const AutomationList = (props) => {
  const { items, onItemClick, iconName } = props
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
            key={'list-item-'.concat(e.id)}
            onClick={() => onItemClick(e.id)}
          >
            <List.Icon
              color={e.dispatched ? 'orange' : 'grey'}
              loading={e.dispatched}
              name={iconName}
              verticalAlign="middle"
            />
            <List.Content verticalAlign="middle">
              <List.Header>{e.name ? e.name : e.func}</List.Header>

              <List.Description>{e.description ? e.description : 'My great automation'}</List.Description>
            </List.Content>
          </List.Item>
        ))
      }
    </List>
  )
}

AutomationList.defaultProps = {
  iconName: 'chrome',
}

AutomationList.propTypes = {
  iconName: PropTypes.string,
  items: PropTypes.arrayOf(PropTypes.object).isRequired,
  onItemClick: PropTypes.func.isRequired,
}

export default AutomationList
