import React, { Component,useState,useEffect } from "react"
import DataTable from 'react-data-table-component'
import {Link} from 'react-router-dom'

let codigo="";

const datoprueba=[{nombre:"Brandon",tiposimbolo:"Funcion",tipodato:"string",ambito:"Global",fila:12,columna:14},
{nombre:"Alex",tiposimbolo:"Variable",tipodato:"i64",ambito:"Local",fila:32,columna:71}
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

export const UpdateTabla=function(){
    datoprueba.push({nombre:"Fernandojijo",tiposimbolo:"Variable",tipodato:"i64",ambito:"Local",fila:32,columna:71})
    console.log("Xd")
    return datoprueba
}
export const sentServer=function(texto){
    const url="https://localhost:5000/"

}


export default class TablaErrores extends Component{
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
                <header align="center"><h1>Tabla de Errores</h1></header>
                <Link id="BtnHome" to="/" className="btn btn-dark">Home</Link>
                <button id="showTabla" className="btn btn-dark" onClick={()=>this.showTabla()} >Mostrar Tabla</button>
                <DataTable 
                    columns={this.state.columnas}
                    data={this.state.Data}
                    title="Tabla de Errores"
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
    showTabla(){
        this.setState({
            Data: []
          },
          () => {
            this.setState({
                Data: UpdateTabla()
              });
          }
        );
    }

}