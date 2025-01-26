async function calculateKey() {
	const p = parseInt(document.getElementById("p").value);
	const g = parseInt(document.getElementById("g").value);
	const privateKeyA = parseInt(document.getElementById("privateKeyA").value);
	const privateKeyB = parseInt(document.getElementById("privateKeyB").value);
	console.log(p);
	try {
		const response = await fetch(`/api/diffie-hellman/exchange`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ p, g, privateKeyA, privateKeyB }),
		});

		const result = await response.json();
		if (result.error) {
			document.getElementById(
				"result"
			).innerText = `Error: ${result.error}`;
		} else {
			document.getElementById("result").innerText = `
            Alice's Public Key: ${result.publicKeyA}\n
            Bob's Public Key: ${result.publicKeyB}\n
            Shared Secret Key: ${result.sharedKey}
          `;
		}
		console.log(result)
	} catch (error) {
		document.getElementById("result").innerText = `Error: ${error.message}`;
	}
}
