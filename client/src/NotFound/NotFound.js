import React, { Component } from 'react';
import NotFoundLogo from '../assets/images/not-found.png';


export default class NotFound extends Component {

    componentDidMount(){
        console.log("Hi")
    }
  render(){
      return(
            <div>
                {/* <img src={NotFoundLogo} alt="404 Not Found" className="not-found" /> */}
            </div>
      )
  }

}