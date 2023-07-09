import { LAppDelegate } from '../src/lappdelegate';
import React, { useState, useEffect } from 'react';

function ReactLive2d(props) {

    // 容器样式
    let containerStyle = {
        position: 'fixed',
        top: props.top ? props.top : '0',
        bottom: props.bottom ? props.bottom : '0',
        left: `calc(60% - ${props.width})`
    }
    // canvas样式
    let canvasStyle = {
        position: 'relative',
        top: props.top ? props.top : '',
        right: props.right ? props.right : '0',
        bottom: props.bottom ? props.bottom : '0',
        left: props.left ? props.left : ''
    }

    useEffect(() => {
        if (!navigator.userAgent.match(/mobile/i) || props.MobileShow == true) {

            if (LAppDelegate.getInstance().initialize() == false) {
                return;
            }
            LAppDelegate.getInstance().run();
            // window.onbeforeunload = () => LAppDelegate.releaseInstance();
        }
    }, []);

    const [previousSave, newSave] = useState('')
    const [previousSaveMood, newSaveMood] = useState('')
    const [previousSaveTime, newSaveTime] = useState(0)
    const [currentAudio, newAudio] = useState(new Audio)

    if (props.token !== previousSave){
        newSave(props.token)
        newSaveMood(props.mood)
        newSaveTime(props.time)
    }

    useEffect( ()=> {

        if (previousSave !== ''){
            console.log(previousSaveMood)
            if (previousSaveMood != 'exp_01'){
                LAppDelegate.getInstance().setExpression(previousSaveMood)
            }
            
            currentAudio.pause()
            LAppDelegate.getInstance().audio(previousSave, currentAudio)


            if (previousSaveMood != 'exp_01'){

                const timedDefault = () => {
                    LAppDelegate.getInstance().setExpression('exp_01')
                }
                setTimeout(timedDefault, previousSaveTime * 1000 + 100)
                //LAppDelegate.getInstance().setExpression('exp_01')
            }
        }
    }, [previousSave, previousSaveMood, previousSaveTime])

    useEffect(() => {}, [currentAudio])


    useEffect(() =>{

        if(props.release==true){
            LAppDelegate.releaseInstance();
        }
    }, [props.release])

    return (
        <div>
            <div
                style={containerStyle}
                width={props.width ? props.width : '300'}
                height={props.height ? props.height : '500'}
                id="live2d-container">
                <div id="live2d-hidden"
                    style={{
                        width:'100%',
                        height:'100%',
                        position:'absolute',
                        top:'0',
                        left:'0',
                        zIndex:'2'
                    }}
                >

                </div>
                <canvas
                    id="live2d"
                    style={canvasStyle}
                    width={props.width ? props.width : '300'}
                    height={props.height ? props.height : '500'}
                    className="live2d"
                >
                </canvas>
            </div>
        </div>
    )
}

export default ReactLive2d