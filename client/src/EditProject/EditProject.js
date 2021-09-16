import React, { Component } from 'react';

import { HashRouter as Router, Route, Link } from 'react-router-dom';
import { AnalogTime } from 'react-clock-select';
import toast, { Toaster } from 'react-hot-toast';
import Table from 'react-table-lite';

import { SERVER } from './../assets/scripts/constants';


export default class EditProject extends Component {

    constructor(props) {
        super(props)

        this.state = {
            pid: "",
            name: "",
            start_date: "",
            end_date: "",
            status: ""
        }
    }

    componentDidMount() {
        const { pid } = this.props.match.params;
        this.setState({ pid }, () => {
            this.getProjectInfo();
        })
    }

    _goBack() {
        window.location.hash = "#/projects"
    }

    _toggleRstPwd() {
        this.setState({ reset_pwd: true })
    }

    getProjectInfo() {
        let API = SERVER + '/getProject'
        var formData = new FormData();
        formData.append('pid', this.state.pid);
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        }).then(res => res.json()).then(response => {
            if (parseInt(response.success)) {
                if (response.data.length) {
                    this.setState({
                        name: response.data[0].name,
                        start_date: response.data[0].start_date.replaceAll("-","/"),
                        end_date: response.data[0].end_date.replaceAll("-","/"),
                        status: response.data[0].status
                    })
                }
            }
            else {
                toast.error(response.msg);
            }
        })
    }

    _bluring(e){
        if(e.target.name.includes("date")){
            let d = this.state[e.target.name];
            d.replace('-','/');
            this.setState({ [e.target.name]: d });
        }
    }

    handleInput(e) {         
        this.setState({ [e.target.name]: e.target.value });
    }

    submitProject(e) {
        e.preventDefault();
        let API = SERVER + '/editProject'
        var formData = new FormData();
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        formData.append('pid', this.state.pid);
        formData.append('name', this.state.name);
        formData.append('start_date', this.state.start_date.replaceAll("-","/"));
        formData.append('end_date', this.state.end_date.replaceAll("-","/"));
        formData.append('status', this.state.status);       
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        }).then(res => res.json()).then(response => {            
            if (parseInt(response.success)) {
                toast.success("Project updated successfully");
            }
            else {
                toast.error(response.msg);
            }
        })
    }

    TopBar() {
        return (
            <div className="container-fluid">
                <div className="row top-bar">
                    <button onClick={() => this._goBack()} className="btn btn-primary mgn-lf"> ← Go Back </button>
                </div>
            </div>
        )
    }

    UserForm = () => {
        return (
            <div className="padded-section">
                <div className="center-card-input">
                    <form id="newProjectForm" className="custom-input-form" onSubmit={e => this.submitProject(e)}>
                        <h2> Edit Project </h2>
                        <input
                            id="name"
                            onChange={e => this.handleInput(e)}
                            name="name"
                            placeholder="Project name..."
                            value={this.state.name}
                            required={true}
                        />
                        <input
                            id="start_date"
                            onChange={e => this.handleInput(e)}
                            name="start_date"
                            placeholder="Start Date"
                            value={this.state.start_date}
                            required={true}
                            onFocus={e => e.target.type = "date"}
                            onBlur={e => {e.target.type = "text"; this._bluring(e)}}
                        />
                        <input
                            id="end_date"
                            onChange={e => this.handleInput(e)}
                            name="end_date"
                            placeholder="End Date"
                            value={this.state.end_date}
                            onFocus={e => e.target.type = "date"}
                            onBlur={e => {e.target.type = "text"; this._bluring(e)}}
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


                        <button style={{ margin: '0 5%', width: "95px" }} className="btn btn-primary flt-right" type="submit"> Save </button>
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
                <Toaster toastOptions={{ className: 'Toast_Class' }} />
            </>
        )
    }
}
