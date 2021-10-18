import React, { Component } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import { SERVER } from './../assets/scripts/constants';
import '../assets/css/grid.min.css';


export default class ViewTimeSheet extends Component {

    constructor(props) {
        super(props)
        this.state = {
            tasks: [],
        }
    }

    componentDidMount() {
        this.getSheetInfo();
    }

    _goBack() {
        window.location.hash = "#/timesheets"
    }

    getSheetInfo() {
        let API = SERVER + '/getTimesheet';
        const { sid } = this.props.match.params;
        var formData = new FormData();
        formData.append("sid", sid);
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        fetch(API, {
            method: 'POST',
            body: formData,
            headers: myHeaders,
        }).then(res => res.json()).then(response => {
            if (parseInt(response.success)) {
                let tasks = response.data.length ? response.data : []
                this.setState({ tasks })
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
                        <span>Time Sheet</span>
                    </h2>
                </div>
                {this.Tasks()}
            </div>
        )
    }

    Tasks() {
        return (
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
                                            value={task.task}
                                            disabled={true}
                                            onChange={e => { }}
                                        />
                                    </div>
                                    <div className="col-md-3 col-sm-6">
                                        <input
                                            name="project"
                                            placeholder="project"
                                            value={task.project}
                                            disabled={true}
                                            onChange={e => { }}
                                        />
                                    </div>
                                    <div className="col-md-3 col-sm-6">
                                        <input
                                            name="hours"
                                            placeholder="hours"
                                            value={task.hours}
                                            disabled={true}
                                            onChange={e => { }}
                                        />
                                    </div>
                                    <div className="col-md-3 col-sm-6" >
                                        <select
                                            name="status"
                                            value={task.status}
                                            disabled={true}
                                            onChange={e => { }}
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
                                            disabled={true}
                                            onChange={e => { }}
                                        />
                                    </div>
                                </div>
                            </div>
                        )
                    })
                    :
                    ""
                }
            </div>
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
