import { Component } from "react"
import React from 'react';
import CodeMirror from "@uiw/react-codemirror"
let codigo="";
export default class Principal extends Component{
    
    render(){
        return(
            <React.Fragment>
            <header align="center"><h1>DB Rust</h1></header>
            <div id="GButtons" className="btn-group">
                <button className="btn btn-secondary">
                Editor
                </button>
                <button className="btn btn-secondary">
                Ejecutar 
                </button>
                <div className="dropdown btn btn-secondary">
                Reportes
                <div className="dropdown-content">
                    <a >Reporte Tabla de Simbolos</a>
                    <a >Reporte Errores</a>
                    <a >Reporte Base de Datos Existentes</a>
                    <a >Reporte Tabla de Base de Datos</a>
                </div>
                </div>
                <button className="btn btn-secondary">
                Acerca de 
                </button>
            </div>
            <div  id="InOutCode" className="container-fluid">
                <div className="row">
                    <div className="col-5">
                        <CodeMirror value={this.codigo} height="100%" className="tAreaW" theme = "dark" align="left"  />
                    </div>
                    <div className="col-1"></div>
                    <div className="col-5">
                        <textarea id="consoleLfs" className=" tAreaW" ></textarea>
                    </div>
                </div> 
            </div>
            </React.Fragment> 
        )
    }


    
}