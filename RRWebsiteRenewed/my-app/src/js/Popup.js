import "../css/Nav.css"


function PopUp(props){
    const handleChildClick = (event) => {
        event.stopPropagation();
      };

    return ((props.trigger) ? (<div class = "oddBox" onClick={() => {props.setTrigger(false)}}> 
        <center><div class = "oddBoxInner" onClick = {handleChildClick}>
        {props.children}    
        </div></center>
    </div>) : "");
}

export default PopUp;