async function decode() {
	const text = document.getElementById("ciphertext").value;
	const key = document.getElementById("key").value;
	try {
		const response = await fetch("/api/playfair/decode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key }),
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
	const key = document.getElementById("key").value;
	try {
		const response = await fetch("/api/playfair/encode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.encoded
			? `Encoded Text: ${result.encoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
