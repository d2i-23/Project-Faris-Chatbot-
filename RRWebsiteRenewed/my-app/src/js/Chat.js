import '../css/Chat.css';
import {useState, useEffect, useRef} from 'react';
import DOMPurify from 'dompurify';
import ReactLive2d from './ReactLive2d';


// Initialization code for Live2DCubismFramework

function Chat(){
  //const [message, addMessage] = useState([])

  //let messageList = [];
  const[chatHTML, update] = useState([]);
  const[assistantHTML, update2] = useState([]);
  const [message, addKey] = useState('');
  const [active, isActive] = useState(false);
  const [realMessage, needResponse] = useState(false)
  const chatboxRef = useRef(null)
  
  const setMessage = (event = null) => {

    if (event !== null){
      event.preventDefault();
    }
    const date = new Date();
    var dictionary = {'date': `${date.getMonth()}/${date.getDate()}`, 
                      'time': `${date.getHours()}:${date.getMinutes() < 10 ? '0' : ''}${date.getMinutes()}`, 
                      'year': `${date.getFullYear()}`,
                      'role': 'User',
                      'message': DOMPurify.sanitize(message)};


    update([...chatHTML, dictionary])
    
    addKey('');
    document.getElementById('messageBox').value = '';
    document.getElementById('messageBox').style.height = '20px'

    needResponse(true);
    //console.log(chatHTML);

  }

  const addKeyStroke = (event) => {
  
    isActive(true);
    setTimeout(() => {isActive(false);}, 500); // Adjust the delay duration as needed


    addKey(event.target.value);
    const messageBox = document.getElementById('messageBox');
    messageBox.addEventListener('input', function() {
      
      this.style.height = 'auto'; // Reset the height to auto
      var height = this.scrollHeight;
  
      if (height < 75){
        this.style.height = height + 'px'
      }
      else{
        //this.style.height = 'fit-content'
        this.style.height = '75px'
      }
    })

  }
  
  const detectEnter = (event) => {
    if (event.key === "Enter"){
      console.log('here')
      if (event.shiftKey == false){
        event.preventDefault()
        setMessage()
      }
      else{
        event.target.value += '\n'
      }
    }
  }


  const postData = async () => {
    if (chatHTML.length !== 0){
      const response = await fetch('/returnResponse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(chatHTML[chatHTML.length - 1]),
      }
      )

      const message = await response.json()
      update2([...assistantHTML, message])
      
  };
  } 



  const processLength = (text, id) => {
    if (text.length <= 200){
      return (<h3>{text}</h3>)
    }

    else{
      return (<h3 >{text.substring(0, 175) + '...'}<a id = {`buttonID${id}`}class = 'readMore'>Read More</a></h3>)
    }
  }
  /*
  document.getElementsByClassName('readMore').addEventListener('click', function(){
    index = Number.parseInt(this.id.substring(9, this.id.substring.length - 1))

    document.getElementById('overallContainer').appendChild(
      <PopUp trigger = {true} setTrigger = {}>
      {}
      </PopUp>
    )
  })
  */


  useEffect(() => {
    if (realMessage){
      postData();
      needResponse(false);
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight
    } }, [chatHTML]);

  useEffect(() => {chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight}, [assistantHTML])
  

  return (

    <div class = "overallContainer"> 
      
      <div class = 'chatBox'>
          <br></br>
          <form onSubmit = {setMessage} >
            <button id = 'chatEnter' type = 'submit'>>>></button>
            <br/>
            <textarea class = {active ? 'active' : ''} onChange = {addKeyStroke} onKeyDown = {detectEnter}type = "text" id = 'messageBox' ></textarea>

          </form>
          <div id = 'chatBorderTop'>
          <div id = 'chat' ref = {chatboxRef}>  
            {chatHTML.map((items, index) => (
            <div class = "chatDialogue">
              <div class = "timeStampInclude">{chatHTML[index]['date']} | {chatHTML[index]['time']}
               <div class = "chatLogUser">{processLength(chatHTML[index]['message'], index)}</div>
              </div>
              <div class = "chatDialogue reply">
                <div class = "chatLogAssistant"><h3>{assistantHTML[index] !== undefined  ? assistantHTML[index]['message'] : 
                (<div class = "dotContainer">
                  <div id = "dot1"></div>
                  <div id = "dot2"></div>
                  <div id = "dot3"></div>
                </div>)
                
                }</h3></div>
              </div>
            </div> ))}
          </div>
          
          </div>
          <br></br>
          <h2 class = {active ? 'active' : ''} >Live Chat</h2>
        </div>
        

        <div class = "AnimationBox" ><ReactLive2d 
        token =  {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['token']: ''}`}
        mood = {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['mood']: ''}`}
        time = {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['time']: ''}`}
        width={1200} 
        height={1200}
        top = {2}/>
        </div>
    </div>

  )
}
// /<!--<Animation data = {(assistantHTML.length !== 0) ? assistantHTML[assistantHTML.length - 1] : ""}/>--?
export default Chat;
