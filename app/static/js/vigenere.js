async function encode() {
	const text = document.getElementById("ciphertext").value;
	const key1 = document.getElementById("key1").value;
	const key2 = document.getElementById("key2").value;
	try {
		const response = await fetch("/api/vigenere/encode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key1, key2 }),
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
	const key1 = document.getElementById("key1").value;
	const key2 = document.getElementById("key2").value;
	try {
		const response = await fetch("/api/vigenere/decode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, key1, key2 }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.decoded
			? `Encoded Text: ${result.decoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
