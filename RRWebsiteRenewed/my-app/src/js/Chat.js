import '../css/Chat.css';
import {useState, useEffect, useRef} from 'react';
import DOMPurify from 'dompurify';
import ReactLive2d from './ReactLive2d';
import ChatMessage from './ChatMessage';


// Initialization code for Live2DCubismFramework

function Chat(){
  //const [message, addMessage] = useState([])

  //let messageList = [];
  const [sentMemory, updateMemory] = useState([])
  const[chatHTML, update] = useState([]);
  const[assistantHTML, update2] = useState([]);
  const [message, addKey] = useState('');
  const [active, isActive] = useState(false);
  const [realMessage, needResponse] = useState(false)
  const chatboxRef = useRef(null)
  const [expandChat, expand] = useState(true)

  useEffect(() => {console.log('here'); console.log(sentMemory)}, [sentMemory])
  
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
      if (event.shiftKey == false && chatHTML.length == assistantHTML.length){
        event.preventDefault()
        setMessage()
      }
      else{
        event.target.value += '\n'
      }
    }
  }


  const postData = async () => {
    let savedJson = chatHTML[chatHTML.length - 1]
    savedJson['sentMemory'] = sentMemory

    if (chatHTML.length !== 0){
      const response = await fetch('/returnResponse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(savedJson),
      }
      )

      const message = await response.json()
      update2([...assistantHTML, message['response'][0]])
      updateMemory(message['sentMemory']) 
      
  };
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

  const processEnter = (child) => {
    child = DOMPurify.sanitize(child)

    return <h3 dangerouslySetInnerHTML={{__html: child.replace(/\n/g, '<br />')}}></h3>
  }


  useEffect(() => {
    if (realMessage){
      postData();
      needResponse(false);
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight
    } }, [chatHTML]);

  useEffect(() => {chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight}, [assistantHTML])
  //<button id = 'voiceInput'>hi</button>

  useEffect(() => {}, [expandChat])

  return (

    <div class = "overallContainer"> 
      
      <div class = 'chatBox' style = {{visibility: expandChat ? "visible" : "hidden"}}>
      <br></br><br></br>
          <form onSubmit = {setMessage} style = {{visibility: "visible"}}>
          
            <div style = {{"display": "flex", marginLeft: "80%"}}> 
            <div id = 'expandOrNot' style = {{margin: 5, background: "rgb(0, 0, 0, 0.6)", "border": expandChat ? "solid 2px #eb8042" : "solid 2px #c85de3" }} onClick = {() => {expand(!expandChat)}}></div>
            {chatHTML.length == assistantHTML.length ? <button id = 'chatEnter' type = 'submit' style = {{margin: 5, background: "rgb(0, 0, 0, 0.6)"}}> >>></button> : <button id = 'fakeEnter' type = 'button' style = {{margin: 5, background: "rgb(0, 0, 0, 0.6)"}}>...</button>}
            </div>
            <br></br>
            <textarea class = {active ? 'active' : ''} onChange = {addKeyStroke} onKeyDown = {detectEnter}type = "text" id = 'messageBox' ></textarea> 

          </form>
          
          <div id = 'chatBorderTop'>

          <div id = 'chat' ref = {chatboxRef} >  
            {chatHTML.map((items, index) => (
            <div class = "chatDialogue">
              <div class = "timeStampInclude">{chatHTML[index]['date']} | {chatHTML[index]['time']}
              <ChatMessage user = {true} realChild = {chatHTML[index]['message']}></ChatMessage>
              </div>
              <div class = "chatDialogue reply">
              {assistantHTML[index] !== undefined  ? <ChatMessage user = {false} realChild = {assistantHTML[index]['message']}></ChatMessage> : 
                <div class = "chatLogAssistant">
                <div class = "dotContainer">
                  <div id = "dot1"></div>
                  <div id = "dot2"></div>
                  <div id = "dot3"></div>
                </div>
                
                </div>}
              </div>
            </div> ))}
          </div>
          
          </div>
          <br></br>

        </div>
        
        <div style = {{height: 900, width: 600, overflow: "hidden"}}>
        <ReactLive2d 
        token =  {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['token']: ''}`}
        mood = {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['mood']: ''}`}
        time = {`${assistantHTML.length !== 0 ? assistantHTML[assistantHTML.length - 1]['time']: ''}`}
        width={600} 
        height={1700}
        top = {0}/>

        </div>


    </div>

  )
}
// /<!--<Animation data = {(assistantHTML.length !== 0) ? assistantHTML[assistantHTML.length - 1] : ""}/>--?
export default Chat;
