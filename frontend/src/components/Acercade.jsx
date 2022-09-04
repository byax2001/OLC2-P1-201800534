import React, { Component,useState,useEffect } from "react"
import CodeMirror from "@uiw/react-codemirror"
import {Link} from 'react-router-dom'


export default class Acercade extends Component{
    
    render(){
        return(<React.Fragment>
            <header align="center"><h1>Datos del estudiante</h1></header>
            <Link id="BtnHome" to="/" className="btn btn-dark">Home</Link>
            <h2 className="font-weight-normal text-light">Carnet: 201800534</h2>
            <h2 className="font-weight-normal text-light">Brandon Oswaldo Yax Campos</h2>
            <h2 className="font-weight-normal text-light">ORGANIZACION DE LENGUAJES Y COMPILADORES 2 Sección A</h2>
            </React.Fragment>
            )
            
    }
}