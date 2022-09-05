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
        name:'Nombre Tabla',
        selector: row => row.nombre,
        sortable:true,
        grow:2
    },{
        name:'No. Tablas',
        selector: row => row.ntablas,
        sortable:true,
        grow:2
    },{
        name:'Linea',
        selector: row => row.linea,
        sortable:true
    }
]



export default class TablaBasedatos extends Component{
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
                <header align="center"><h1>Bases de Datos</h1></header>
                <Link id="BtnHome" to="/" className="btn btn-dark">Home</Link>
                <button id="showTabla" className="btn btn-dark" onClick={()=>this.showTabla()} >Mostrar Tabla</button>
                <DataTable 
                    columns={this.state.columnas}
                    data={this.state.Data}
                    title="Bases de datos"
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
        const url="http://localhost:5000/lbdatos"
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