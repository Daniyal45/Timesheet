import React, { Component } from 'react';
import {HashRouter as Router, Route, Link} from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import Table from 'react-table-lite';

import { SERVER } from './../assets/scripts/constants';
export default class Projects extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             projects:[]
        }
    }
    
    componentDidMount(){
        this.getProjects();
    }

    _goBack(){
        window.location.hash = "#/"
    }

    getProjects(){        
        let API = SERVER + '/getProjects' ;
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        myHeaders.append("Content-Type", "application/json");        
        fetch(API, {
            method: 'GET',
            headers: myHeaders,            
        }).then(res => res.json()).then(response => {
            if(parseInt(response.success)){
                this.setState({projects: response.data});
            }
            else{
                toast.error(response.msg);
            }
        })
    }

    TopBar(){
        return(
            <div className="container-fluid">
                <div className="row top-bar">
                    <button onClick={()=>this._goBack()} className="btn btn-primary mgn-lf"> ← Go Back </button>
                </div>
            </div>
        )
    }

    _switchToEditScreen(e, row) {
        window.location.hash = '#/editProject/'+row.id;
    }

    TableView(){
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-12 col-sm-12 col-lg-12">
                        <div className="padded-section">
                            <Link to="addProject" replace>
                                <button className="btn btn-primary flt-right mgn-bt"> Add Project </button>
                            </Link>
                            <Table
                                data={this.state.projects}
                                header={["name","start_date","end_date","status"]}
                                sortBy={["name","start_date","status"]}
                                customHeaders={{"start_date":"Start Date", "end_date":"End Date"}}
                                dataStyle={{color:"white"}}
                                showActions = {true}        
                                actionTypes={["edit"]}
                                onRowEdit = {(event, row) => { 
                                    this._switchToEditScreen(event,row)
                                }} 
                                headerStyle={{background:'#4a77d4',textShadow: "0 -1px 0 rgba(0, 0, 0, 0.25)", color: "#ffffff"}}
                            />
                        </div>
                    </div>
                </div>
            </div>
        )
    }
    render() {
        return (
            <div className="Users">
                {this.TopBar()}
                {this.TableView()}
                <Toaster toastOptions={{className: 'Toast_Class'}}/>
            </div>
        )
    }
}
