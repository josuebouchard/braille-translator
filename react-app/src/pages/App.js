import React, { useState } from 'react';
import '../scss/App.scss';
import BrailleInput from "../components/BrailleInput";
import data from "../data.json"

function App() {
	let [currentBraillePattern, setCurrentBraillePattern] = useState([]);
	let [word, setWord] = useState([]);

	let inputChange = (data) => {
		setCurrentBraillePattern(data)
	}

	const computedBrailleDotPattern = () => {
		let brailleDotPattern = currentBraillePattern
			.map((isSelected, index) => isSelected ? index + 1 : "")
			.filter(elem => elem !== "")
			.join("");
		return brailleDotPattern !== "" ? brailleDotPattern : "0";
	}

	const insertWord = () => {
		let patternData = data.filter(elem => elem["dotPattern"] === computedBrailleDotPattern())[0];
		console.log(patternData);
		setWord([...word, patternData]);
	}
	const deleteWord = () => { setWord(word.slice(0, -1)); }
	const clearWord = () => { setWord([]); }

	return (
		<div className="App">
			<BrailleInput inputChange={inputChange} />
			<span>Dot pattern: {computedBrailleDotPattern()}</span>
			<div>
				<button onClick={insertWord}>Insert</button>
				<button onClick={deleteWord}>Delete</button>
				<button onClick={clearWord}>Clear</button>
			</div>
			<div id="brailleText">
				{word.map((elem, index) => <React.Fragment key={index}>
					<img src={"data:image/png;base64, " + elem.imageBase64} />
					<span>{elem.meanings["english braille"]}</span>
				</React.Fragment>)}
			</div>
		</div>
	);
}

export default App;
