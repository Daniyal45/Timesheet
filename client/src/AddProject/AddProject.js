import React, { Component } from 'react';

import { HashRouter as Router, Route, Link } from 'react-router-dom';
import { AnalogTime } from 'react-clock-select';
import toast, { Toaster } from 'react-hot-toast';
import Table from 'react-table-lite';

import { SERVER } from './../assets/scripts/constants';


export default class AddProject extends Component {

    constructor(props) {
        super(props)

        this.state = {
            name: "",
            start_date: "",
            end_date: "",
            status: "",          
        }
    }

    handleInput(e){
        this.setState({ [e.target.name] : e.target.value });
    }

    submitProject(e) {
        e.preventDefault();
        let API = SERVER + '/addProject'
        var formData = new FormData();
        formData.append('name', this.state.name);
        formData.append('start_date', this.state.start_date);
        formData.append('end_date', this.state.end_date);
        formData.append('status', this.state.status);
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        }).then(res => res.json()).then(response => {            
            if (parseInt(response.success)) {
                toast.success("Project created successfully");
            }
            else {
                toast.error(response.msg);
            }
        })

    }

    _goBack(){
        window.location.hash = "#/projects"
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

    ProjectForm = () => {
        return (
            <div className="padded-section">
                <div className="center-card-input">
                    <form id="newProjectForm" className="custom-input-form" onSubmit={e=>this.submitProject(e)}>
                        <h2> Add Project </h2>
                        <input
                            id="name"
                            onChange={e => this.handleInput(e)}
                            name="name"
                            placeholder="Project name..."
                            value={this.state.name}
                            required={true}
                            maxLength={20}
                        />
                        <input
                            id="start_date"
                            onChange={e => this.handleInput(e)}
                            name="start_date"                            
                            placeholder="Start Date"
                            value={this.state.start_date}
                            required={true}
                            onFocus={e=>e.target.type = "date"}
                            onBlur={e=>e.target.type = "text"}
                        />
                        <input
                             id="end_date"
                             onChange={e => this.handleInput(e)}
                             name="end_date"                            
                             placeholder="End Date"
                             value={this.state.end_date}                             
                             onFocus={e=>e.target.type = "date"}
                             onBlur={e=>e.target.type = "text"}
                        />
                        <select
                             id="status"
                             onChange={e => this.handleInput(e)}
                             name="status"                                                        
                             value={this.state.status}                                        
                        >
                            <option value={""} disabled> Status </option> 
                            <option value={1}> On going </option>
                            <option value={2}> On Hold </option>
                            <option value={3}> Closed </option>
                        </select>   

                     
                        <button style={{margin: '0 5%', width:"95px"}} className="btn btn-primary flt-right" type="submit"> Save </button>                    
                    </form>
                </div>
            </div>
        )
    }

    render() {



        return (
            <>
                {this.TopBar()}                
                <div className="container">
                    <div className="row">                        
                        <div className="col-md-12 col-sm-12 col-lg-12">
                            {this.ProjectForm()}
                        </div>
                    </div>
                </div>
                <Toaster toastOptions={{className: 'Toast_Class'}}/>
            </>
        )
    }
}
