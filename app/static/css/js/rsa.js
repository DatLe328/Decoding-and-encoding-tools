async function generateKeys() {
	const p = document.getElementById("p").value;
	const q = document.getElementById("q").value;
	const e = document.getElementById("e").value;

	try {
		const response = await fetch(`/api/rsa/generate-keys`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ p, q, e }),
		});

		const result = await response.json();
		document.getElementById("keys").innerText = result.keys
			? `Generated Keys:\nPublic Key: ${result.keys.public}\nPrivate Key: ${result.keys.private}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("keys").innerText = `Error: ${error.message}`;
	}
}
async function encode() {
	const text = document.getElementById("ciphertext").value;

	try {
		const response = await fetch("/api/rsa/encode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text }),
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

	try {
		const response = await fetch("/api/rsa/decode", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text }),
		});

		const result = await response.json();
		document.getElementById("result").innerText = result.decoded
			? `Encoded Text: ${result.decoded}`
			: `Error: ${result.error}`;
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
