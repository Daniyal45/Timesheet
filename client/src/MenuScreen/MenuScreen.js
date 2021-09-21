import React, { Component } from 'react';
import {HashRouter as Router, Route, Link} from 'react-router-dom';
import {AnalogTime} from 'react-clock-select';

export default class MenuScreen extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             
        }
    }
    
    logout = (e) => {
        localStorage.clear();
        window.location.reload(1);
    }
    
    Menu = () => (
        <div className="center">
            <AnalogTime
                type={"display"}
                size={1.2}
                value={new Date()}
                liveUpdater={true}
                baseColor={"#FFFFFF"}
                hourHandColor={"#FFFFFF"}
                minuteHandColor={"#FFFFFF"}
                secondHandColor={"red"}
            />
            <Router>
                <ul>
                    {this.props.isAdmin?
                        <>
                            <li>
                                <Link to="users" replace> Users </Link>
                            </li>
                            <li>
                                <Link to="projects" replace> Projects </Link>
                            </li>
                            <li>
                                <Link to="reports" replace> Reports </Link>
                            </li>
                        </>
                        : ""
                    }
                    <li>
                        <Link to="timesheets" replace> Timesheets </Link>
                    </li>
                    {!this.props.isAdmin ?
                        <li>
                            <Link to="createSheet" replace> Today's Timesheet </Link>
                        </li>
                        :
                        ""
                    }
                    <li>
                        <Link to="/" replace onClick={e=>this.logout(e)}> Logout </Link>
                    </li>
                </ul>
            </Router>
        </div>
    )

    render() {
        return (
            <div className="Menu">
                {this.Menu()}
            </div>
        )
    }
}
