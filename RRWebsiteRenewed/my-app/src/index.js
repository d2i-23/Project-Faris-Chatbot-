import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import Chat from './js/Chat';
import TopNav from './js/TopNavBar';
import reportWebVitals from './js/reportWebVitals';


const root = ReactDOM.createRoot(document.getElementById('root'));
//const nav = ReactDOM.createRoot(document.getElementById('nav'));
//This is how the id gets rendered in the html file 


root.render(
  <React.StrictMode>
    <TopNav />
    <Chat />
  </React.StrictMode>
);



// If you want to start measuring performance in your Chat, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
