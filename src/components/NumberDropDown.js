import React from "react";

export const NumberDropDown = ({wine}) => {
  
    const numbers = Array.from({ length: wine.units }, (_, index) => index + 1);
  

  return (
    <div>
      
      <select id="numberDropdown">
      {numbers.map((number) => (
          <option key={number} value={number}>
            {number}
          </option>
        ))}
      </select>
    </div>
  );
};
