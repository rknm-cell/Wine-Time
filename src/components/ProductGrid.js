import React, { useState } from "react";
import "./Styles.css";
import ProductCard from "./ProductCard";
// import Search from "./Search";
// import Sort from "./Sort";

function Sort({ setSortValue }) {
  return (
    <div className="sortbar">
      <label>Sort Wines: </label>
      <select
        className="select"
        defaultValue={"DEFAULT"}
        onChange={(e) => setSortValue(e.target.value)}
      >
        <option value="a.id > b.id">Bestselling</option>
        <option value="a.name > b.name">Alphabetical Ascending</option>
        <option value="b.name > a.name">Alphabetical Descending</option>
        <option value="a.price > b.price">Price Ascending</option>
        <option value="b.price > a.price">Price Descending</option>
        {/* <option value="b.best_selling > a.best_selling">Bestselling</option> */}
      </select>
    </div>
  );
}

function Search({ onSearch, searchInput }) {
  return (
    <div className="searchbar">
      <label htmlFor="search">Search Wines: </label>
      <input
        className="bar"
        value={searchInput}
        type="text"
        id="search"
        placeholder="    Type a name to search..."
        onChange={(e) => onSearch(e.target.value)}
      />
    </div>
  );
}

function ProductGrid({ user, session, wines, searchInput, onSearch }) {
  const [sortValue, setSortValue] = useState("");

  return (
    <>
      <div className="product-grid-header">
        <Search searchInput={searchInput} onSearch={onSearch} />
        <Sort setSortValue={setSortValue} />
      </div>
      <div className="product-grid">
        
        {[...wines]
          .sort((a, b) => (eval(sortValue) ? 1 : -1))
          .map((wine) => {
            return (
              <ProductCard
                wine={wine}
                key={wine.name}
                user={user}
                session={session}
              />
            );
          })}
      </div>
    </>
  );
}

export default ProductGrid;
