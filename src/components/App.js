import React, { useEffect, useState} from "react";
import { Route, Routes, useNavigate } from "react-router-dom";
import "./Styles.css";

import ProductGrid from "./ProductGrid";
import Login from "./Login";
import ProductDetails from "./ProductDetails";
import Cart from "./Cart";
import Header from "./Header";
import SignUp from "./Signup";
import Checkout from "./Checkout";
import LandingPage from "./LandingPage";

function App() {
  const [user, setUser] = useState(null);

  const [session, setSession] = useState(null);
  const [wines, setWines] = useState([]);
  const [searchInput, setSearchInput] = useState("");

  const [sortType, setSortType] = useState("default");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/check_session").then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);
  function handleLogin(user) {
    setUser(user);
    navigate("/");
  }

  useEffect(() => {
    fetch("/products") // localhost works here too!
      .then((r) => r.json())
      .then(setWines);
  }, []);

  function handleLogout() {
    setUser(null);
  }
  function onSearch(input) {
    console.log(input);
    setSearchInput(input);
  }
  const filteredWines = wines.filter((wine) => {
    var wineNames = wine.name.toLowerCase().includes(searchInput.toLowerCase());

    return wineNames;
  });

  const wineAscending = [...wines].sort((a, b) => (a.name > b.name ? 1 : -1));
  const wineDescending = [...wines].sort((b, a) => (b.name > a.name ? 1 : -1));

  const defaultSort = [...wines].sort((a, b) => (a.id > b.id ? 1 : -1));
  function handleSortType(sort) {
    if (sort === "ascending alphabetical") {
      setSortType(wineAscending);
    } else if (sort === "descending alphabetical") {
      setSortType(wineDescending);
    }
  }

  // const images = [
  //   "/src/pash-rash.jpg",
  //   "/src/its-your-birthday.jpg",
  //   "/src/naturalwine_hero.webp",
  //   "/src/alba.jpg",
  // ];

  return (
    <div className="App">
      <div>
        <Header user={user} onLogout={handleLogout} />
        {/* <Search searchInput={searchInput} onSearch={onSearch}/> */}
        <Routes>
          <Route path="/" element={<LandingPage />}></Route>
          {/* <Route path="/home" element={<Home images={images} />}></Route> */}
          <Route
            path="/products"
            element={
              <ProductGrid
                searchInput={searchInput}
                onSearch={onSearch}
                wines={filteredWines}
                user={user}
                session={session}
              />
            }
          ></Route>
          {user ? null : (
            <Route
              path="/login"
              element={<Login onLogin={handleLogin} user={user} />}
            ></Route>
          )}
          {user ? null : (
            <Route
              path="/create-account"
              element={
                <SignUp
                  user={user}
                  onLogin={handleLogin}
                  setSession={setSession}
                />
              }
            ></Route>
          )}
          <Route
            path="/products/:id"
            element={<ProductDetails session={session} />}
          ></Route>
          <Route
            path="/cart"
            element={<Cart user={user} session={session} />}
          ></Route>
          <Route path="/checkout" element={<Checkout />}></Route>
        </Routes>
      </div>
    </div>
  );
}

export default App;
