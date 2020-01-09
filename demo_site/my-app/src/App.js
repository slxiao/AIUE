import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function range(size, startAt = 0) {
  return [...Array(size).keys()].map(i => i + startAt);
}

class ChildPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
    <h2>ChildPage: {this.props.index}</h2>
    )
  }
}

class Links extends Component {
  constructor(props) {
    super(props);
  }
  
  render() {
    
    return (
      <div>
      <Router>
        <div>
        <nav>
        {
          this.props.indices.map((item) => 
            <div>
              <Link to={"/link" + item}>Link: {item}</Link>
            </div>
          )
        }
        </nav>

      <Switch>
        {
          this.props.indices.map((item) =>
          <Route path={"/link" + item}> 
            {
              item < 1000 ? <Links indices={range(9, 10*item)} /> : <h2>end</h2>
            }
            
          </Route>
          )
        }
        
      </Switch>
    </div>
    </Router>
    </div>
    )
  }
}

class App extends Component {
  render() {
    const indices = range(9, 1)

    return (
     <Links indices={indices} />
    );
  }
}

export default App;
