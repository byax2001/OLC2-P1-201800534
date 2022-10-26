import { Component, useEffect } from "react"
import React,{useState,useRef} from 'react';
import CodeMirror from "@uiw/react-codemirror"
import {Link, resolvePath} from 'react-router-dom'




let consola=""


export default class Principal extends Component{
    
    constructor() {
        super();
        this.state={
            consola:consola,
            entrada:""
        }
        
    }
    render(){
        return(
            <React.Fragment>
            <header align="center"><h1>DB Rust</h1></header>
            <button id="CopiarC3d" className="btn btn-dark btnEffect" onClick={()=>{this.copyToClipBoard()}}>Copiar </button>
            <div id="GButtons" className="btn-group">
                <button className="btn btn-secondary" onClick={()=>this.Execute()}>
                Ejecutar 
                </button>
                <div className="dropdown btn btn-secondary">
                Reportes
                <div className="dropdown-content">
                    <Link to="/tsimbolos">Tabla de Simbolos</Link>
                    <Link to="/terrores">Reporte de Errores</Link>
                    <Link to="/tbdatos">Reporte Base de datos existentes</Link>
                    <Link to="/tt_bdatos">Reporte de tabla de base de datos</Link>
                </div>
                </div>
                <Link to="/acercade"  className="btn btn-secondary">Acerca de</Link>
            </div>
            <div  id="InOutCode" className="container-fluid">
                <div className="row">
                    <div className="col-6 p-0">
                        <CodeMirror ref={this.entrada} id="textAnalizar" width="100%"  height="100%" className="tAreaW" 
                        theme = "dark" align="left" 
                        mode="javascript"
                        onChange={(value) => {this.setState({entrada: value}) }}
                        />
                    </div>
                    
                    <div className="col-6 p-0">
                        <textarea id="consoleLfs" className=" tAreaW" value={this.state.consola}
                            onChange={(e)=>{this.setState({consola:e.target.value})}}
                        ></textarea>
                    </div>
                </div> 
            </div>
            </React.Fragment> 
        )


    }
    componentDidMount() { /*SE EJECUTA AL INICIO O AL RECARGAR PAGINA */
        this.setState({
            consola:""
        })  
    }
    
    copyToClipBoard() {
        var content = this.state.consola;
        navigator.clipboard.writeText(content)
        alert("Codigo 3D Copiado!");
    }

    Execute=async()=>{
        const url="http://localhost:5000/DataAnalisisC3d"
        let config={
            method:'POST',       //ELEMENTOS A ENVIAR
            body:JSON.stringify([{entrada:this.state.entrada}]),
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
        }
    
        const res= await fetch(url,config)
        const data =await res.json()
        console.log(data)
        this.setState({
            consola:data.Contenido
        })
        //esto lo devuelve como una lista {hola: "pureba"}
    }


    
}