import React, { useState } from "react";
import "../scss/BrailleInput.scss"

const BrailleInput = ({inputChange}) => {
	let [state, setState] = useState([false, false, false, false, false, false]);

	const handleInputChange = (event) => {
		let target = event.target;
		let newState = [...state];
		newState[target.id-1] = target.checked;

		setState(newState);
		inputChange(newState);
	}

	return (
		<div id="brailleInput">
			<input type="checkbox" id="1" checked={state[0]} onChange={handleInputChange}/>
			<input type="checkbox" id="2" checked={state[1]} onChange={handleInputChange}/>
			<input type="checkbox" id="3" checked={state[2]} onChange={handleInputChange}/>
			<input type="checkbox" id="4" checked={state[3]} onChange={handleInputChange}/>
			<input type="checkbox" id="5" checked={state[4]} onChange={handleInputChange}/>
			<input type="checkbox" id="6" checked={state[5]} onChange={handleInputChange}/>
		</div>
	);
}

export default BrailleInput;