import "../css/Nav.css"


function PopUp(props){
    const handleChildClick = (event) => {
        event.stopPropagation();
      };


    return ((props.trigger) ? (<div class = "oddBox" onClick={() => {props.setTrigger(false)}}> 
        <center><div class = "oddBoxInner" style = {{borderColor: props.Color != undefined ? props.Color : '#454440'}} onClick = {handleChildClick}>
        {props.children}    
        </div></center>
    </div>) : "");
}

export default PopUp;