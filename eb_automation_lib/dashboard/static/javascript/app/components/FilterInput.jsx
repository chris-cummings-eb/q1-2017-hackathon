import 'babel-polyfill'
import React, { PropTypes } from 'react'
import { Divider, Input } from 'semantic-ui-react'

const FilterInput = props => (
  <div>
    <Input
      fluid
      icon="filter"
      onChange={props.onChange}
      placeholder="find an automation..."
      size="big"
    />
    <Divider />
  </div>
)

FilterInput.propTypes = {
  onChange: PropTypes.func.isRequired,
}

export default FilterInput
