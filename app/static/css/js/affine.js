async function decode() {
	const text = document.getElementById("ciphertext").value;
	const a_coefficient = parseInt(
		document.getElementById("a_coefficient").value,
		10
	);
	const b_coefficient = parseInt(
		document.getElementById("b_coefficient").value,
		10
	);
	try {
		const response = await fetch("/api/affine/decode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, a_coefficient, b_coefficient }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.decoded
			? `Encoded Text: ${result.decoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
async function encode() {
	const text = document.getElementById("ciphertext").value;
	const a_coefficient = parseInt(
		document.getElementById("a_coefficient").value,
		10
	);
	const b_coefficient = parseInt(
		document.getElementById("b_coefficient").value,
		10
	);

	const response = await fetch("/api/affine/encode", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ text, a_coefficient, b_coefficient }),
	});

	const result = await response.json();
	if (result.error)
		document.getElementById("error").textContent = result.error;
	else document.getElementById("result").textContent = result.encoded;
}
