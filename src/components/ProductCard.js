import React, { useState } from "react";
import "./Styles.css";
// import ProductDetails from "./ProductDetails";
import { useNavigate } from "react-router-dom";
import { NumberDropDown } from "./NumberDropDown";

function ProductCard({ wine, session }) {
  const [producNum, setProductNum] = useState(1);
  // const [itemInCart, setItemInCart] = useState(false)
  console.log();
  const [showAlert, setShowAlert] = useState(false);
  const navigate = useNavigate();
  function handleCardClick() {
    console.log(wine);
    navigate(`/products/${wine.id}`, { state: wine });
  }

  function handleAddToCartClick() {
    console.log("added to cart");

    // setItemInCart(true)

    fetch("/cart_items", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        shopping_session_id: localStorage.getItem("shopping_session"),
        product_id: wine.id,
        product_num: producNum,
      }),
    })
      .then((resp) => resp.json())
      .then((data) => console.log(data));

    setShowAlert(true);

    // Hide the alert after 2 seconds
    setTimeout(() => {
      setShowAlert(false);
    }, 1500);
  }

  return (
    <div>
      <div className="wine-card">
        <div className="wine-card-detail">
          <img src={wine.image_url} alt={wine.name} onClick={handleCardClick} />

          <h3 className="wine-card-name">{wine.name}</h3>
          <p className="wine-card-price">${wine.price}</p>
          <div className="wine-add-to-cart">
            {/* <NumberDropDown wine={wine} /> */}
            <button className="wine-card-button" onClick={handleAddToCartClick}>
              Add To Cart
            </button>
          </div>
          {showAlert && (
            <div className="alert-add-to-cart">{wine.name} added to cart!</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductCard;
