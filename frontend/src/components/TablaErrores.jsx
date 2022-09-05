import React, { Component,useState,useEffect } from "react"
import DataTable from 'react-data-table-component'
import {Link} from 'react-router-dom'



const datoprueba=[
]

const columnas=[
    {
        name:'No',
        selector: row => row.No,
        sortable:true
    },
    {
        name:'Descripcion',
        selector: row => row.descripcion,
        sortable:true,
        grow:3
    },{
        name:'Ambito',
        selector: row => row.ambito,
        sortable:true
    },{
        name:'Linea',
        selector: row => row.linea,
        sortable:true
    },{
        name:'Columna',
        selector: row => row.columna,
        sortable:true
    },{
        name:'Fecha y Hora',
        selector: row => row.tiempo,
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
    showTabla=async()=>{
        const url="http://localhost:5000/lerrores"
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