import React, { Component } from 'react';
import Logo from './../assets/images/logo.svg';
import toast, { Toaster } from 'react-hot-toast';
import './../assets/css/login.min.css';

import { SERVER } from './../assets/scripts/constants';

export default class Login extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
             email:"",
             password:"",
        }
    }

    _handleLogin(e){
        e.preventDefault();
        let API = SERVER + '/login'
        var formData = new FormData(document.getElementById('LoginForm'));
        fetch(API, {
            method: 'POST',
            body: formData,
        }).then(res => res.json()).then(response => {
            if(parseInt(response.success)){
                localStorage.setItem("token",response.token);
                window.location.reload(1);
            }
            else{
                toast.error(response.msg);
            }
        })
    }

    _handleInput(e){
        this.setState({ [e.target.name] : e.target.value })
    }
    
    render() {
        return (
            <div className="login">                
                <img src={Logo} alt="Timesheet Login" />
                <form  onSubmit={this._handleLogin.bind(this)} id="LoginForm" >
                    <input onChange={e=>this._handleInput(e)} type="text" name="email" placeholder="Email" required="required" />
                    <input onChange={e=>this._handleInput(e)}  type="password" name="password" placeholder="Password" required="required" />
                    <button type="submit" className="btn btn-primary btn-block btn-large">Sign in.</button>
                </form>
                <Toaster toastOptions={{className: 'Toast_Class'}}/>
            </div>
        )
    }
}
