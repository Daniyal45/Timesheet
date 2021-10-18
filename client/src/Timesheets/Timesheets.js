import React, { Component } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import Table from 'react-table-lite';
import { SERVER } from './../assets/scripts/constants';

export default class Timesheets extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             sheets:[],
             page:1,
             totalPages:1
        }
    }
    
    componentDidMount(){
        this.getSheets();
    }

    _goBack(){
        window.location.hash = "#/"
    }

    _switchToViewScreen(event,row){
        window.location.hash = "#/timesheet/"+row.id;
    }

    _handlePageChange(page){
        if(page !== this.state.page)
            this.setState({page},
                ()=>{ this.getSheets(); }
            )
    }

    getSheets(){
        let API = SERVER + '/getTimesheets' ;
        var formData = new FormData();
        var myHeaders = new Headers();
        myHeaders.append("Authorization", localStorage.getItem('token'));
        formData.append('page', this.state.page );
        fetch(API, {
            method: 'POST',
            headers: myHeaders, 
            body: formData            
        }).then(res => res.json()).then(response => {
            if(parseInt(response.success)){
                this.setState({
                    sheets: response.data,
                    totalPages: response.total_pages
                });
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

  
    TableView(){
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-12 col-sm-12 col-lg-12">
                        <div className="padded-section">
                            {/* <Link to="createSheet" replace>
                                <button className="btn btn-primary flt-right mgn-bt"> Create Sheet </button>
                            </Link> */}
                            <Table
                                data={this.state.sheets}
                                header={["date","employee","total_tasks","total_hours"]}
                                sortBy={["date","employee","total_tasks","total_hours"]}
                                customHeaders={{"total_tasks":"Total Tasks", "total_hours":"Hours Worked"}}
                                dataStyle={{color:"white"}}
                                showActions = {true}        
                                actionTypes={["view"]}
                                showPagination={true}
                                totalPages={this.state.totalPages} 
                                currentPage={this.state.page}
                                onRowEdit = {(event, row) => { 
                                    this._switchToEditScreen(event,row)
                                }} 
                                onRowView = {(event, row) => { 
                                    this._switchToViewScreen(event,row)
                                }} 
                                onPaginate={(currentPage)=>{
                                   this._handlePageChange(currentPage)
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
