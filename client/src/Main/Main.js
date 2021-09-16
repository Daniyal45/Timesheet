import React, { Component } from 'react';
import {HashRouter as Router, Route, Link} from 'react-router-dom';
import Logo from './../assets/images/logo.svg';
import toast, { Toaster } from 'react-hot-toast';

import Loader from './../../src/assets/images/load.gif';


import { SERVER } from './../assets/scripts/constants';
// import Timesheets from './../Timesheets/Timesheets';
import MenuScreen from './../MenuScreen/MenuScreen';
import Users from './../Users/Users';
import AddUser from './../AddUser/AddUser';
import EditUser from './../EditUser/EditUser';
import Projects from './../Projects/Projects';
import AddProject from '../AddProject/AddProject';
import EditProject from '../EditProject/EditProject';
import Timesheets from '../Timesheets/Timesheets';
import CreateSheet from '../CreateSheet/CreateSheet';

export default class Main extends Component {
    constructor(props) {
        super(props)    
        this.state = { 
            isAdmin:false,
            loading:true,      
        }
    }
   
    componentDidMount(){
        let API = SERVER+'/permissionGet';
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        myHeaders.append("Content-Type", "application/json");        
        fetch(API, {
            method:'GET',
            headers: myHeaders
        }).then(res => res.json()).then(response => {
            if(parseInt(response.success))
                this.setState({
                    isAdmin: !Boolean(Number(response.type)),
                    loading: false
                })
        })
    }

    HomeScreen(){
        return(
            <div>
          
            </div>
        )
    }

    render() {
        return (
            <div className="main">
                <Router>
                    {this.state.loading ?
                        <div className="lds-dual-ring"></div>
                        :
                        <>
                            <Route exact path="/"
                                render={(props) => (<MenuScreen isAdmin={this.state.isAdmin} />)}
                            />
                            <Route exact path="/timesheets" 
                                render={(props) => (<Timesheets isAdmin={this.state.isAdmin} />)}
                            />
                            <Route path="/createSheet" component={CreateSheet} />                            
                            {this.state.isAdmin ?
                                <>
                                    <Route path="/users" component={Users} />
                                    <Route path="/addUser" component={AddUser} />
                                    <Route path="/editUser/:uid" component={EditUser} />
                                    <Route path="/projects" component={Projects} />
                                    <Route path="/addProject" component={AddProject} />
                                    <Route path="/editProject/:pid" component={EditProject} />
                                </>
                                : 
                                ""
                            }
                        </>
                    }
                </Router>
            </div>
        )
    }
}
