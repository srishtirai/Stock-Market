import React, { useState, useEffect, Component } from 'react';
import ReactSearchBox from 'react-search-box'
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

class Form extends React.Component {
  constructor(props) {
    super(props);
    this.state={
        data:''
      }
        this.updateState = this.updateState.bind(this);
    }

    updateState = (event) => {
        let nam = event.target.name;
        let val = event.target.value;
        this.setState({[nam]: val});
    }

  render() {
  return (

      <div className="main">
      <form  method="post">
      <div className="row_main">
      <ReactSearchBox
        name="name"
        placeholder="Enter Company Name"
        value={this.data}
        onchange={this.updateState}
        />
      </div>
      <div className="row" >
        <button className="but" ><FontAwesomeIcon icon={faSearch} size="lg" color="white"/></button>
      </div></form>
      </div>
  );
}
}

export default Form;