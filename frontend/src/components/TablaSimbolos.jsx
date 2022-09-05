import React, { Component,useState,useEffect } from "react"
import DataTable from 'react-data-table-component'
import {Link} from 'react-router-dom'



const datoprueba=[
]

const columnas=[
    {
        name:'ID',
        selector: row => row.nombre,
        sortable:true
    },
    {
        name:'Tipo Simbolo',
        selector: row => row.tiposimbolo,
        sortable:true
    },{
        name:'Tipo Dato',
        selector: row => row.tipodato,
        sortable:true
    },{
        name:'Ambito',
        selector: row => row.ambito,
        sortable:true
    },{
        name:'Fila',
        selector: row => row.fila,
        sortable:true
    },{
        name:'Columna',
        selector: row => row.columna,
        sortable:true
    }
]




export default class TablaSimbolos extends Component{
    constructor() {
        super();
        this.state={
            columnas:columnas,
            Data:datoprueba
        }
    }
    render(){
        return (   
            <React.Fragment>
                <header align="center"><h1>Tabla de Simbolos</h1></header>
                <Link id="BtnHome" to="/" className="btn btn-dark">Home</Link>
                <button id="showTabla" className="btn btn-dark" onClick={()=>this.showTabla()} >Mostrar Tabla</button>
                <DataTable 
                    columns={this.state.columnas}
                    data={this.state.Data}
                    title="Tabla de Simbolos"
                    pagination
                    fixedHeader
                    fixedHeaderScrollHeight="600px"
                /> 
           </React.Fragment>
        )
    }
    componentDidMount() {
        this.setState({
            Data:[]
        })  
    }
    showTabla=async()=>{
        const url="http://localhost:5000/ltsimbolos"
        let config={
            method:'POST',       //ELEMENTOS A ENVIAR
            //body:JSON.stringify([{entrada:this.state.entrada}]),  no hay necesidad de mandar nada aqui
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
        }
    
        const res= await fetch(url,config)
        const data =await res.json()
        this.setState({
            Data:data.Contenido
        })
        //esto lo devuelve como una lista {hola: "pureba"}
    }

}