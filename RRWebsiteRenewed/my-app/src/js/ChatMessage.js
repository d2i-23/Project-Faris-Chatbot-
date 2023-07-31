import '../css/Chat.css'
import {useState, useEffect, useRef} from 'react';
import PopUp from './Popup';
import DOMPurify from 'dompurify';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { monokai } from 'react-syntax-highlighter/dist/esm/styles/hljs';


function codeBlockOutput(child){


    const determineLanguage = (code) => {
        let thirdBackTick = code.search('```') + 2
        let firstEnter = code.search('\n')

        let language = code.substring(thirdBackTick + 1, firstEnter)

        return language
    }

    const searchCodeList = (text) => {
        let currentText = text 
        let locations = []
        let index = currentText.search('```')
        let coordinates = []


        while (index != -1){
            if (coordinates.length == 0){
                coordinates.push(index + (text.length - currentText.length))
            }

            else{
                
                coordinates.push(index + (text.length - currentText.length))
                locations.push([coordinates[0], coordinates[1]])

                coordinates = []
            }

            currentText = currentText.substring(index + 2, currentText.length)
            index = currentText.search('```')
        }
        

        let codeBlocks = []
        let previousEnd = 0

        if (locations.length == 0){
            return [text]
        }

        else{
            for (let i = 0; i < locations.length; i++){
                let codeString = text.substring(locations[i][0], locations[i][1] + 3)
                codeBlocks.push(text.substring(previousEnd, locations[i][0]))
                codeBlocks.push([determineLanguage(codeString), codeString.substring(codeString.search('\n') + 1, codeString.length - 3)])
                previousEnd = locations[i][1] + 1
            }
            codeBlocks.push(text.substring(previousEnd + 2, text.length))

            return codeBlocks
        }
    }


    return searchCodeList(child)
}
                                       

function ChatMessage(props){

   

    const [On, Switch] = useState(false)

    const className = props.user ? 'chatLogUser': 'chatLogAssistant'
    let requiersReadMore = false

    useEffect(() => {console.log(On)}, [On])


    const processLength = (child) => {
        if (child.length > 200){
            requiersReadMore = true
            return child.substring(0, 200) 
        }

        return child
    } 

    const processEnter = (child, big = false) => {
        child = DOMPurify.sanitize(child)
        return <h3 class = {big ? 'classBox' : ''} dangerouslySetInnerHTML={{__html: child.replace(/\n/g, '<br />')}}></h3>
    }

    let displayedText = processLength(props.realChild)
    let boxText = !props.user ? codeBlockOutput(props.realChild) : [props.realChild]
    
    console.log(boxText)

    return (
    <div class = {className} >
        <h3 onClick={() => {Switch(true)}}>{processEnter(displayedText + (requiersReadMore ? '...' : ''))}</h3>
        <PopUp trigger = {On} setTrigger = {Switch}     Color = {props.user ? '#eb8042': '#c85de3'}> 
        {On ? boxText.map((items, index) => (
        
           typeof boxText[index] == "string" ? processEnter(boxText[index], true) : <SyntaxHighlighter style = {monokai} language = {boxText[index][0]}>{boxText[index][1]}</SyntaxHighlighter>

        )) : ''} 
        </PopUp>
    
    </div>)
}


export default ChatMessage