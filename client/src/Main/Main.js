import React, { Component } from 'react';
import {HashRouter as Router, Route, Switch} from 'react-router-dom';
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
import ViewTimeSheet from '../ViewTimeSheet/ViewTimeSheet';
import Reports from '../Reports/Reports';
import NotFound from '../NotFound/NotFound';

export default class Main extends Component {
    constructor(props) {
        super(props)    
        this.state = { 
            isAdmin:false,
            loading:true,    
            user_name: "",  
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
                    user_name : response.user.name,
                    loading: false
                })
            else{
                toast.error(response.msg);
                setTimeout(()=>{
                    localStorage.clear(); 
                    window.location.reload(1);
                },2500);
            }

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
                                render={(props) => (<MenuScreen isAdmin={this.state.isAdmin} user={this.state.user_name} />)}
                            />

                            <Route exact path="/timesheets"
                                render={(props) => (<Timesheets isAdmin={this.state.isAdmin} />)}
                            />

                            <Route exact path="/timesheet/:sid" component={ViewTimeSheet} />

                            {this.state.isAdmin ?
                                <>
                                    <Route exact path="/users" component={Users} />
                                    <Route exact path="/addUser" component={AddUser} />
                                    <Route exact path="/editUser/:uid" component={EditUser} />
                                    <Route exact path="/projects" component={Projects} />
                                    <Route exact path="/addProject" component={AddProject} />
                                    <Route exact path="/editProject/:pid" component={EditProject} />
                                    <Route exact path="/reports" component={Reports} />
                                </>
                                :
                                <Route exact path="/createSheet" component={CreateSheet} />
                            }
                            <Route exact path="*" component={NotFound} />
                        </>
                    }
                </Router>
                <Toaster toastOptions={{ className: 'Toast_Class' }} />
            </div >
        )
    }
}
