import React, { Component } from 'react';

import { HashRouter as Router, Route, Link } from 'react-router-dom';
import { AnalogTime } from 'react-clock-select';
import toast, { Toaster } from 'react-hot-toast';
import Table from 'react-table-lite';

import { SERVER } from './../assets/scripts/constants';


export default class AddUser extends Component {

    constructor(props) {
        super(props)

        this.state = {
            name: "",
            email: "",
            contact: "",
            designation: "",
            password: "",
            cpassword: "",
        }
    }

    handleInput(e){
        this.setState({ [e.target.name] : e.target.value });
    }

    submitUser(e) {
        e.preventDefault();
        if (this.state.password !== this.state.cpassword || this.state.password === "") {
            toast.error("Password fields do not match");
        }
        else {            
            let API = SERVER + '/addUser'
            var formData = new FormData();
            formData.append('name',this.state.name);
            formData.append('contact',this.state.contact);
            formData.append('email',this.state.email);
            formData.append('designation',this.state.designation);
            formData.append('password',this.state.password);
            var myHeaders = new Headers();
            myHeaders.append("Authorization", localStorage.getItem('token'));                    
            fetch(API, {
                method: 'POST',
                headers: myHeaders, 
                body: formData,
            }).then(res => res.json()).then(response => {                
                if (parseInt(response.success)) {
                    toast.success("User created successfully");
                }
                else {
                    toast.error(response.msg);
                }
            })

        }
    }

    _goBack(){
        window.location.hash = "#/users"
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

    UserForm = () => {
        return (
            <div className="padded-section">
                <div className="center-card-input">
                    <form id="newUserForm" className="custom-input-form" onSubmit={e=>this.submitUser(e)}>
                        <h2> Add User </h2>
                        <input
                            id="name"
                            onChange={e => this.handleInput(e)}
                            name="name"
                            placeholder="User name..."
                            value={this.state.name}
                            required={true}
                        />
                        <input
                            id="email"
                            onChange={e => this.handleInput(e)}
                            name="email"
                            placeholder="User email..."
                            value={this.state.email}
                            required={true}
                        />
                        <input
                            id="contact"
                            onChange={e => this.handleInput(e)}
                            name="contact"
                            placeholder="User contact..."
                            value={this.state.contact}
                        />
                        <input
                            id="designation"
                            onChange={e => this.handleInput(e)}
                            name="designation"
                            placeholder="Designation"
                            value={this.state.designation}
                        />
                        <input
                            id="password"
                            type="password"
                            onChange={e => this.handleInput(e)}
                            name="password"
                            placeholder="Enter Password..."
                            value={this.state.password}
                        />
                    
                        <input
                            type="password"
                            onChange={e => this.handleInput(e)}
                            name="cpassword"
                            placeholder="Confirm Password..."
                            value={this.state.cpassword}
                        />    
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
                            {this.UserForm()}
                        </div>
                    </div>
                </div>
                <Toaster toastOptions={{className: 'Toast_Class'}}/>
            </>
        )
    }
}
