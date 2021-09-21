import React from 'react';
import toast, { Toaster } from 'react-hot-toast';
import { SERVER } from './../assets/scripts/constants';


export default class Reports extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            user: '',
            project: '',
            start_date:'',
            end_date:'',
            dbUsers: [],
            dbProjects: []
        }
    }

    componentDidMount = () => {
        this.initScreen();
    }

    initScreen = () => {
        let API = SERVER + '/getProjects';
        var myHeaders = new Headers();
        var dbProjects = [];
        myHeaders.append("Authorization", localStorage.getItem('token'));
        myHeaders.append("Content-Type", "application/json");
        fetch(API, {
            method: 'GET',
            headers: myHeaders,
        }).then(res => res.json()).then(response => {
            if (parseInt(response.success)) {
                dbProjects = response.data;
                API = SERVER + '/getUsers';
                fetch(API, {
                    method: 'GET',
                    headers: myHeaders,
                }).then(res => res.json()).then(response => {
                    if (parseInt(response.success)) {
                        let users = response.data.filter(user=>{return user.designation!=="manager"})
                        this.setState({
                            dbUsers: users,
                            dbProjects: dbProjects
                        });
                    }
                    else {
                        toast.error(response.msg);
                    }
                })
            }
            else {
                toast.error(response.msg);
            }
        })
    }

    _goBack = () => {
        window.location.hash = "#/"
    }

    _handleFilterChange = (e) => {
        this.setState({
            [e.target.name] : e.target.value
        })
    }

    _requestGenerateReport = (e) => {
        e.preventDefault();
        let API = SERVER + '/generateReport'
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        var formData = new FormData(document.getElementById('report-filters'))
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        }).then(res => res.blob()).then(blob => URL.createObjectURL(blob))
            .then(uril => {
                var link = document.createElement("a");
                link.href = uril;
                link.download = "Report" + ".xlsx";                                                         
                var event = new MouseEvent('click', {
                    'view': window,
                    'bubbles': false,
                    'cancelable': true
                });
               link.dispatchEvent(event);
            })
            .catch(err=>{
                toast.error("Process Failed");
            });

    }

    TopBar = () => {
        return (
            <div className="container-fluid">
                <div className="row top-bar">
                    <button onClick={() => this._goBack()} className="btn btn-primary mgn-lf"> ← Go Back </button>
                </div>
            </div>
        )
    }

    ReportFilters = () => {
        return (
            <div className="filter-card">
                <form 
                    id="report-filters"
                    className="custom-input-form" 
                    onSubmit={this._requestGenerateReport.bind(this)}
                > 
                    <label> Filter </label>                   
                    <select 
                        name="user" 
                        id="user" 
                        onChange={e=>this._handleFilterChange(e)}
                        value={this.state.user} 
                        required={true}                        
                    >
                        <option disabled value=""> select user </option>
                        <option value="-3"> All </option>
                        {this.state.dbUsers.length ?
                            this.state.dbUsers.map((user, key) => (
                                <option key={key} value={user.id}>{user.name}</option>
                            ))
                            :
                            ""
                        }
                    </select>                    
                    <select 
                        name="project" 
                        id="projects" 
                        required={true}
                        onChange={e=>this._handleFilterChange(e)}
                        value={this.state.project}
                    >
                        <option disabled value=""> select project </option>
                        <option value="-3"> All </option>
                        {this.state.dbProjects.length ?
                            this.state.dbProjects.map((project, key) => (
                                <option key={key} value={project.id}>{project.name}</option>
                            ))
                            :
                            ""
                        }
                    </select>
                    <label> Date Range </label>
                   <div className="date-range-div">
                        <input 
                            onChange={e=>this._handleFilterChange(e)}
                            type="date" 
                            name="start_date" 
                        />
                        <input 
                            onChange={e=>this._handleFilterChange(e)}
                            type="date" 
                            name="end_date" 
                        />
                   </div>
                   <button type="submit" className="btn btn-primary report-generate-btn"> Download </button>
                </form>
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.TopBar()}
                {this.ReportFilters()}
                <Toaster toastOptions={{className: 'Toast_Class'}}/>
            </div>
        )
    }
}