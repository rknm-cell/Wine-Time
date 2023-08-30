import React from 'react'
import "./Styles.css";
import wine from '../wine.mp4'
import { useNavigate } from 'react-router-dom';

function Home() {
const navigate = useNavigate();
  function handleClick() {
    console.log(wine)
    navigate('/Home')
  }
return (
  <div onClick={handleClick} id='main' className='main'>
    <div  className='overlay'></div>
        <video src={wine} autoPlay loop muted />
        <div className='content'>
            <div className='textContent'>
              <h1 className='homepageName'>Wine Time</h1>
              <h3 className='homepageTitle'>Natural Wines</h3>
            </div> 
        </div>
  </div>
)
  
}

export default Home