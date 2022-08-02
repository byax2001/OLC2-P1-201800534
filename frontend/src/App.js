import './App.css';
import React from 'react';
import {Route,BrowserRouter,Routes} from 'react-router-dom';

//BOOTSTRAPT
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/bootstrap/dist/js/bootstrap.js';
//CODEMIRROR
import CodeMirror from '@uiw/react-codemirror';
//PAGINAS WEB
import Principal from './components/Principal';


function App() {
  return (
    <BrowserRouter>
      <Routes>
      <Route path="/" exact element={<Principal />} />
      </Routes>
    </BrowserRouter>
    
  );
}
//Obligatoriamente colocar mayuscula al inicio del nombre de cada componente
function Console2() { 
  return <h1>HOla </h1>
  ;
}
export default App;
