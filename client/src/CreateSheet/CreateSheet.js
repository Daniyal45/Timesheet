import React, { Component } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import { SERVER } from './../assets/scripts/constants';
import '../assets/css/grid.min.css';

var task_count = 0;
export default class CreateSheet extends Component {

    constructor(props) {
        super(props)

        this.state = {
            sheetID:"",
            tasks: [],
            projects: [],
            editExistingSheet:0,
            date: new Date().toISOString().slice(0, 10)
        }
    }

    componentDidMount() {
        this.initSheet();
    }

    _goBack() {
        window.location.hash = "#/"
    }

    _handleNewTaskAdd() {
        let new_task = {};
        new_task.id = task_count + 1;
        task_count++;
        new_task.comment = "";
        new_task.pid = "";
        new_task.name = "";
        new_task.sid = "";
        new_task.pid = "";
        new_task.hours = "";
        new_task.status = "";
        let tasks = [...this.state.tasks];
        tasks.push(new_task);
        this.setState({ tasks });
    }

    _handleTaskChange(id, e) {
        let tasks = [...this.state.tasks];
        tasks.forEach((task) => {
            if (task.id === id) {
                task[e.target.name] = e.target.value;
            }
        });
        this.setState({ tasks });
    }

    _handleNewTaskRemove(id, e) {
        let tasks = [...this.state.tasks];
        let remainingTasks = [];
        remainingTasks = tasks.filter((task) => { return task.id !== id })
        this.setState({ tasks: remainingTasks });
    }


    initSheet() {
        let API = SERVER + '/initTimesheet';
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        myHeaders.append("Content-Type", "application/json");
        fetch(API, {
            method: 'GET',
            headers: myHeaders,
        }).then(res => res.json()).then(response => {
            if (parseInt(response.success)) {
                this.setState({
                    date: response.data.date,
                    projects: response.data.projects,
                    tasks: response.data.existingTaskSheet,
                    editExistingSheet: response.data.editExistingSheet,
                    sheetID: response.data.sheetId
                });
                if(response.data.existingTaskSheet.length)
                    task_count = Math.max.apply(Math, response.data.existingTaskSheet.map(function(tsk) { return tsk.id; }));                   
            }
            else {
                toast.error(response.msg);
            }
        })
    }

    _submitSheet(e) {
        e.preventDefault();
        let API = SERVER + '/newSheet'
        var formData = new FormData();
        var myHeaders = new Headers();
        formData.append('tasks', JSON.stringify(this.state.tasks));
        formData.append('date', this.state.date);
        if(this.state.editExistingSheet){
            API = SERVER + '/editSheet'
            formData.append('sid', this.state.sheetID);
        }     
        myHeaders.append("Authorization", localStorage.getItem('token'));
        fetch(API, {
            method: 'POST',
            headers: myHeaders,
            body: formData,
        })
            .then(res => res.json()).then(response => {
                if (parseInt(response.success)) {
                    toast.success("Sheet submitted successfully");
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



    SheetView() {
        return (
            <div className="container">
                <div className="padded-section">
                    <h2 className="page-title">
                        <i className="icon-c">
                            <svg fill="currentColor" style={{ display: 'inline-block', verticalAlign: 'middle' }} height={32} width={32} viewBox="0 0 16 16"><path d="M5 6h2v2h-2zM8 6h2v2h-2zM11 6h2v2h-2zM2 12h2v2h-2zM5 12h2v2h-2zM8 12h2v2h-2zM5 9h2v2h-2zM8 9h2v2h-2zM11 9h2v2h-2zM2 9h2v2h-2zM13 0v1h-2v-1h-7v1h-2v-1h-2v16h15v-16h-2zM14 15h-13v-11h13v11z" /></svg>
                        </i>
                        <span>Today's Sheet</span>
                    </h2>
                </div>
                {this.Tasks()}
                <div className="row">
                    <div className="col-md-12 col-sm-12 col-lg-12">
                        <div className="padded-section">
                            {this.state.tasks.length ?
                                <button type="submit" form="task-sheet-form" className="btn btn-primary flt-right mgn-bt sm-margin"> Save </button>
                                :
                                ""
                            }
                            <button onClick={this._handleNewTaskAdd.bind(this)} className="btn btn-primary flt-right mgn-bt"> Add Task </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    Tasks() {
        return (
            <form id="task-sheet-form" onSubmit={this._submitSheet.bind(this)}>
                <div className="add-tasks">
                    {this.state.tasks.length ?
                        this.state.tasks.map((task, index_1) => {
                            return (
                                <div key={index_1} >
                                    <div className="row">
                                        <div className="col-md-3 col-sm-6">
                                            <input
                                                name="name"
                                                placeholder="name"
                                                value={task.name}
                                                required={true}
                                                onChange={this._handleTaskChange.bind(this, task.id)}
                                            />
                                        </div>
                                        <div className="col-md-3 col-sm-6">
                                            <select
                                                name="pid"
                                                value={task.pid}
                                                required={true}
                                                onChange={this._handleTaskChange.bind(this, task.id)}
                                            >
                                                <option value={""} disabled> Project </option>
                                                {this.state.projects.length ?
                                                    this.state.projects.map((project, index_2) => (
                                                        <option key={index_2} value={project.id}>{project.name}</option>
                                                    ))
                                                    :
                                                    ""
                                                }
                                            </select>
                                        </div>
                                        <div className="col-md-3 col-sm-6">
                                            <input
                                                name="hours"
                                                type="number"
                                                placeholder="hours"
                                                value={task.hours}
                                                required={true}
                                                onChange={this._handleTaskChange.bind(this, task.id)}
                                            />
                                        </div>
                                        <div className="col-md-3 col-sm-6" >
                                            <select
                                                required={true}
                                                name="status"
                                                value={task.status}
                                                onChange={this._handleTaskChange.bind(this, task.id)}
                                            >
                                                <option value={""} disabled> Status </option>
                                                <option value={1}> In Progress </option>
                                                <option value={2}> Complete </option>
                                                <option value={3}> On Hold </option>
                                                <option value={4}> Need to Discuss </option>
                                            </select>
                                        </div>
                                        <div className="col-md-3 col-sm-6">
                                            <input

                                                name="comment"
                                                type="text"
                                                placeholder="comments"
                                                value={task.comment}
                                                onChange={this._handleTaskChange.bind(this, task.id)}
                                            />
                                        </div>
                                        <div>
                                            <i className="icon-c delete" onClick={this._handleNewTaskRemove.bind(this, task.id)}>
                                                <svg fill="currentColor" style={{ display: 'inline-block', verticalAlign: 'middle' }} height={32} width={32} viewBox="0 0 20 20"><path d="M14.348,14.849c-0.469,0.469-1.229,0.469-1.697,0L10,11.819l-2.651,3.029c-0.469,0.469-1.229,0.469-1.697,0c-0.469-0.469-0.469-1.229,0-1.697l2.758-3.15L5.651,6.849c-0.469-0.469-0.469-1.228,0-1.697c0.469-0.469,1.228-0.469,1.697,0L10,8.183l2.651-3.031c0.469-0.469,1.228-0.469,1.697,0c0.469,0.469,0.469,1.229,0,1.697l-2.758,3.152l2.758,3.15C14.817,13.62,14.817,14.38,14.348,14.849z" /></svg>
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            )
                        })
                        :
                        ""
                    }
                </div>
            </form>
        )
    }

    render() {
        return (
            <div className="Timesheet">
                {this.TopBar()}
                {this.SheetView()}
                <Toaster toastOptions={{ className: 'Toast_Class' }} />
            </div>
        )
    }
}
