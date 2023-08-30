import React from 'react'
import "./Styles.css";
import wine from '../wine.mp4'
import { useNavigate } from 'react-router-dom';
import ImageCarousel from './ImageCarousel';
function Home() {
const navigate = useNavigate();
  function handleClick() {
    console.log(wine)
    navigate('/products')
  }

  const images = [
    
  ]
return (
  <>
  <ImageCarousel/>
  </>
)
  
}

export default Home