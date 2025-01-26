document.addEventListener("DOMContentLoaded", function () {
	generateMatrixInput();
});
function generateMatrixInput() {
	const matrixSize = parseInt(document.getElementById("matrixSize").value);
	const matrixInputDiv = document.getElementById("matrixInput");
	matrixInputDiv.innerHTML = "";

	const label = document.createElement("label");
	label.textContent = `Enter Key Matrix (${matrixSize}x${matrixSize}):`;
	matrixInputDiv.appendChild(label);

	for (let i = 0; i < matrixSize; i++) {
		const rowDiv = document.createElement("div");
		rowDiv.classList.add("matrix-row");

		for (let j = 0; j < matrixSize; j++) {
			const input = document.createElement("input");
			input.type = "number";
			input.classList.add("matrix-cell");
			input.id = `matrix-${i}-${j}`;
			input.placeholder = "0";
			rowDiv.appendChild(input);
		}

		matrixInputDiv.appendChild(rowDiv);
	}
}
function parseMatrix(matrixSize) {
	const matrix = [];
	for (let i = 0; i < matrixSize; i++) {
		const row = [];
		for (let j = 0; j < matrixSize; j++) {
			const value = document.getElementById(`matrix-${i}-${j}`).value;
			if (value === "") {
				throw new Error(
					`Matrix cell [${i + 1}, ${j + 1}] cannot be empty.`
				);
			}
			row.push(parseInt(value, 10));
		}
		matrix.push(row);
	}
	return matrix;
}
async function encode() {
	const text = document.getElementById("ciphertext").value;
	const matrixSize = parseInt(document.getElementById("matrixSize").value);
	const order = document.getElementById("order").value;

	try {
		const keyMatrix = parseMatrix(matrixSize);
		const response = await fetch(`/api/hill/encode`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key_matrix: keyMatrix, order }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.encoded
			? `Encoded Text: ${result.encoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}

async function decode() {
	const text = document.getElementById("ciphertext").value;
	const matrixSize = parseInt(document.getElementById("matrixSize").value);
	const order = document.getElementById("order").value;

	try {
		const keyMatrix = parseMatrix(matrixSize);
		const response = await fetch(`/api/hill/decode`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key_matrix: keyMatrix, order }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.decoded
			? `Decoded Text: ${result.decoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
