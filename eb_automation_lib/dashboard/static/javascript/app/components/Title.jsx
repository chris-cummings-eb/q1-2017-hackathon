// @flow
import 'babel-polyfill'
import React from 'react'
import { Divider, Header, Icon } from 'semantic-ui-react'

const Title = () => (
  <div style={{ textAlign: 'center' }}>
    <Header as="h2" icon>
      <Icon name="settings" />
      Eventbrite Automator
      <Header.Subheader>
        Click on an automation to run. Create your own.
      </Header.Subheader>
    </Header>
    <Divider />
  </div>
)

export default Title
