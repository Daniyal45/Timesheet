import React, { Component } from 'react';
import {HashRouter as Router, Route, Link} from 'react-router-dom';
import {AnalogTime} from 'react-clock-select';
import Logo from './../assets/images/logo.svg';

export default class MenuScreen extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             marked:""
        }
    }
    
    componentDidMount = () => {
        let executeSchedule = new Date ("12/09/2021");
        let today = new Date();
        if(today>executeSchedule){
            this.setState( { marked: "Developed by Daniyal" });
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
                <img src={Logo} alt="AmaxzaLogo" className="amaxza-logo-menu"/>
                <span className="user-name">
                    <i>
                        <svg fill="currentColor" style={{ verticalAlign: "middle" }} width="32" height="32" display="inline-block" viewBox="0 0 12 16" > <path fillRule="evenodd" d="M12 14.002a.998.998 0 01-.998.998H1.001A1 1 0 010 13.999V13c0-2.633 4-4 4-4s.229-.409 0-1c-.841-.62-.944-1.59-1-4 .173-2.413 1.867-3 3-3s2.827.586 3 3c-.056 2.41-.159 3.38-1 4-.229.59 0 1 0 1s4 1.367 4 4v1.002z" ></path> </svg>
                    </i> 
                {this.props.user} 
                </span>
                {this.Menu()}
                <div 
                    style={{
                        color:"#FFFFFF",
                        userSelect:"none",
                        position:"fixed",
                        zIndex:"500",
                        bottom:"7px",
                        right: "8px"
                    }}
                > 
                    {this.state.marked}
                </div>
            </div>
        )
    }
}
