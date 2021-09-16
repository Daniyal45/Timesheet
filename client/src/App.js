
import React, { Component } from 'react'
import Login from './Login/Login';
import Main from './Main/Main';
import './assets/css/grid.min.css';
import './assets/css/App.css';

export default class App extends Component {

    constructor(props) {
        super(props)

        this.state = {
            loggedIn: false
        }
    }

    componentDidMount() {
        if (localStorage.getItem('token'))
            this.setState({ loggedIn: true })
        else
            this.setState({ loggedIn: false })
    }

    render() {
        return (
            <div>
                {
                    this.state.loggedIn ?
                        <Main />
                        :
                        <Login />
                }
            </div>
        )
    }
}


