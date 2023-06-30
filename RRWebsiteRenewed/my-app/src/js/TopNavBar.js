import "../css/Nav.css"
import PopUp from "./Popup.js"
import {useState, useEffect} from "react"



function sendHTML(HTMLContain){
    if (HTMLContain === "about"){
        return (<div class = "textContainer"> 

        </div> ); 
    }

    if (HTMLContain === "patches"){
        return (<div class = "textContainer"> 

        </div> );  
    }

    if (HTMLContain === "contact"){
        return (<div class = "textContainer"> 
        
        </div> ); 
    }

    if (HTMLContain === "github"){
        return (<div class = "textContainer"> 
        
        </div> ); 
    }
}


function TopNavBar(){
    const [selected, changeSelected] = useState('');
    const[popOut, Switching] = useState(false);
    const[storedHTML, changeHTML] = useState('')

    const handleIndentifier = (string) => {
        changeSelected(string)
        Switching(!popOut);
    }

    useEffect(()=>{
        changeHTML(sendHTML(selected))
    }, [selected, popOut])
    useEffect(() =>{}, [storedHTML])

    return (
        <div class = "NavBar">
        <div class = "InsideBox1">
             <button onClick = {() => handleIndentifier("about")}>About</button>
             <button onClick = {() => handleIndentifier("patches")}>Patches</button>
             <button onClick = {() => handleIndentifier("contact")}>Contact</button>
             <button onClick = {() => handleIndentifier("github")}>Github</button>
    
        </div>
        <div class = "InsideBox2"></div>   

        <PopUp trigger = {popOut} setTrigger = {Switching}>
        {storedHTML}
        </PopUp>
    </div>
    );
}

export default TopNavBar;