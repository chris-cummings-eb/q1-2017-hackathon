// @flow
import 'babel-polyfill'
import React from 'react'
import { Divider, Header, Icon } from 'semantic-ui-react'

const readmeURL = 'https://github.com/chris-cummings-eb/q1-2017-hackathon/blob/master/eb_automation_lib/HowToCreateAutomations.md'

const Title = () => (
  <div style={{ textAlign: 'center' }}>
    <Header as="h2" icon>
      <Icon name="settings" />
      Eventbrite Automator
      <Header.Subheader>
        Click on an automation to run it.<br />
        Learn how to <a href={readmeURL} target="_blank">create your own automations.</a>
      </Header.Subheader>
    </Header>
    <Divider />
  </div>
)

export default Title
