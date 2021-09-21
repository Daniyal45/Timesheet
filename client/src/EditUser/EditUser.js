import React, { Component } from 'react';
import { HashRouter as Router, Route, Link } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import { SERVER } from './../assets/scripts/constants';


export default class AddUser extends Component {

    constructor(props) {
        super(props)

        this.state = {
            uid: "",
            name: "",
            email: "",
            contact: "",
            designation: "",
            password: "",
            cpassword: "",
            reset_pwd: false
        }
    }

    componentDidMount() {
        const { uid } = this.props.match.params;
        this.setState({ uid }, () => {
            this.getUserInfo();
        })
    }

    _goBack() {
        window.location.hash = "#/users"
    }

    _toggleRstPwd() {
        this.setState({ reset_pwd: true })
    }

    getUserInfo() {
        let API = SERVER + '/getUser'
        var formData = new FormData();
        formData.append('uid', this.state.uid);
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
                        email: response.data[0].email,
                        contact: response.data[0].contact,
                        designation: response.data[0].designation,
                    })
                }
            }
            else {
                toast.error(response.msg);
            }
        })
    }

    handleInput(e) {
        this.setState({ [e.target.name]: e.target.value });
    }

    submitUser(e) {
        e.preventDefault();
        let API = SERVER + '/editUser'
        var formData = new FormData();
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        formData.append('uid', this.state.uid);
        formData.append('name', this.state.name);
        formData.append('contact', this.state.contact);
        formData.append('email', this.state.email);
        formData.append('designation', this.state.designation);
        if (this.state.reset_pwd) {
            if (this.state.password !== this.state.cpassword || this.state.password === "") {
                toast.error("Password fields do not match");
                return;
            }
            else
                formData.append('password', this.state.password);
        }
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        }).then(res => res.json()).then(response => {
            if (parseInt(response.success)) {
                toast.success("User updated successfully");
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
                    <form id="newUserForm" className="custom-input-form" onSubmit={e => this.submitUser(e)}>
                        <h2> Edit User </h2>
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
                        <select
                            id="designation"
                            onChange={e => this.handleInput(e)}
                            name="designation"
                            placeholder="Designation"
                            value={this.state.designation}
                        >
                            <option value="" disabled> Designation </option>
                            <option value="manager"> Manager </option>
                            <option value="employee"> Employee </option>
                        </select>
                        {!this.state.reset_pwd ?
                            <div
                                className="btn btn-primary" style={{ margin: '2% 0%', width: "90%" }}
                                onClick={this._toggleRstPwd.bind(this)}
                            >
                                Reset Password
                            </div>
                            :
                            ""
                        }
                        {this.state.reset_pwd ?
                            <>
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
                            </>
                            :
                            ""
                        }
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
