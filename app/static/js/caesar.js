async function decode() {
	const text = document.getElementById("ciphertext").value;
	const shift = parseInt(document.getElementById("shift").value, 10);

	try {
		const response = await fetch("/api/caesar/decode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, shift }),
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
	const shift = parseInt(document.getElementById("shift").value, 10);

	try {
		const response = await fetch("/api/caesar/encode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, shift }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.encoded
			? `Encoded Text: ${result.encoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
